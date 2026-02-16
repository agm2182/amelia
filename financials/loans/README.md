# Cherri Loans & Credit

Overview of all loan and credit products used by Cherri.

## Quick Scan (Feb 2026)

### Current Debt Snapshot

| Source | Product | Balance | Monthly Cost | Due Date | Status |
|--------|---------|---------|--------------|----------|--------|
| Shopify Capital | Loan #12 | **$4,276** | ~$400/mo* | Nov 2026 | Active |
| Shopify Credit | Credit Card | **$8,284** | ~$300/mo* | Rolling | Active (over limit) |
| OnRamp Funds | Revenue Advance | $0 | - | - | Paid Off |
| Clear.co | Invoice Funding | $0 | - | - | Inactive |
| **TOTAL** | | **$12,560** | | | |

*Estimated - actual varies with sales volume (repayment = % of daily sales)

### Monthly Payment Obligations

| Product | Mechanism | Rate | Bank Account |
|---------|-----------|------|--------------|
| Shopify Capital | Auto-deduct from sales | 17% of daily sales | Via Shopify payouts |
| Shopify Credit | Auto-deduct from sales | 10% of daily sales | Via Shopify payouts |

### Quick Links

| Data | Location |
|------|----------|
| All financing payments (combined) | [`all_financing_history.csv`](all_financing_history.csv) |
| Shopify Capital loan details | [`shopify/README.md`](shopify/README.md) |
| Shopify Credit card details | [`shopify/README.md`](shopify/README.md) |
| OnRamp repayment history | [`onramp/2025_statements.csv`](onramp/2025_statements.csv) |
| Clearco payment history | [`clearco/payment_history.csv`](clearco/payment_history.csv) |

## Loan Sources

| Source | Type | Status | Balance | Subfolder |
|--------|------|--------|---------|-----------|
| Shopify Capital | Revenue-based loans | Active - $4,276 remaining | Loan #12: $21K | `shopify/` |
| Shopify Credit | Credit card | Active - $8,284 balance (over limit) | $6.2K limit | `shopify/` |
| OnRamp Funds | Revenue-based | Fully repaid Nov 2025 | $0 | `onramp/` |
| Clear.co | Invoice funding | Inactive | $6K capacity available | `clearco/` |

## Summary

### Active Debt
- **Shopify Capital Loan #12:** $4,276.45 remaining (of $23,730 total, 81% repaid)
- **Shopify Credit Card:** $8,283.55 balance ($6,200 limit — over limit, $0 available)

### Completed/Inactive
- **OnRamp Funds:** $6,500 advance fully repaid ($7,605 total with fees)
- **Clear.co:** Invoice funding used 2024-2025, $18K+ repaid, now inactive

## Folder Structure

- `shopify/` - Shopify Capital loans & Credit card (active)
- `onramp/` - OnRamp Funds revenue-based financing (completed)
- `clearco/` - Clear.co invoice funding (inactive)

See each subfolder's README for detailed documentation.
