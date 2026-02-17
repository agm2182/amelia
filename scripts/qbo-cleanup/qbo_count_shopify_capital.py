"""Count Shopify Capital and Credit related transactions in CSV."""
import csv

txns = []
for path in [
    "/Users/user/cc/cherri/financials/expenses/bank-statements/capital-one-checking/2024/2024_checking_qb_import.csv",
    "/Users/user/cc/cherri/financials/expenses/bank-statements/capital-one-checking/2025_qb_import.csv",
]:
    with open(path) as f:
        for row in csv.DictReader(f):
            txns.append({
                "date": row["Date"],
                "desc": row["Description"],
                "amount": float(row["Amount"]),
            })

# Categorize
capital = [t for t in txns if "SHOPIFY CAPITAL" in t["desc"].upper()]
credit = [t for t in txns if "SHOPIFY CREDIT" in t["desc"].upper()]
other = [t for t in txns if "SHOPIFY CAPITAL" not in t["desc"].upper()
         and "SHOPIFY CREDIT" not in t["desc"].upper()]

print(f"Total CSV transactions: {len(txns)}")
print(f"\nShopify Capital:  {len(capital)} txns, total ${sum(t['amount'] for t in capital):,.2f}")
print(f"  Advances (+):   {sum(1 for t in capital if t['amount'] > 0)} txns, ${sum(t['amount'] for t in capital if t['amount'] > 0):,.2f}")
print(f"  Repayments (-): {sum(1 for t in capital if t['amount'] < 0)} txns, ${sum(t['amount'] for t in capital if t['amount'] < 0):,.2f}")

print(f"\nShopify Credit:   {len(credit)} txns, total ${sum(t['amount'] for t in credit):,.2f}")
print(f"  Advances (+):   {sum(1 for t in credit if t['amount'] > 0)} txns, ${sum(t['amount'] for t in credit if t['amount'] > 0):,.2f}")
print(f"  Repayments (-): {sum(1 for t in credit if t['amount'] < 0)} txns, ${sum(t['amount'] for t in credit if t['amount'] < 0):,.2f}")

print(f"\nAll other:        {len(other)} txns, total ${sum(t['amount'] for t in other):,.2f}")
print(f"  Deposits (+):   {sum(1 for t in other if t['amount'] > 0)} txns, ${sum(t['amount'] for t in other if t['amount'] > 0):,.2f}")
print(f"  Payments (-):   {sum(1 for t in other if t['amount'] < 0)} txns, ${sum(t['amount'] for t in other if t['amount'] < 0):,.2f}")

# If Shopify Capital transactions were NOT imported to the checking register
# (they'd be in the Shopify Capital Loan account instead), what would the balance be?
without_capital = sum(t["amount"] for t in txns if "SHOPIFY CAPITAL" not in t["desc"].upper())
without_capital_credit = sum(t["amount"] for t in txns
                             if "SHOPIFY CAPITAL" not in t["desc"].upper()
                             and "SHOPIFY CREDIT" not in t["desc"].upper())

print(f"\n\nHYPOTHESIS: If Shopify Capital txns excluded from checking:")
print(f"  Net without Capital:         ${without_capital:,.2f}")
print(f"  Net without Capital+Credit:  ${without_capital_credit:,.2f}")
print(f"  QBO register shows:          $83,969.13")
print(f"  Difference (Capital only):   ${83969.13 - without_capital:,.2f}")
print(f"  Difference (both):           ${83969.13 - without_capital_credit:,.2f}")

# Count non-Capital/Credit transactions
non_shopify_loans = [t for t in txns
                     if "SHOPIFY CAPITAL" not in t["desc"].upper()
                     and "SHOPIFY CREDIT" not in t["desc"].upper()]
print(f"\n  Non-loan transactions: {len(non_shopify_loans)}")
print(f"  QBO register entries:  4094")
print(f"  If QBO has all non-loan + some loan: {4094 - len(non_shopify_loans)} loan entries in QBO")
