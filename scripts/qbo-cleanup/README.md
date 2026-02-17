# QBO Cleanup Scripts

Analysis and automation scripts for fixing QuickBooks Online account balances.
Created during the Feb 2026 cleanup session. See GitHub issue #56 for the
Capital One Checking work that uses these.

## Python Analysis Scripts

Run with `uv run python3 <script>`.

| Script | Purpose |
|--------|---------|
| `qbo_checking_analysis.py` | Monthly breakdown of Capital One CSV data — deposits, withdrawals, running balance |
| `qbo_checking_gap_analysis.py` | Compares CSV totals vs QBO register, identifies missing transactions by category |
| `qbo_count_shopify_capital.py` | Counts Shopify Capital/Credit transactions in CSV, tests hypothesis about missing loan entries |

## JavaScript DOM Helpers

Run with `agent-browser eval "$(cat <script>)"`. These extract data from QBO register pages.

| Script | Purpose |
|--------|---------|
| `qbo_click_first_entry.js` | Clicks the first data row in any QBO register grid |
| `qbo_count_rows.js` | Counts data rows on the current register page |
| `qbo_extract_page2.js` | Extracts all entries on current page: date, payment, deposit, balance, type, memo |
| `qbo_read_inputs.js` | Reads all input field values on a QBO form (for verifying before save) |
| `qbo_check_balance.js` | Reads first data row's INC/DEC/BAL values (liability register) |
| `qbo_read_headers.js` | Reads column headers from the register grid |
| `qbo_read_checking.js` | Reads headers + first 5 entries from checking register |
| `qbo_read_oldest_detail.js` | Reads last 20 entries (oldest) from current page |
| `qbo_read_coa_row.js` | Reads Chart of Accounts row details for a filtered account |

## Shell Automation

| Script | Purpose |
|--------|---------|
| `qbo_delete_loop_v3.sh` | Deletes register entries one by one (liability register). Click → Delete → Yes loop. |
| `qbo_delete_loan_loop.sh` | Extended deletion loop with page refresh logic for large accounts (500+ entries). |

## QBO Account IDs

| Account | ID | URL |
|---------|----|-----|
| Capital One Checking x2420 | 1150040000 | `https://qbo.intuit.com/app/register?accountId=1150040000` |
| Shopify Capital Loan | 1150040012 | `https://qbo.intuit.com/app/register?accountId=1150040012` |
| Shopify Capital Loans Payable | 1150040025 | `https://qbo.intuit.com/app/register?accountId=1150040025` |
| Shopify Credit | 1150040013 | `https://qbo.intuit.com/app/register?accountId=1150040013` |
