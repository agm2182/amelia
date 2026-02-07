# Bookkeeping Notes

Categorization decisions and QuickBooks conventions for Cherri.

## QuickBooks Chart of Accounts Reference

| Account | Type | Detail Type | Notes |
|---------|------|-------------|-------|
| Shopify Credit | Credit Card BAL | Credit Card | Shopify credit card product, NOT a loan. Shopify takes 10% of daily sales to pay it down. |
| Order Protection Pass Through | Other Expense | Other Expense | Pass-through: customer pays at checkout, Order Protection debits checking. Should net to ~$0. |
| Capital One Checking x2420 | Bank | Checking | Primary business checking account |
| Capital One Credit Card x6284 | Credit Card | Credit Card | Business credit card |

## Transaction Categorization Rules

### Shopify Credit Card Transactions

| Transaction Type | Category/Action | Reasoning |
|-----------------|----------------|-----------|
| REPAYMENT FROM SALES | Record as transfer → Capital One Checking x2420 | Shopify's daily 10% deduction from sales. Balance transfer, not an expense. |
| Manual (lump sum payments) | Record as transfer → Capital One Checking x2420 | Voluntary payments Gaby makes from checking to pay down the card. |
| AUTOMATIC PAYMENT | Record as transfer → Capital One Checking x2420 | Bank autopay from checking. Same as manual payments. |
| CASHBACK-REWARD | Categorize → Other income: Credit card rewards | Cashback earned on purchases. |
| Klaviyo | Categorize → Software & Subscriptions | Email marketing platform subscription. |
| Statement fees | Categorize → Other business expenses: Bank and credit card fees | Monthly statement/service fees. |
| Facebk * (various) | Categorize → Advertising & marketing | Meta/Facebook/Instagram ad charges. Payee should be renamed to "Meta Ads". |
| Tiktok Ads | Categorize → Advertising & marketing | TikTok advertising charges. |

**Key principle:** Credit card payments between accounts are **transfers** (balance sheet), not **expenses** (P&L). The actual expenses are the individual charges on the card.

### Vendor Categorization Decisions

| Vendor | Category | Reasoning |
|--------|----------|-----------|
| Discountmugs.com | Shipping & Fulfillment Expense | Prints care instruction cards included in shipments. NOT advertising despite the vendor name. |
| Order Protection | Order Protection Pass Through | Customer-funded package protection. Has dedicated COA account. |
| Unsellable product samples | Design & Development | Pre-production/R&D costs for prototypes that can't be sold. Not COGS. |
| Resource Fashion | Inventory/COGS | Primary manufacturer. |
| Klaviyo | Software & Subscriptions | Email marketing SaaS. |

### Photoshoot Expenses

Depends on purpose:
- **Marketing assets** (product photos for website/ads) → Advertising & marketing
- **Studio rental, props, styling** → Advertising & marketing (subfolder of the shoot)
- **Model fees** → Contract labor (if separate line items)

