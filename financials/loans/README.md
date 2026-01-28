# Cherri Loans & Credit

Overview of all loan and credit products used by Cherri.

## Quick Scan (Jan 2026)

### Current Debt Snapshot

| Source | Product | Balance | Monthly Cost | Due Date | Status |
|--------|---------|---------|--------------|----------|--------|
| Shopify Capital | Loan #12 | **$4,544** | ~$1,500/mo* | Nov 2026 | Active |
| Shopify Credit | Credit Card | **$8,400** | ~$800/mo* | Rolling | Active |
| OnRamp Funds | Revenue Advance | $0 | - | - | Paid Off |
| Clear.co | Invoice Funding | $0 | - | - | Inactive |
| **TOTAL** | | **$12,944** | | | |

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
| Shopify Capital | Revenue-based loans | Active - $4,544 remaining | Loan #12: $21K | `shopify/` |
| Shopify Credit | Credit card | Active - $8,400 balance | $12K limit | `shopify/` |
| OnRamp Funds | Revenue-based | Fully repaid Nov 2025 | $0 | `onramp/` |
| Clear.co | Invoice funding | Inactive | $6K capacity available | `clearco/` |

## Summary

### Active Debt
- **Shopify Capital Loan #12:** $4,544.10 remaining (of $23,730 total)
- **Shopify Credit Card:** $8,399.98 balance

### Completed/Inactive
- **OnRamp Funds:** $6,500 advance fully repaid ($7,605 total with fees)
- **Clear.co:** Invoice funding used 2024-2025, $18K+ repaid, now inactive

## Folder Structure

- `shopify/` - Shopify Capital loans & Credit card (active)
- `onramp/` - OnRamp Funds revenue-based financing (completed)
- `clearco/` - Clear.co invoice funding (inactive)

See each subfolder's README for detailed documentation.
