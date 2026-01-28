# Clear.co (Clearco)

**Portal:** https://my.clearbanc.com/
**Data captured:** January 28, 2026

## Current Status

| Field | Value |
|-------|-------|
| Fixed Funding Capacity | $6,000 (preliminary) |
| Used | $0 |
| Available | $6,000 |
| Capital Advances | None active |

The account shows available funding capacity but no active loans or advances.

## Product Types

Clear.co offers several funding products:

1. **Capital Advances** (Legacy) - Cash advances repaid as % of revenue
2. **Invoice Funding** - Funding against vendor invoices, repaid weekly
3. **Receipt Funding** - Similar to invoice funding

## Invoice Funding History

119 payments recorded from July 2024 to September 2025, all successful.

### Vendors

| Vendor | Typical Weekly Payment | Period |
|--------|----------------------|--------|
| MadeCo, LLC | $125-171 | Jul 2024 - Sep 2025 |
| ITB Fulfillment | $243 | Dec 2024 - Mar 2025 |
| Stellar Fashion Consulting | $162 | Jul 2024 - Nov 2024 |

### Payment Summary by Year

| Year | Payments | Total Amount |
|------|----------|--------------|
| 2024 | 59 | ~$9,800 |
| 2025 | 60 | ~$8,400 |
| **Total** | **119** | **~$18,200** |

## Signed Contracts (Documents)

| Document | Type | Date |
|----------|------|------|
| bnpl_bill-68878-203806-2025-05-13.pdf | BNPL Bill | May 13, 2025 |
| bnpl_bill-68306-203806-2025-04-07.pdf | BNPL Bill | Apr 7, 2025 |
| bnpl_bill-67512-203806-2025-03-06.pdf | BNPL Bill | Mar 6, 2025 |
| bnpl_bill-64498-203806-2024-11-01.pdf | BNPL Bill | Nov 1, 2024 |
| bnpl_bill-62247-203806-2024-08-24.pdf | BNPL Bill | Aug 24, 2024 |
| bnpl_bill-61261-203806-2024-07-17.pdf | BNPL Bill | Jul 17, 2024 |
| bnpl_bill-61040-203806-2024-07-03.pdf | BNPL Bill | Jul 3, 2024 |
| ach-59671-138862-2024-04-25.pdf | ACH Authorization | Apr 25, 2024 |
| advance-40085-207194-2022-01-06.pdf | Capital Advance | Jan 6, 2022 |
| ach-40086-116577-2022-01-06.pdf | ACH Authorization | Jan 6, 2022 |

The January 2022 advance document indicates an original capital advance that has been fully repaid.

## How Invoice Funding Works

1. Clearco pays vendor invoices on behalf of the business
2. Business repays Clearco weekly via automatic ACH
3. Repayment tied to invoice ID (e.g., 91C05, 1D2E1, B45F3)
4. Multiple invoices can run concurrently

## Data Files

| File | Description |
|------|-------------|
| `payment_history.csv` | All 119 invoice funding payments |
| `browser-state.json` | Saved browser session (gitignored) |

## Browser Session

To restore authenticated session:
```bash
agent-browser --headed --state .claude/browser-states/clearco.json open https://my.clearbanc.com/home
```

## Account Notes

- Business Profile: 3 of 4 steps completed
- Payment Obligations: Need updating to avoid funding delays
- Revenue Sources: Not connected (shows empty)
