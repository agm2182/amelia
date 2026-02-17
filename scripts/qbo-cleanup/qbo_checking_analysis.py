"""Analyze Capital One Checking CSV data to compute expected balance."""
import csv
from collections import defaultdict

# Load 2024 data
txns_2024 = []
with open("/Users/user/cc/cherri/financials/expenses/bank-statements/capital-one-checking/2024/2024_checking_qb_import.csv") as f:
    for row in csv.DictReader(f):
        txns_2024.append({
            "date": row["Date"],
            "desc": row["Description"],
            "amount": float(row["Amount"]),
        })

# Load 2025 data
txns_2025 = []
with open("/Users/user/cc/cherri/financials/expenses/bank-statements/capital-one-checking/2025_qb_import.csv") as f:
    for row in csv.DictReader(f):
        txns_2025.append({
            "date": row["Date"],
            "desc": row["Description"],
            "amount": float(row["Amount"]),
        })

print("=" * 90)
print("CAPITAL ONE CHECKING x2420 - SOURCE DATA ANALYSIS")
print("=" * 90)

print(f"\n2024 transactions: {len(txns_2024)}")
print(f"2025 transactions: {len(txns_2025)}")
print(f"Total:             {len(txns_2024) + len(txns_2025)}")

# Compute totals
dep_2024 = sum(t["amount"] for t in txns_2024 if t["amount"] > 0)
wdl_2024 = sum(t["amount"] for t in txns_2024 if t["amount"] < 0)
dep_2025 = sum(t["amount"] for t in txns_2025 if t["amount"] > 0)
wdl_2025 = sum(t["amount"] for t in txns_2025 if t["amount"] < 0)

print(f"\n2024: Deposits=${dep_2024:,.2f}  Withdrawals=${wdl_2024:,.2f}  Net=${dep_2024 + wdl_2024:,.2f}")
print(f"2025: Deposits=${dep_2025:,.2f}  Withdrawals=${wdl_2025:,.2f}  Net=${dep_2025 + wdl_2025:,.2f}")

total_net = dep_2024 + wdl_2024 + dep_2025 + wdl_2025
print(f"\nTotal net (2024+2025): ${total_net:,.2f}")
print(f"QBO shows:            $83,969.13")
print(f"Bank balance:         $729.96")
print(f"QBO - Bank:           ${83969.13 - 729.96:,.2f}")

# Monthly breakdown
monthly = defaultdict(lambda: {"dep": 0.0, "wdl": 0.0, "count": 0})
for t in txns_2024 + txns_2025:
    month = t["date"][:7]  # YYYY-MM
    if t["amount"] > 0:
        monthly[month]["dep"] += t["amount"]
    else:
        monthly[month]["wdl"] += t["amount"]
    monthly[month]["count"] += 1

print(f"\n{'Month':8s} {'Deposits':>12s} {'Withdrawals':>12s} {'Net':>12s} {'Running':>12s} #Txns")
print("-" * 70)

running = 0.0
for month in sorted(monthly.keys()):
    m = monthly[month]
    net = m["dep"] + m["wdl"]
    running += net
    print(f"{month:8s} ${m['dep']:>11,.2f} ${m['wdl']:>11,.2f} ${net:>11,.2f} ${running:>11,.2f} {m['count']:5d}")

print("-" * 70)
print(f"{'TOTAL':8s} ${sum(m['dep'] for m in monthly.values()):>11,.2f} "
      f"${sum(m['wdl'] for m in monthly.values()):>11,.2f} "
      f"${total_net:>11,.2f} ${running:>11,.2f} "
      f"{sum(m['count'] for m in monthly.values()):5d}")

# If we assume the starting balance was $0 on 01/01/2024
# then the ending balance should be the running total
print(f"\nExpected ending balance (starting from $0): ${running:,.2f}")
print(f"Bank says ending balance:                   $729.96")
print(f"Implied opening balance (01/01/2024):       ${729.96 - running:,.2f}")

# Check for potential duplicate patterns
print("\n" + "=" * 90)
print("DUPLICATE ANALYSIS")
print("=" * 90)

# Group by date+amount to find potential dupes
from collections import Counter
keys_2024 = Counter()
keys_2025 = Counter()
for t in txns_2024:
    keys_2024[(t["date"], t["amount"])] += 1
for t in txns_2025:
    keys_2025[(t["date"], t["amount"])] += 1

# Cross-year check: any 2024 transactions also in 2025?
overlap_keys = set(keys_2024.keys()) & set(keys_2025.keys())
if overlap_keys:
    print(f"\nDate+Amount combos appearing in BOTH years: {len(overlap_keys)}")
    for k in sorted(overlap_keys)[:10]:
        print(f"  {k[0]} ${k[1]:,.2f} (2024:{keys_2024[k]}x, 2025:{keys_2025[k]}x)")

# Within-year duplicates
print(f"\n2024 same date+amount appearing 3+ times:")
for k, v in keys_2024.most_common(10):
    if v >= 3:
        print(f"  {k[0]} ${k[1]:,.2f} x{v}")

print(f"\n2025 same date+amount appearing 3+ times:")
for k, v in keys_2025.most_common(10):
    if v >= 3:
        print(f"  {k[0]} ${k[1]:,.2f} x{v}")
