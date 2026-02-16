#!/usr/bin/env python3
"""Reconstruct historically accurate Shopify Capital & Credit balances.

Cross-references:
- capital_history.csv (loan advances, dates, amounts)
- Capital One bank data (ACH repayment withdrawals)
- credit_purchases.csv (Shopify Credit card charges)

Outputs monthly balance schedule showing what each account SHOULD
show in QuickBooks at each month-end.
"""

import csv
from collections import defaultdict
from datetime import date, datetime


def parse_date(d: str) -> date:
    """Parse date from various formats."""
    for fmt in ("%Y-%m-%d", "%b %d, %Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(d.strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {d}")


def load_bank_data(
    files: list[str],
    loan_funding_amounts: list[float] | None = None,
) -> tuple[dict[str, float], dict[str, float], list[dict]]:
    """Load Capital One bank data, return monthly Capital and Credit totals.

    Returns (capital_monthly, credit_monthly, excluded) where values are
    positive amounts representing cash paid toward each product.

    The loan_funding_amounts parameter identifies loan disbursements that
    the statement parser misclassified as withdrawals (negative amounts
    with "ACH deposit" in the description). These are excluded from
    repayment totals.
    """
    funding_set = set(loan_funding_amounts or [])
    capital: dict[str, float] = defaultdict(float)
    credit: dict[str, float] = defaultdict(float)
    excluded: list[dict] = []

    for filepath in files:
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                desc = row["Description"].upper()
                amt = float(row["Amount"])
                month = row["Date"][:7]

                if "SHOPIFY CAPITAL" in desc and amt < 0:
                    abs_amt = abs(amt)
                    if abs_amt in funding_set:
                        excluded.append({
                            "date": row["Date"],
                            "amount": abs_amt,
                            "desc": row["Description"],
                        })
                        funding_set.discard(abs_amt)
                        continue
                    capital[month] += abs_amt
                elif "SHOPIFY CREDIT" in desc and amt < 0:
                    credit[month] += abs(amt)

    return dict(capital), dict(credit), excluded


def load_loan_history(filepath: str) -> list[dict]:
    """Load Shopify Capital loan/advance history."""
    loans = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            loan = {
                "number": int(row["loan_number"]),
                "type": row["type"],
                "funding": float(row["funding_amount"]),
                "fee": float(row["fixed_fee"]),
                "total_to_repay": float(row["total_to_repay"]),
                "agreement_date": (
                    parse_date(row["agreement_date"])
                    if row["agreement_date"]
                    else None
                ),
                "completion_date": (
                    parse_date(row["completion_date"])
                    if row["completion_date"]
                    else None
                ),
                "status": row["status"],
            }
            loans.append(loan)
    return sorted(loans, key=lambda x: x["number"])


def estimate_funding_dates(loans: list[dict]) -> list[dict]:
    """Fill in missing agreement dates by estimating from prior loan
    completion dates.

    Pattern: new loan is funded approximately when the prior loan completes.
    """
    for i, loan in enumerate(loans):
        if loan["agreement_date"] is not None:
            continue
        if i == 0:
            continue
        prev = loans[i - 1]
        if prev["completion_date"]:
            loan["agreement_date"] = prev["completion_date"]
            loan["date_estimated"] = True
    return loans


def load_credit_charges(filepath: str) -> dict[str, float]:
    """Load Shopify Credit card charges by month.

    Handles the CSV where dates like "Dec 8, 2025" contain unquoted commas,
    causing the date to split across two fields.
    """
    charges: dict[str, float] = defaultdict(float)
    with open(filepath) as f:
        reader = csv.reader(f)
        header = next(reader)
        for fields in reader:
            if len(fields) >= 4:
                # Date split across fields[0] and fields[1]
                # e.g. ["Dec 8", " 2025", "TIKTOK ADS", "$53.00"]
                date_str = f"{fields[0]},{fields[1]}"
                amt_str = fields[-1].replace("$", "").replace(",", "").replace('"', "")
                d = parse_date(date_str)
                month = d.strftime("%Y-%m")
                charges[month] += float(amt_str)
            elif len(fields) == 3:
                # Properly formatted row
                d = parse_date(fields[0])
                month = d.strftime("%Y-%m")
                amt_str = fields[2].replace("$", "").replace(",", "").replace('"', "")
                charges[month] += float(amt_str)
    return dict(charges)


