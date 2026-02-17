"""Analyze why QBO register has fewer entries but higher balance than CSV."""
import csv
from collections import defaultdict

# Load all CSV data
txns = []
for year, path in [
    (2024, "/Users/user/cc/cherri/financials/expenses/bank-statements/capital-one-checking/2024/2024_checking_qb_import.csv"),
    (2025, "/Users/user/cc/cherri/financials/expenses/bank-statements/capital-one-checking/2025_qb_import.csv"),
]:
    with open(path) as f:
        for row in csv.DictReader(f):
            txns.append({
                "date": row["Date"],
                "desc": row["Description"],
                "amount": float(row["Amount"]),
                "year": year,
            })

print("=" * 90)
print("CAPITAL ONE CHECKING - GAP ANALYSIS")
print("=" * 90)

total_csv = len(txns)
total_qbo = 4094  # from register (82 pages)
qbo_register_balance = 83969.13
csv_net = sum(t["amount"] for t in txns)

print(f"\nCSV transactions:    {total_csv}")
print(f"QBO register entries: {total_qbo}")
print(f"Missing entries:      {total_csv - total_qbo}")

print(f"\nCSV net:             ${csv_net:,.2f}")
print(f"QBO register:        ${qbo_register_balance:,.2f}")
print(f"Excess in QBO:       ${qbo_register_balance - csv_net:,.2f}")

missing_count = total_csv - total_qbo  # 638
excess = qbo_register_balance - csv_net  # ~$46,043

print(f"\nIf {missing_count} entries are missing from QBO:")
print(f"  Each missing entry averages: ${excess / missing_count:,.2f}")
print(f"  (positive = missing withdrawals that reduce balance)")

# Separate deposits and withdrawals
deposits = [t for t in txns if t["amount"] > 0]
withdrawals = [t for t in txns if t["amount"] < 0]

print(f"\nCSV breakdown:")
print(f"  Deposits:     {len(deposits)} totaling ${sum(t['amount'] for t in deposits):,.2f}")
print(f"  Withdrawals:  {len(withdrawals)} totaling ${sum(t['amount'] for t in withdrawals):,.2f}")

# If all missing entries are withdrawals:
print(f"\nIf all {missing_count} missing are withdrawals:")
print(f"  CSV total withdrawals: ${sum(t['amount'] for t in withdrawals):,.2f}")
print(f"  Needed missing total:  ${-excess:,.2f}")
print(f"  Remaining in QBO:      ${sum(t['amount'] for t in withdrawals) + excess:,.2f}")

# Monthly analysis of deposits vs withdrawals
print(f"\n{'Month':8s} {'#Dep':>5s} {'#Wdl':>5s} {'Dep$':>12s} {'Wdl$':>12s} {'Net$':>12s}")
print("-" * 60)

monthly = defaultdict(lambda: {"ndep": 0, "nwdl": 0, "dep": 0.0, "wdl": 0.0})
for t in txns:
    month = t["date"][:7]
    if t["amount"] > 0:
        monthly[month]["ndep"] += 1
        monthly[month]["dep"] += t["amount"]
    else:
        monthly[month]["nwdl"] += 1
        monthly[month]["wdl"] += t["amount"]

for month in sorted(monthly.keys()):
    m = monthly[month]
    print(f"{month:8s} {m['ndep']:5d} {m['nwdl']:5d} "
          f"${m['dep']:>11,.2f} ${m['wdl']:>11,.2f} "
          f"${m['dep'] + m['wdl']:>11,.2f}")

# Hypothesis: Maybe the QBO balance already accounts for some 2026 activity
# that isn't in the CSV. The page 1 data showed 2026 net = ~$335.
# So QBO balance at end of 2025 should be ~$83,969 - $335 = ~$83,634
print(f"\n\nEstimated QBO balance at end of 2025: ~$83,634")
print(f"CSV net at end of 2025:               ${csv_net:,.2f}")
print(f"Difference:                           ~${83634 - csv_net:,.2f}")

# Let's also check: what if the issue is that SOME but not all
# withdrawals from bank feed got posted but CSV withdrawals did not?
# Or vice versa?

# Check for Shopify Capital repayments, loan advances, and transfers
# that might be in QBO but not in the CSV
print("\n\n" + "=" * 90)
print("LARGE TRANSACTIONS ANALYSIS")
print("=" * 90)
print("\nLargest deposits:")
for t in sorted(deposits, key=lambda x: -x["amount"])[:15]:
    print(f"  {t['date']} ${t['amount']:>10,.2f} {t['desc'][:70]}")

print("\nLargest withdrawals:")
for t in sorted(withdrawals, key=lambda x: x["amount"])[:15]:
    print(f"  {t['date']} ${t['amount']:>10,.2f} {t['desc'][:70]}")

# Check if Shopify Capital advances are in the CSV
print("\n\nShopify Capital related transactions:")
for t in txns:
    desc_lower = t["desc"].lower()
    if "shopify" in desc_lower and ("capital" in desc_lower or "lending" in desc_lower):
        print(f"  {t['date']} ${t['amount']:>10,.2f} {t['desc'][:70]}")

# Check for transfers
print("\nTransfer-like transactions (large single amounts):")
for t in txns:
    if abs(t["amount"]) > 2000:
        print(f"  {t['date']} ${t['amount']:>10,.2f} {t['desc'][:70]}")
