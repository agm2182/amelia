# QuickBooks Chart of Accounts - Cherri

Active accounts after cleanup (reduced from ~125 to ~69 accounts).

## Bank & Credit Cards

| Account | Type | Notes |
|---------|------|-------|
| Capital One Checking x2420 | Bank | Main operating account |
| Capital One Credit Card x6284 | Credit Card | Primary business card |

## Income

| Account | Type | Notes |
|---------|------|-------|
| Channel sales | Income | Parent for e-commerce sales |
| Channel sales:Shopify sales | Income | Shopify revenue |
| TikTok Shop Revenue | Income | TikTok Shop sales |
| Channel shipping income | Income | Parent |
| Channel shipping income:Shopify | Income | Shipping charged to customers |
| Channel discount | Income | Parent (contra-revenue) |
| Channel discount:Shopify discount | Income | Discounts given |
| Refunds & discounts to customers | Income | Contra-revenue |
| Other income:Credit card rewards | Income | Capital One rewards |
| Uncategorized Income | Income | Catch-all |

## Cost of Goods Sold

| Account | Type | Notes |
|---------|------|-------|
| Cost of goods sold | COGS | Parent |
| Cost of goods sold:Direct supplies & materials | COGS | Inventory/manufacturing costs |
| Channel selling fees | COGS | Parent |
| Channel selling fees:Shopify fees | COGS | Shopify transaction fees |
| Channel adjustments | COGS | Parent |
| Channel adjustments:Shopify adjustments | COGS | Shopify adjustments |
| TikTok Shop Fees | COGS | TikTok platform fees |

## Expenses

| Account | Type | Notes |
|---------|------|-------|
| Meta Ads | Expense | Facebook/Instagram advertising |
| TikTok Ads | Expense | TikTok advertising |
| Advertising & marketing | Expense | Parent for other marketing |
| Shipping & Fulfillment | Expense | Outbound shipping costs |
| Packaging Supplies | Expense | Boxes, mailers, etc. |
| Software & Subscriptions | Expense | Shopify, Mailchimp, etc. |
| Merchant Processing Fees | Expense | Payment processing |
| Platform Fees - Shopify | Expense | Shopify subscription |
| Interest Expense | Expense | Loan/credit card interest |
| Other business expenses | Expense | Parent |
| Other business expenses:Bank charges | Expense | Bank fees |
| Contract labor | Expense | Models, interns |
| Professional Services | Expense | Marketing agency |
| Supplies | Expense | General supplies |
| Taxes and Licenses | Expense | Business taxes/licenses |
| Travel | Expense | Business trips |
| Meals:Travel meals | Expense | Meals during business travel |
| Uncategorized Expense | Expense | Catch-all |

## Fixed Assets

| Account | Type | Notes |
|---------|------|-------|
| Tools, machinery, & equipment | Fixed Asset | Sewing machine |

## Liabilities

| Account | Type | Notes |
|---------|------|-------|
| Short-term business loans | Liability | Current portion of loans |
| Long-term business loans | Liability | Long-term debt |
| Channel sales tax payable - USD | Liability | Shopify sales tax |
| Sales tax payable | Liability | General sales tax |

## Equity

| Account | Type | Notes |
|---------|------|-------|
| Opening balance equity | Equity | Initial setup |
| Retained Earnings | Equity | Accumulated profits |
| Owner draws | Equity | Owner withdrawals |
| Owner investments | Equity | Capital contributions |

## Assets

| Account | Type | Notes |
|---------|------|-------|
| Accounts receivable | Asset | A/R |
| Accounts payable | Asset | A/P |
| Inventory | Asset | Product inventory |
| Undeposited funds | Asset | Pending deposits |
| Shopify holds and disputes | Asset | Shopify payment holds |
| Channel clearing account | Asset | Parent |
| Channel clearing account:Shopify | Asset | Shopify clearing |
| Prepaid expenses | Asset | Prepayments |

---

## Bank Rules

Rules to auto-categorize recurring transactions.

### Credit Card Transactions

| Pattern | Category | Vendor | Notes |
|---------|----------|--------|-------|
| `FACEBK*` or `META*` | Meta Ads | Meta | Facebook/Instagram ads |
| `TIKTOK*` | TikTok Ads | TikTok | TikTok advertising |
| `MAILCHIMP` | Software & Subscriptions | Mailchimp | Email marketing |
| `SHOPIFY` | Platform Fees - Shopify | Shopify | Platform subscription |
| `FEDEX` or `FEDERAL EXPRESS` | Shipping & Fulfillment | FedEx | Shipping |
| `USPS` or `STAMPS.COM` | Shipping & Fulfillment | USPS | Shipping |
| `UPS*` | Shipping & Fulfillment | UPS | Shipping |
| `ULINE` | Packaging Supplies | Uline | Packaging materials |
| `INTEREST CHARGE` | Interest Expense | (bank) | Credit card interest |
| `LATE FEE` | Other business expenses:Bank charges | (bank) | Late payment fees |
| `CANVA` | Software & Subscriptions | Canva | Design software |
| `ADOBE` | Software & Subscriptions | Adobe | Creative software |

### Checking Account Transactions

| Pattern | Category | Vendor | Notes |
|---------|----------|--------|-------|
| `SHOPIFY` (deposit) | Channel sales:Shopify sales | Shopify | Payout deposits |
| `TIKTOK` (deposit) | TikTok Shop Revenue | TikTok | Settlement deposits |
| `CAPITAL ONE MOBILE` | (Transfer) | -- | CC payment transfer |
| `Shopify Capital` | Short-term business loans | Shopify Capital | Loan payments |

---

## Notes from Transaction Review

### Credit Card (x6284) - 46 Pending Transactions

**Patterns identified:**

| Pattern | Category | Vendor | Rule Priority |
|---------|----------|--------|---------------|
| `Resource` | Cost of goods sold:Direct supplies & materials | Resource Fashion | HIGH - ~20 transactions |
| `CAPITAL ONE MOBILE` | Transfer | -- | HIGH - CC payments |
| `CAPITAL ONE ONLINE` | Transfer | -- | HIGH - CC payments |
| `ECOENCLOSE` | Packaging Supplies | EcoEnclose | MEDIUM |
| `FEDERAL EXPRESS` or `FEDEX` | Shipping & Fulfillment | FedEx | MEDIUM |
| `INTEREST CHARGE` | Interest Expense | -- | MEDIUM |
| `PAST DUE FEE` or `LATE FEE` | Other business expenses:Bank charges | -- | MEDIUM |
| `SPANX` | Cost of goods sold:Direct supplies & materials | Spanx | LOW - competitor samples |
| `Integrated Financial` | Other business expenses:Bank charges | Integrated Financial | LOW - verify purpose |
| `Velocity Group` | Other business expenses:Bank charges | Velocity Group | LOW - verify purpose |

**Unclear transactions to investigate:**
- "Payment received. Thank y" - $1,200 and $3,400 received - Refunds? Customer payments?

### Checking (x2420) - 2,763 Pending Transactions

*(To be reviewed after credit card)*

