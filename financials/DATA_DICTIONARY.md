# Cherri Financial Data Dictionary

Schema definitions for all CSV files in the financials folder. Use this to understand data structure before analysis.

## Summary Files

### `summary/2025_monthly.csv`
Master monthly metrics combining all channels.

| Column | Type | Description |
|--------|------|-------------|
| month | date | YYYY-MM format |
| shopify_orders | integer | Number of Shopify orders |
| shopify_revenue | decimal | Gross revenue from Shopify |
| meta_ads_spend | decimal | Meta (Facebook/Instagram) ad spend |
| tiktok_ads_spend | decimal | TikTok ad spend |
| tiktok_shop_settlement | decimal | TikTok Shop settlement amount (net after fees) |

**Source:** Aggregated from Shopify Admin API, Meta Ads API, TikTok Ads API, TikTok Shop Finance Center
**Coverage:** 2025-01 to 2025-12

### `summary/2025_quarterly.csv`
Quarterly rollup of revenue, ad spend, and profitability.

| Column | Type | Description |
|--------|------|-------------|
| quarter | string | Q1, Q2, Q3, Q4 |
| shopify_revenue | decimal | Total Shopify revenue for quarter |
| tiktok_shop_settlement | decimal | Total TikTok Shop settlements |
| total_revenue | decimal | shopify_revenue + tiktok_shop_settlement |
| meta_ads_spend | decimal | Total Meta ad spend |
| tiktok_ads_spend | decimal | Total TikTok ad spend |
| total_ad_spend | decimal | meta_ads_spend + tiktok_ads_spend |
| shopify_fees | decimal | Shopify payment processing fees |
| gross_profit | decimal | total_revenue - shopify_fees |
| operating_margin | string | (gross_profit - total_ad_spend) / total_revenue |

**Source:** Derived from summary/2025_monthly.csv, revenue/shopify/all_payment_transactions.csv
**Coverage:** Q1-Q4 2025

### `summary/2025_pl_summary.md`
Comprehensive P&L analysis for 2025.

Includes:
- Revenue breakdown (Shopify, TikTok Shop)
- Cost of sales (payment processing fees)
- Operating expenses (advertising, inventory, software)
- Financing costs (OnRamp, Clearco, Shopify Capital/Credit)
- Key metrics (AOV, ROAS, ad spend ratio)
- Data gaps and caveats

**Source:** Aggregated from all financials data sources
**Coverage:** Full year 2025

## Revenue Files

### `revenue/shopify/2025_orders.csv`
All Shopify orders for 2025.