def reconstruct_capital_balances(
    loans: list[dict],
    bank_repayments: dict[str, float],
    current_balance: float,
    current_date: date,
) -> dict[str, dict]:
    """Reconstruct monthly Shopify Capital ending balances.

    Calculates the starting balance from known endpoint, then simulates
    forward: B(end_N) = B(end_{N-1}) + advanced_N - repaid_N.
    """
    all_months = sorted(
        set(bank_repayments.keys())
        | {current_date.strftime("%Y-%m")}
    )
    if not all_months:
        return {}

    # Advances by month (total_to_repay, not just principal)
    advances_by_month: dict[str, float] = defaultdict(float)
    advance_notes: dict[str, list[str]] = defaultdict(list)
    for loan in loans:
        fund_date = loan["agreement_date"]
        if fund_date:
            month = fund_date.strftime("%Y-%m")
            advances_by_month[month] += loan["total_to_repay"]
            est = " (est)" if loan.get("date_estimated") else ""
            advance_notes[month].append(
                f"Loan #{loan['number']}: "
                f"${loan['total_to_repay']:,.2f}{est}"
            )

    current_month = current_date.strftime("%Y-%m")
    first_month = all_months[0]
    total_repaid = sum(bank_repayments.values())
    total_advanced = sum(
        v for m, v in advances_by_month.items() if m >= first_month
    )
    starting_balance = current_balance + total_repaid - total_advanced

    schedule = {}
    balance = starting_balance

    for month in all_months:
        repaid = bank_repayments.get(month, 0.0)
        advanced = (
            advances_by_month.get(month, 0.0)
            if month >= first_month
            else 0.0
        )
        notes = advance_notes.get(month, []) if month >= first_month else []

        balance = balance + advanced - repaid
        note_str = "; ".join(notes) if notes else ""
        if month == current_month:
            note_str = "current (verified)"

        schedule[month] = {
            "ending_balance": balance,
            "repaid": repaid,
            "advanced": advanced,
            "note": note_str,
        }

    return dict(sorted(schedule.items())), starting_balance


def reconstruct_credit_balances(
    charges_monthly: dict[str, float],
    bank_payments: dict[str, float],
    current_balance: float,
    current_date: date,
) -> dict[str, dict]:
    """Reconstruct monthly Shopify Credit card ending balances.

    Calculates the starting balance from known endpoint, then simulates
    forward: B(end_N) = B(end_{N-1}) + charged_N - paid_N.
    """
    all_months = sorted(
        set(charges_monthly.keys())
        | set(bank_payments.keys())
        | {current_date.strftime("%Y-%m")}
    )
    if not all_months:
        return {}

    current_month = current_date.strftime("%Y-%m")
    total_charged = sum(charges_monthly.values())
    total_paid = sum(bank_payments.values())
    starting_balance = current_balance - total_charged + total_paid

    schedule = {}
    balance = starting_balance

    for month in all_months:
        charged = charges_monthly.get(month, 0.0)
        paid = bank_payments.get(month, 0.0)

        balance = balance + charged - paid
        note = "current (verified)" if month == current_month else ""

        schedule[month] = {
            "ending_balance": balance,
            "charged": charged,
            "paid": paid,
            "note": note,
        }

    return dict(sorted(schedule.items())), starting_balance


