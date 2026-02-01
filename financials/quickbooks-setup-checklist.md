# QuickBooks Setup Checklist for Cherri

## Phase 1: Account & Basic Setup

- [ ] Create QuickBooks Online account (Plus plan recommended for inventory tracking)
- [ ] Set company info: Cherri LLC, business type, fiscal year (calendar)
- [ ] Enable multi-currency if needed (USD only for now)

## Phase 2: Connect Bank Accounts

- [ ] Connect Chase credit card (account ending 0982)
- [ ] Connect Capital One checking (account ending 2420)
- [ ] Connect Capital One credit card (account ending 6284)
- [ ] Verify Shopify Payments deposits appear (via connected checking)

## Phase 3: Chart of Accounts

Create accounts matching existing expense categories:

**Income Accounts**
- [ ] Sales - Shopify
- [ ] Sales - TikTok Shop

**Expense Accounts**
- [ ] Advertising - Meta (Facebook/Instagram)
- [ ] Advertising - TikTok
- [ ] Cost of Goods Sold - Inventory/Manufacturing
- [ ] Software & Subscriptions (Mailchimp, Shopify, etc.)
- [ ] Bank Fees & Interest
- [ ] Late Fees

**Liability Accounts**
- [ ] Shopify Capital Loan
- [ ] Shopify Credit
- [ ] Clearco (if balance remaining)
- [ ] OnRamp Revenue Advance

## Phase 4: Vendor Setup

Create vendors for recurring payees:

- [ ] TikTok Ads
- [ ] Meta (Facebook) Ads
- [ ] Resource Fashion (manufacturer)
- [ ] Mailchimp
- [ ] Shopify
- [ ] L,D,&C Co-Op (contractor - disputed)

## Phase 5: Integrations

- [ ] **A2X** - Connect Shopify for automated sales reconciliation
  - Handles Shopify orders, refunds, fees, payouts
  - ~$19-79/mo depending on order volume
- [ ] **Settle** (optional) - For inventory financing & PO management
  - Useful if scaling inventory purchases

## Phase 6: Historical Data Import

**Option A: Bank feed import (easiest)**
- [ ] Let QuickBooks pull transactions from connected accounts
- [ ] Categorize transactions using rules

**Option B: Manual CSV import**
- [ ] Import `expenses/2025_chase_categorized.csv` as expenses
- [ ] Import `revenue/shopify/all_payouts.csv` as deposits
- [ ] Import `loans/all_financing_history.csv` as loan transactions

## Phase 7: Opening Balances

Set opening balances as of Jan 1, 2025 (or current date):

- [ ] Bank account balances
- [ ] Credit card balances
- [ ] Outstanding loan balances:
  - Shopify Capital: ~$4,500 remaining
  - Shopify Credit: ~$8,400 balance
  - (See `loans/README.md` for current figures)

## Phase 8: Reconciliation

- [ ] Reconcile each bank/card account for 2025
- [ ] Verify revenue matches Shopify reports ($166.6K)
- [ ] Verify TikTok Shop revenue (~$38.6K settlements)
- [ ] Verify ad spend totals (Meta $77.4K, TikTok $7.7K)

## Data Gaps to Address

| Gap | Action Needed |
|-----|---------------|
| ~~Capital One transactions~~ | ✅ Parsed from PDF statements (see below) |
| COGS itemization | Request invoices from Resource Fashion |
| Shipping costs | Pull from Shopify shipping labels or 3PL |
| TikTok Shop fees | Already in `revenue/tiktok-shop/2025_quarterly.csv` |

## Files Reference

| Purpose | File |
|---------|------|
| Chase expenses | `financials/expenses/2025_chase_categorized.csv` |
| Capital One checking (QB import) | `financials/expenses/bank-statements/capital-one-checking/2025_qb_import.csv` |
| Capital One credit (QB import) | `financials/expenses/bank-statements/capital-one-credit/2025_qb_import.csv` |
| Shopify payouts | `financials/revenue/shopify/all_payouts.csv` |
| Shopify orders | `financials/revenue/shopify/2025_orders.csv` |
| TikTok settlements | `financials/revenue/tiktok-shop/2025_statements.csv` |
| All loans | `financials/loans/all_financing_history.csv` |
| Loan details | `financials/loans/README.md` |

## Cost Estimate

| Service | Monthly Cost |
|---------|--------------|
| QuickBooks Online Plus | $50-80 |
| A2X (Shopify) | $19-79 |
| **Total** | ~$70-160/mo |