| Column | Type | Description |
|--------|------|-------------|
| order_name | string | Order number (e.g., #14038) |
| created_at | datetime | ISO 8601 timestamp |
| financial_status | string | PAID, REFUNDED, etc. |
| fulfillment_status | string | FULFILLED, UNFULFILLED, etc. |
| total | decimal | Total order value |
| subtotal | decimal | Subtotal before shipping/tax |
| shipping | decimal | Shipping charges |
| tax | decimal | Tax amount |
| refunded | decimal | Refunded amount |
| discounts | decimal | Discount amount |

**Source:** Shopify Admin GraphQL API
**Coverage:** 2025-01-01 to 2025-12-31
**Records:** 2,993 orders

### `revenue/shopify/2025_monthly.csv`
Monthly Shopify revenue aggregation.

| Column | Type | Description |
|--------|------|-------------|
| month | date | YYYY-MM format |
| orders | integer | Order count |
| gross_revenue | decimal | Total order value |

**Source:** Aggregated from 2025_orders.csv
**Coverage:** 2025-01 to 2025-12

### `revenue/shopify/all_payment_transactions.csv`
Complete Shopify payment transaction history with fees.

| Column | Type | Description |
|--------|------|-------------|
| Transaction Date | datetime | Transaction timestamp |
| Type | string | charge, refund, payout, etc. |
| Order | string | Order number (e.g., #17779) |
| Card Brand | string | visa, mastercard, amex, etc. |
| Card Source | string | online, pos, etc. |
| Payout Status | string | pending, in_transit, paid |
| Payout Date | date | When funds were/will be paid out |
| Payout ID | string | Payout batch identifier |
| Available On | date | When funds become available |
| Amount | decimal | Gross transaction amount |
| Fee | decimal | Payment processing fee (~2.9% + $0.30) |
| Net | decimal | Amount - Fee |
| Checkout | string | Checkout ID |
| Payment Method Name | string | card, shopify_installments, etc. |
| Presentment Amount | decimal | Amount in presentment currency |
| Presentment Currency | string | Currency code |
| Currency | string | Settlement currency (USD) |

**Source:** Shopify Admin → Settings → Payments → View payouts → Export
**Coverage:** July 2019 to January 2026
**Records:** 10,961 transactions

### `revenue/shopify/all_payouts.csv`
Complete Shopify payout history (bank transfers).

| Column | Type | Description |
|--------|------|-------------|
| Payout Date | date | Date of bank transfer |
| Status | string | paid, in_transit, pending |
| Charges | decimal | Total charges in payout |
| Refunds | decimal | Total refunds (negative) |
| Adjustments | decimal | Manual adjustments |
| Marketplace Sales Tax | decimal | Sales tax collected |
| Advances | decimal | Capital/Credit repayments (negative) |
| Reserved Funds | decimal | Held reserves |
| Fees | decimal | Processing fees (negative) |
| Retried Amount | decimal | Failed payout retries |
| Total | decimal | Net payout amount |
| Currency | string | USD |
| Bank Reference | string | Bank transaction reference |

**Source:** Shopify Admin → Settings → Payments → View payouts → Export
**Coverage:** July 2019 to January 2026
**Records:** 2,099 payouts

### `revenue/tiktok-shop/2025_orders.csv`
All TikTok Shop order details for 2025.

| Column | Type | Description |
|--------|------|-------------|
| Statement date | date | Settlement statement date (YYYY/MM/DD) |
| Statement ID | string | TikTok statement identifier |
| Payment ID | string | Payment transaction ID |
| Status | string | Paid, Pending, etc. |
| Currency | string | USD |
| Type | string | Order, Adjustment, etc. |
| Order/adjustment ID | string | TikTok order ID |
| SKU ID | string | Product SKU identifier |
| Quantity | integer | Items ordered |
| Product name | string | Full product name |
| SKU name | string | Size/color variant |
| Order created date | date | When customer placed order |
| Order shipment date | date | When order shipped |
| Order delivery date | date | When order delivered |
| Total settlement amount | decimal | Net amount after fees |
| Net sales | decimal | Sales after discounts |
| Gross sales | decimal | Original sale price |
| Gross sales refund | decimal | Refund amount (negative) |
| ... | ... | Additional fee breakdown columns |

**Source:** TikTok Shop Finance Center exports
**Coverage:** 2025-01-01 to 2025-12-31
**Records:** ~1,714 line items

### `revenue/tiktok-shop/2025_monthly.csv`
Monthly TikTok Shop revenue (estimated from quarterly data).

| Column | Type | Description |
|--------|------|-------------|
| month | date | YYYY-MM format |
| settlement_amount | decimal | Net settlement after all fees |
| gross_sales | decimal | Original sale prices |
| refunds | decimal | Refund amounts (negative) |
| fees | decimal | Platform fees (negative) |
| affiliate_commission | decimal | Affiliate payouts (negative) |
| sales_tax | decimal | Sales tax collected (negative) |

**Source:** Derived from tiktok_2025_summary.csv quarterly data
**Coverage:** 2025-01 to 2025-12
**Note:** Monthly values are quarterly totals divided by 3 (approximation)

### `revenue/tiktok-shop/2025_quarterly.csv`
Quarterly TikTok Shop summary with fee breakdowns.

| Column | Type | Description |
|--------|------|-------------|
| Quarter | string | Q1_2025, Q2_2025, etc. |
| Total settlement amount | decimal | Net amount paid out |
| Net sales | decimal | Sales after discounts/refunds |
| Gross sales | decimal | Original sale prices |
| Gross sales refund | decimal | Refund amounts |
| Transaction fee | decimal | Payment processing fees |
| Referral fee | decimal | TikTok platform commission |
| Affiliate Commission | decimal | Creator/affiliate payouts |
| TikTok Shop shipping fee | decimal | Platform shipping charges |
| Customer-paid shipping fee | decimal | Customer shipping payments |
| Sales tax payment | decimal | Tax remittance |

**Source:** TikTok Shop Finance Center
**Coverage:** Q1-Q4 2025

### `revenue/tiktok-shop/2025_statements.csv`
TikTok Shop settlement statements.

| Column | Type | Description |
|--------|------|-------------|
| Statement date | date | Statement date (YYYY/MM/DD) |
| Statement ID | string | Unique statement identifier |
| Payment ID | string | Payment transaction ID |
| Status | string | Paid status |
| Total settlement amount | decimal | Total payout |
| Net sales | decimal | Sales minus returns |
| Shipping | decimal | Shipping fees |
| Fees | decimal | Platform fees |
| Adjustments | decimal | Manual adjustments |
| Reserve Amount | decimal | Held reserves |
| Payable amount | decimal | Amount transferred |

**Source:** TikTok Shop Finance Center
**Coverage:** 2025-01 to 2025-12

## Advertising Files

### `advertising/meta/2025_monthly.csv`
Monthly Meta (Facebook/Instagram) advertising metrics.

| Column | Type | Description |
|--------|------|-------------|
| month | date | YYYY-MM format |
| spend | decimal | Total ad spend |
| impressions | integer | Ad impressions |
| clicks | integer | Ad clicks |
| cpc | decimal | Cost per click |
| cpm | decimal | Cost per 1000 impressions |
| reach | integer | Unique users reached |

**Source:** Meta Ads API
**Coverage:** 2025-01 to 2025-12
**Note:** Nov-Dec 2025 show $0 spend (ads paused)

### `advertising/tiktok/2025_monthly.csv`
Monthly TikTok advertising spend.

| Column | Type | Description |
|--------|------|-------------|
| month | date | YYYY-MM format |
| spend | decimal | Total ad spend |
| impressions | integer | Ad impressions (when available) |
| clicks | integer | Ad clicks (when available) |
| source | string | Data source (chase_card, tiktok_ads_api, combined) |
| notes | string | Additional context |

**Source:** Chase credit card statement + TikTok Ads API
**Coverage:** 2025-01 to 2025-12
**Note:** Chase card captures total spend; API has engagement metrics for some months

## Expense Files

### `expenses/2025_chase_categorized.csv`
All Chase credit card transactions with expense categories.

| Column | Type | Description |
|--------|------|-------------|
| transaction_date | date | Transaction date (YYYY-MM-DD) |
| post_date | date | Post date (YYYY-MM-DD) |
| description | string | Transaction description |
| amount | decimal | Amount (negative = expense) |
| category | string | Top-level category |
| subcategory | string | Detailed category |

**Categories:**
- `advertising` - tiktok, meta, tiktok_refund
- `inventory` - manufacturer (Resource Fashion)
- `software` - email_marketing (Mailchimp)
- `fees` - interest, late_fee, credit
- `payment` - credit_card_payment
- `other` - dining, misc

**Source:** Chase credit card CSV export
**Coverage:** 2025-01-02 to 2025-12-12
**Records:** 175 transactions

### `expenses/2025_expense_summary.csv`
Monthly expense totals by category.

| Column | Type | Description |
|--------|------|-------------|
| month | date | YYYY-MM format |
| advertising_tiktok | decimal | TikTok ad spend |
| advertising_meta | decimal | Meta ad spend (from Chase) |
| inventory | decimal | Resource Fashion purchases |
| software | decimal | Mailchimp, etc. |
| fees_interest | decimal | Credit card interest |
| fees_late | decimal | Late payment fees |
| fees_other | decimal | Credits, adjustments |
| other | decimal | Dining, misc |
| total_expenses | decimal | Sum of all expenses |

**Source:** Aggregated from 2025_chase_categorized.csv
**Coverage:** 2025-01 to 2025-12
**Note:** Excludes payments (credit card payments are not expenses)

## Bank Statements

### `expenses/bank-statements/capital-one-checking/`
Capital One business checking account x2420 statements and QB imports.

**2025 files:** Business_Basic_Checking...2420_{MONTH}_2025.pdf (12 PDFs), 2025_qb_import.csv + 3 parts
**2024 files (in `2024/`):** Business_Basic_Checking...2420_{MONTH}_2024.pdf (13 PDFs), quarterly QB imports (4 files) + full import
**Coverage:** Jan 2024 - Dec 2025
**QB import:** 2,614 transactions (2025), 2,118 transactions (2024)

### `expenses/bank-statements/capital-one-credit/`
Capital One credit card x6284 statements and QB imports.

**2025 files:** Statement_{MMYYYY}_6284.pdf (13 PDFs), 2025_qb_import.csv
**2024 files (in `2024/`):** Statement_{MMYYYY}_6284.pdf (14 PDFs), 2024_credit_qb_import.csv
**Coverage:** Jan 2024 - Jan 2026
**QB import:** 45 transactions (2025), 39 transactions (2024)

### `expenses/bank-statements/chase-credit/`
Chase credit card x0982 (G. Scaringe) CSV exports.

**2024 (in `2024/`):** Chase0982_Activity CSV + 2024_chase_qb_import.csv
**2025 (in `2025/`):** 2025 Chase Credit Card Transactions.CSV (not imported - already in QB via bank feed)
**Coverage:** Feb 2024 - Dec 2025
**QB import:** 31 transactions (2024 only; 2025 synced via bank feed, 174 transactions)

### `expenses/bank-statements/shopify-credit/`
Shopify Credit card x2450 transaction exports.

**2024 (in `2024/`):** Shopifycredit-transactions CSV + 2024_shopify_credit_qb_import.csv
**Coverage:** Jan - Dec 2024
**QB import:** 115 transactions

## Archive Files

### `archive/originals/`
Original TikTok Shop XLSX exports before CSV conversion.

### `archive/tiktok-shop-raw/`
Duplicate/overlapping TikTok Shop quarterly exports:
- Q2a (apr01-jun27) - superseded by Q2b
- Q3a (jun30-sep26) - non-standard start date, superseded by Q3b
- Q4b (oct02-dec27) - covered by Q4a + Q4c

## Loans & Financing Files

### `loans/all_financing_history.csv`
Combined financing activity from all sources.

| Column | Type | Description |
|--------|------|-------------|
| date | date | Payment/funding date (YYYY-MM-DD) |
| source | string | shopify_capital, clearco, onramp |
| type | string | loan, cash_advance, invoice_funding, revenue_advance |
| amount | decimal | Total payment amount |
| principal | decimal | Principal portion (if applicable) |
| fee | decimal | Fee/interest portion (if applicable) |
| loan_id | string | Source-specific identifier |
| notes | string | Vendor name, status, or context |

**Source:** Combined from shopify/capital_history.csv, clearco/payment_history.csv, onramp/2025_statements.csv
**Coverage:** July 2021 to November 2025
**Records:** 146 entries (12 Shopify, 119 Clearco, 15 OnRamp)

### `loans/shopify/capital_history.csv`
Complete Shopify Capital loan and cash advance history.

| Column | Type | Description |
|--------|------|-------------|
| loan_number | integer | Sequential loan number (1-12) |
| type | string | Loan or Cash Advance |
| funding_amount | decimal | Amount funded |
| fixed_fee | decimal | Fixed fee (13% of funding) |
| fee_rate | decimal | Fee rate (0.13) |
| total_to_repay | decimal | funding_amount + fixed_fee |
| repayment_rate | decimal | Daily sales deduction rate (0.17) |
| agreement_date | date | Loan agreement date (YYYY-MM-DD) |
| completion_date | date | When fully repaid (YYYY-MM-DD) |
| status | string | In Progress or Completed |
| shopify_id | integer | Shopify internal loan ID |

**Source:** Shopify Admin → Finance → Capital
**Coverage:** July 2021 to present
**Records:** 12 loans/advances

### `loans/shopify/credit_purchases.csv`
Shopify Credit card purchase history (advertising spend).

| Column | Type | Description |
|--------|------|-------------|
| date | string | Transaction date (Mon DD, YYYY format) |
| description | string | Merchant name (TIKTOK ADS, FACEBK *, KLAVIYO, etc.) |
| amount | decimal | Purchase amount |

**Source:** Shopify Admin → Finance → Credit → Purchases tab (scraped via agent-browser)
**Coverage:** November 2023 to December 2025
**Records:** 168 transactions

**2025 Summary:**
- TikTok Ads: $2,431.87
- Meta Ads: $22,646.59
- Total: $25,078.46

**Note:** This captures ad spend charged to Shopify Credit, separate from Chase card. Meta Ads used Shopify Credit heavily in 2025 ($22.6K), while TikTok Ads was primarily on Chase.

### `loans/clearco/payment_history.csv`
Clear.co invoice funding weekly payments.

| Column | Type | Description |
|--------|------|-------------|
| date | date | Payment date (YYYY-MM-DD) |
| id | string | Invoice ID (e.g., 91C05, 1B39B) |
| type | string | Invoice Funding |
| vendor | string | Vendor being paid (MadeCo LLC, ITB Fulfillment, etc.) |
| amount | decimal | Weekly payment amount |
| status | string | Success |

**Source:** Clear.co Portal → Payment History
**Coverage:** July 2024 to September 2025
**Records:** 119 payments

### `loans/onramp/2025_statements.csv`
OnRamp Funds revenue-based financing statements.

| Column | Type | Description |
|--------|------|-------------|
| statement_date | date | Statement period end date (YYYY-MM-DD) |
| payment_date | date | ACH payment date (YYYY-MM-DD) |
| eligible_sales | decimal | Sales subject to repayment |
| principal_rate | decimal | Principal deduction rate (0.17) |
| principal_amount | decimal | Principal repaid |
| fee_rate | decimal | Fee rate (0.0289) |
| fee_amount | decimal | Fee paid |
| total_paid | decimal | principal_amount + fee_amount |

**Source:** OnRamp Funds Portal → Statements
**Coverage:** August 2025 to November 2025
**Records:** 15 weekly statements

## Data Quality Notes

1. **TikTok Shop monthly estimates:** Monthly values are quarterly totals ÷ 3. Actual monthly variance not captured.

2. **TikTok Ads data gaps:** API only has data for Apr, Oct, Nov. Chase card captures all charges but lacks impressions/clicks.

3. **Meta Ads Nov-Dec 2025:** Shows $0 spend - ads were paused, not missing data.

4. **Chase card timing:** Transaction dates may differ from when ads actually ran.

5. **Shopify orders with $0 total:** Some orders show $0 - likely comped/test orders.