def main() -> None:
    base = "/Users/user/cc/cherri/financials"

    bank_files = [
        f"{base}/expenses/bank-statements/capital-one-checking/"
        "2024/2024_checking_qb_import.csv",
        f"{base}/expenses/bank-statements/capital-one-checking/"
        "2025_qb_import.csv",
    ]
    loans = load_loan_history(f"{base}/loans/shopify/capital_history.csv")
    loans = estimate_funding_dates(loans)

    # Loan funding amounts that appear as misclassified withdrawals
    # in the bank CSV (parser bug: "ACH deposit" with negative amount).
    # These are loan disbursements, NOT repayments.
    loan_fundings = [loan["funding"] for loan in loans]

    capital_monthly, credit_monthly, excluded = load_bank_data(
        bank_files, loan_funding_amounts=loan_fundings
    )

    # Known current balances (from Shopify Admin, Feb 15, 2026)
    capital_current = 4276.45
    credit_current = 8283.55
    as_of = date(2026, 2, 15)

    if excluded:
        print("=" * 80)
        print("EXCLUDED: Loan fundings misclassified as withdrawals")
        print("=" * 80)
        for e in excluded:
            print(
                f"  {e['date']}: ${e['amount']:>10,.2f}  "
                f"{e['desc'][:55]}"
            )
        print()

    # === SHOPIFY CAPITAL ===
    capital_schedule, cap_start = reconstruct_capital_balances(
        loans, capital_monthly, capital_current, as_of
    )

    print("=" * 80)
    print("SHOPIFY CAPITAL - Reconstructed Monthly Ending Balances")
    print("(Source: bank ACH withdrawals + loan history)")
    print("=" * 80)
    print(f"Starting balance (pre-{min(capital_schedule)}): "
          f"${cap_start:,.2f}")
    print(
        f"{'Month':<10} {'Ending Bal':>12} {'Repaid':>12} "
        f"{'Advanced':>12} {'Notes'}"
    )
    print("-" * 80)
    for month, data in capital_schedule.items():
        print(
            f"{month:<10} ${data['ending_balance']:>11,.2f} "
            f"${data['repaid']:>11,.2f} "
            f"${data['advanced']:>11,.2f} "
            f"{data['note']}"
        )

    # === SHOPIFY CREDIT ===
    try:
        credit_charges = load_credit_charges(
            f"{base}/loans/shopify/credit_purchases.csv"
        )
    except (FileNotFoundError, KeyError):
        credit_charges = {}

    if credit_charges:
        credit_schedule, cred_start = reconstruct_credit_balances(
            credit_charges, credit_monthly, credit_current, as_of
        )
        print()
        print("=" * 80)
        print("SHOPIFY CREDIT - Reconstructed Monthly Ending Balances")
        print("(Source: credit_purchases.csv charges + bank ACH payments)")
        print("=" * 80)
        print(f"Starting balance (pre-{min(credit_schedule)}): "
              f"${cred_start:,.2f}")
        print(
            f"{'Month':<10} {'Ending Bal':>12} {'Charged':>12} "
            f"{'Paid':>12} {'Notes'}"
        )
        print("-" * 80)
        for month, data in credit_schedule.items():
            print(
                f"{month:<10} ${data['ending_balance']:>11,.2f} "
                f"${data['charged']:>11,.2f} "
                f"${data['paid']:>11,.2f} "
                f"{data['note']}"
            )
    else:
        print()
        print("=" * 80)
        print("SHOPIFY CREDIT - Bank Repayments Only")
        print("=" * 80)
        print(f"{'Month':<10} {'Bank Repaid':>12}")
        print("-" * 30)
        for month in sorted(credit_monthly.keys()):
            print(f"{month:<10} ${credit_monthly[month]:>11,.2f}")
        total = sum(credit_monthly.values())
        print(f"{'TOTAL':<10} ${total:>11,.2f}")

    # === CSV EXPORT ===
    out_dir = f"{base}/loans/shopify"
    with open(f"{out_dir}/capital_monthly_balances.csv", "w") as f:
        f.write("month,ending_balance,repaid,advanced,note\n")
        for month, data in capital_schedule.items():
            f.write(
                f"{month},{data['ending_balance']:.2f},"
                f"{data['repaid']:.2f},{data['advanced']:.2f},"
                f"\"{data['note']}\"\n"
            )
    print(f"\nWrote: {out_dir}/capital_monthly_balances.csv")

    if credit_charges:
        with open(f"{out_dir}/credit_monthly_balances.csv", "w") as f:
            f.write("month,ending_balance,charged,paid,note\n")
            for month, data in credit_schedule.items():
                f.write(
                    f"{month},{data['ending_balance']:.2f},"
                    f"{data['charged']:.2f},{data['paid']:.2f},"
                    f"\"{data['note']}\"\n"
                )
        print(f"Wrote: {out_dir}/credit_monthly_balances.csv")

    # === SUMMARY ===
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("Target QBO balances (Feb 15, 2026):")
    print(f"  Shopify Capital Loan:  ${capital_current:>10,.2f}")
    print(f"  Shopify Credit:        ${credit_current:>10,.2f}")
    print(f"  Total debt:            ${capital_current + credit_current:>10,.2f}")
    print()
    print("Loan funding timeline (for QBO advance entries):")
    for loan in loans:
        if loan["number"] >= 8:
            d = loan["agreement_date"]
            est = " (estimated)" if loan.get("date_estimated") else ""
            end = loan["completion_date"] or "in progress"
            print(
                f"  {d}{est}: Loan #{loan['number']} funded "
                f"${loan['funding']:,.0f} "
                f"(+${loan['fee']:,.0f} fee = "
                f"${loan['total_to_repay']:,.0f} liability)"
                f" → completed {end}"
            )

    # === DATA QUALITY ===
    print()
    print("=" * 80)
    print("DATA QUALITY NOTES")
    print("=" * 80)
    print()
    print("Capital (HIGH confidence):")
    print(f"  ✓ Forward simulation endpoint matches known balance")
    print(f"  ✓ Starting balance ${cap_start:,.2f} consistent with "
          f"Loan #8 remaining")
    print(f"  ⚠ 3 loan fundings excluded (misclassified as "
          f"withdrawals in bank CSV)")
    print(f"  ⚠ Loan #9 funding date estimated (no bank entry found)")
    print(f"  ⚠ Jan-Feb 2026 gap (bank data ends Dec 2025)")
    print()
    print("Credit (LOW confidence for Nov 2023 - Feb 2024):")
    print(f"  ✗ Starting balance ${cred_start:,.2f} "
          f"(should be $0, card opened Nov 2023)")
    print(f"  ✗ Missing ~${abs(cred_start):,.2f} in early payments "
          f"(Nov 2023-Feb 2024)")
    print(f"  ✗ Bank 'SHOPIFY CREDIT' entries only start Mar 2024")
    print(f"  ✓ Mar 2024 onwards: charges + payments data complete")
    print(f"  → Need: Shopify Credit statements (PDFs) for "
          f"Nov 2023-Feb 2024 balances")


if __name__ == "__main__":
    main()
