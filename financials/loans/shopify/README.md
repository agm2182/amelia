# Shopify Capital & Credit Data

Data captured: January 27, 2026

> **This README covers Shopify debt products only.** For Shopify revenue data (payouts, orders, transaction fees), see [`financials/revenue/shopify/`](../../revenue/shopify/).

## Shopify Capital

### Current Loan (Loan #12)

| Field | Value |
|-------|-------|
| Loan Amount | $21,000 |
| Cost of Funds | $2,730 (13%) |
| Total to Repay | $23,730 |
| Repayment Rate | 17% of daily sales |
| Agreement Date | February 11, 2025 |
| Due Date | November 6, 2026 |
| Outstanding Balance | $4,544.10 |
| Amount Repaid | $19,185.90 (80%) |
| Status | In Progress |

### Funding History Summary

| # | Type | Funding | Fee | Total Repaid | Agreement | Completed |
|---|------|---------|-----|--------------|-----------|-----------|
| 12 | Loan | $21,000 | $2,730 | In Progress | Feb 2025 | - |
| 11 | Loan | $17,000 | $2,210 | $19,210 | Aug 2024 | May 2025 |
| 10 | Loan | $14,000 | $1,820 | $15,820 | - | Oct 2024 |
| 9 | Loan | $15,000 | $1,950 | $16,950 | - | Jun 2024 |
| 8 | Loan | $19,000 | $2,470 | $21,470 | - | Jan 2024 |
| 7 | Cash Advance | $16,000 | $2,080 | $18,080 | Dec 2022 | Jun 2023 |
| 6 | Cash Advance | $6,000 | $780 | $6,780 | - | Dec 2022 |
| 5 | Cash Advance | $9,735 | $1,265 | $11,000 | - | Nov 2022 |
| 4 | Cash Advance | $5,354 | $696 | $6,050 | - | Apr 2022 |
| 3 | Cash Advance | $7,000 | $910 | $7,910 | - | Feb 2022 |
| 2 | Cash Advance | $2,300 | $299 | $2,599 | - | Oct 2021 |
| 1 | Cash Advance | $1,500 | $195 | $1,695 | Jul 2021 | Aug 2021 |

### Historical Totals

- **Total Funded (completed):** $113,889
- **Total Fees Paid (completed):** $14,675
- **Total Repaid (completed):** $128,564

### Terms (Consistent Since 2021)

- **Fee Rate:** 13% of funding amount
- **Repayment Rate:** 17% of daily sales
- **Max Term:** 18 months from agreement date
- **Minimum Repayment Milestones:**
  - 30% of total at 6 months
  - 60% of total at 12 months
- **Issuer:** WebBank (USA)

### New Offer Available

- Up to $8,400 in additional funding
- Fixed fee: $924 (11%)
- Repayment: 12% of daily sales
- Repayment starts after current loan ends

## Shopify Credit

### Account Overview

| Field | Value |
|-------|-------|
| Card | Shopify Credit •••• 7253 |
| Credit Limit | **$12,000** |
| Current Balance | $8,399.98 |
| Pending | $46 |
| Available Credit | $3,500 |
| Issuer | Celtic Bank (via Stripe Payments Company) |

### Terms & Fees

| Term | Value |
|------|-------|
| Remaining Balance Fee | 11% |
| Daily Repayment Rate | 10% of sales |
| Monthly Late Fee | 2% |
| Repayment Period | 10 calendar months |
| Payment Account | Capital One National Association (2420) |

### December 2025 Statement

| Item | Amount |
|------|--------|
| Statement Total | $11,187.87 |
| Payments, credits, & fees | -$2,763.96 |
| Remaining Statement Balance | $8,399.98 |

### Fee History (Sample)

- Nov 2025 Fee: $226.48
- Jul 2025 Fee Discount: -$249.09
- Aug 2025 Fee Discount: -$54.04

### Cashback Rewards

- December 2025: $11.19
- Year to date 2025: $0.00 (resets annually)

### Credit Card Usage

The Shopify Credit card is used **exclusively for TikTok Ads**. This represents additional TikTok ad spend beyond what's tracked in the Chase credit card data.

### Statement History

Monthly statements available from November 2023 through December 2025 (26 months).

**2025 statements downloaded:** `credit_statements/` folder contains all 12 monthly PDFs for 2025.

Admin URL: https://admin.shopify.com/store/shop-cherri/credit/statements

## Related Financial Data

The following Shopify data is documented elsewhere but affects loan understanding:

### Payouts (Revenue Side)

Payouts are bank transfers after deducting Capital/Credit repayments and fees.

- **Data:** [`financials/revenue/shopify/all_payouts.csv`](../../revenue/shopify/all_payouts.csv)
- **Key columns:** `Advances` (Capital/Credit repayments), `Fees`, `Total`
- **Schema:** See [`DATA_DICTIONARY.md`](../../DATA_DICTIONARY.md#revenueshopifyall_payoutscsv)

### Transaction Fees (Expense Side)

Payment processing fees (~2.9% + $0.30 per transaction).

- **Data:** [`financials/revenue/shopify/all_payment_transactions.csv`](../../revenue/shopify/all_payment_transactions.csv)
- **Key columns:** `Fee`, `Net`
- **Schema:** See [`DATA_DICTIONARY.md`](../../DATA_DICTIONARY.md#revenueshopifyall_payment_transactionscsv)

### Shopify Balance (Inactive)

| Field | Value |
|-------|-------|
| Account | Main (6179) |
| Current Balance | $0.00 |
| Earnings Rate | 2.29% APY |
| Status | Inactive (last activity Jan 2023) |

## Data Files

- `capital_history.csv` - Complete loan/cash advance history
- `credit_statements/` - Monthly credit card statements (PDF)
  - 2025: `shopify_credit_statement_2025-01.pdf` through `shopify_credit_statement_2025-12.pdf`
- `browser-state.json` - Saved browser session for re-authentication (gitignored)

## What's Still Missing

The following data would complete the financial picture:

1. ~~**Payouts CSV**~~ - ✅ Received → `financials/revenue/shopify/all_payouts.csv`
2. ~~**Order Transactions CSV**~~ - ✅ Received → `financials/revenue/shopify/all_payment_transactions.csv`
3. ~~**Credit Statement PDFs**~~ - ✅ Downloaded → `credit_statements/` (12 months for 2025)
4. **2025 Transaction Fees Total** - Can now calculate from `all_payment_transactions.csv`

## Browser Session

To restore authenticated session:
```bash
agent-browser --headed --state financials/loans/shopify/browser-state.json open https://admin.shopify.com/store/shop-cherri/finance
```
