# Cherri Financial Data

Financial records for Cherri, organized for quick analysis.

## 2025 Summary

| Metric | Value |
|--------|-------|
| **Shopify Revenue** | $166,637.68 |
| **TikTok Shop Settlement** | $38,568.21 |
| **Total E-commerce Revenue** | $205,205.89 |
| | |
| **Meta Ads Spend** | $77,362.49 |
| **TikTok Ads Spend** | $7,652.84 |
| **Total Ad Spend** | $85,015.33 |
| | |
| **Shopify Orders** | 2,993 |

*TikTok Ads includes $5,220.97 (Chase) + $2,431.87 (Shopify Credit)*

## Folder Structure

```
financials/
├── summary/                        # Quick-access aggregated data
│   ├── 2025_monthly.csv           # Master monthly metrics (all channels)
│   ├── 2025_quarterly.csv         # Quarterly rollup
│   └── 2025_pl_summary.md         # Full P&L analysis
│
├── revenue/                        # Revenue by channel
│   ├── shopify/
│   │   ├── 2025_orders.csv        # All 2,993 orders
│   │   ├── 2025_monthly.csv       # Monthly aggregation
│   │   ├── all_payouts.csv        # Bank transfer history (2019-2026)
│   │   └── all_payment_transactions.csv  # Transaction-level with fees
│   └── tiktok-shop/
│       ├── 2025_orders.csv        # Deduplicated order details
│       ├── 2025_monthly.csv       # Monthly aggregation (estimated)
│       ├── 2025_quarterly.csv     # Quarterly with fee breakdowns
│       └── 2025_statements.csv    # Settlement statements
│
├── advertising/                    # Ad spend by platform
│   ├── meta/
│   │   └── 2025_monthly.csv       # Meta Ads metrics
│   └── tiktok/
│       └── 2025_monthly.csv       # TikTok Ads spend
│
├── expenses/                       # Operating expenses
│   ├── 2025_chase_categorized.csv # Categorized Chase transactions
│   ├── 2025_expense_summary.csv   # Monthly expense totals by category
│   └── bank-statements/           # Original PDFs (25 files)
│       ├── capital-one-checking/
│       └── capital-one-credit/
│
├── loans/                          # Financing & credit products
│   ├── all_financing_history.csv  # Combined history (all sources)
│   ├── README.md                  # Loan status overview
│   ├── shopify/
│   │   ├── capital_history.csv    # 12 loans/advances
│   │   ├── credit_purchases.csv   # Credit card transactions
│   │   ├── credit_statements/     # Monthly PDFs (12 files)
│   │   └── README.md
│   ├── clearco/
│   │   ├── payment_history.csv    # Invoice funding payments
│   │   └── README.md
│   └── onramp/
│       ├── 2025_statements.csv    # Revenue advance statements
│       └── README.md
│
├── archive/                        # Raw exports (69 files)
│   ├── tiktok-shop-raw/           # Superseded quarterly exports
│   └── originals/                  # Original XLSX files
│
├── DATA_DICTIONARY.md             # Schema definitions for all CSVs
└── README.md                      # This file
```

## Quick Reference: Which File to Use

| Question | Use This File |
|----------|---------------|
| **Full P&L analysis** | `summary/2025_pl_summary.md` |
| Monthly revenue summary | `summary/2025_monthly.csv` |
| Quarterly P&L | `summary/2025_quarterly.csv` |
| Shopify order details | `revenue/shopify/2025_orders.csv` |
| Shopify payouts (bank transfers) | `revenue/shopify/all_payouts.csv` |
| Shopify transaction fees | `revenue/shopify/all_payment_transactions.csv` |
| TikTok Shop revenue | `revenue/tiktok-shop/2025_quarterly.csv` |
| Meta ad performance | `advertising/meta/2025_monthly.csv` |
| TikTok ad spend | `advertising/tiktok/2025_monthly.csv` |
| Operating expenses | `expenses/2025_expense_summary.csv` |
| Expense details | `expenses/2025_chase_categorized.csv` |
| All loan/financing history | `loans/all_financing_history.csv` |
| Loan status overview | `loans/README.md` |
| Shopify Credit purchases | `loans/shopify/credit_purchases.csv` |
| Schema definitions | `DATA_DICTIONARY.md` |

## Data Sources

### Shopify (via Admin GraphQL API)
- Full order export with financial/fulfillment status
- **Coverage:** Jan 1 - Dec 31, 2025

### Meta Ads (via Meta Ads API)
- Monthly performance metrics: spend, impressions, clicks, reach
- **Coverage:** Jan - Oct 2025 (ads paused Nov-Dec)

### TikTok Shop (manual export)
- Quarterly exports from TikTok Shop Seller Center
- Includes fees, orders, payments, settlements
- **Coverage:** Jan 1 - Dec 31, 2025

### TikTok Ads
- Combined from Chase card transactions and TikTok Ads API
- API has engagement metrics for Apr, Oct, Nov only
- **Coverage:** Jan - Dec 2025

### Chase Credit Card
- Categorized transaction-level data
- Categories: advertising, inventory, software, fees
- **Coverage:** Jan - Dec 2025

## Expense Categories

| Category | Vendor/Description |
|----------|-------------------|
| `advertising/tiktok` | TikTok Ads charges |
| `advertising/meta` | Facebook/Instagram ads |
| `inventory` | Resource Fashion (manufacturer) |
| `software` | Mailchimp (email marketing) |
| `fees/interest` | Credit card interest charges |
| `fees/late` | Late payment fees |

## Known Data Limitations

1. **TikTok Shop monthly values** are quarterly totals ÷ 3 (approximation)
2. **TikTok Ads API gaps** - Chase captures spend, API has metrics for limited months
3. **Meta Ads Nov-Dec** shows $0 - ads were paused, not missing data
4. **Shopify order breakdowns missing** - subtotal/shipping/tax/discounts columns are 0; only total populated
5. **Refund amounts not captured** - `refunded` column shows $0 even for REFUNDED orders
6. **Shopify $0 orders** - 301 orders have $0 total for two reasons:
   - TikTok Shop synced orders (tagged `["free", "tiktok"]`, email `@scs.tiktokw.us`) - payment via TikTok, synced for fulfillment only
   - Free exchanges/replacements (tagged `["exchange", "free"]` or `["damage", "exchange", "free"]`)

## Data Gaps to Fill

| Missing Data | Where to Get It | Impact |
|--------------|-----------------|--------|
| COGS/inventory costs | Resource Fashion invoices, other suppliers | Needed for true profit calculation |
| Shipping/fulfillment costs | 3PL invoices, USPS/UPS statements | Major expense currently untracked |

See `DATA_DICTIONARY.md` for complete schema documentation.
