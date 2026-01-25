# Financials

Financial records for Cherri.

## Folder Structure

```
financials/
├── bank-statements/
│   ├── Capital One Checking Account Statements/  # Monthly PDFs
│   ├── Capital One Credit Card/                  # Monthly PDFs
│   └── Chase Credit Card/                        # Transaction CSV
└── tiktok-shop/
    ├── originals/                # Archived XLSX exports (16 files)
    ├── 2025-q{N}_{dates}.*.csv   # Quarterly data by sheet type
    ├── tiktok_2025_combined.csv  # All order details merged
    └── tiktok_2025_summary.csv   # Monthly revenue summary
```

## TikTok Shop Data

Each TikTok Shop income export contains 6 sheets, converted to separate CSVs:

| Sheet | Description |
|-------|-------------|
| `Fees_explanation` | Breakdown of TikTok Shop fees |
| `Order_details` | Line-item transaction data |
| `Payments` | Payment settlement records |
| `Reports` | Summary report data |
| `Reserve_details` | Held/reserve fund details |
| `Statements` | Account statements |

Original XLSX files are archived in `tiktok-shop/originals/`.

### Quarterly Data Files

Files are named `2025-q{N}_{start}-{end}.{sheet}.csv` where N indicates the quarter and sub-period:

| File Prefix | Date Range | Notes |
|-------------|------------|-------|
| `2025-q1_jan01-mar29` | Jan 1 - Mar 29 | Full Q1 |
| `2025-q2a_apr01-jun27` | Apr 1 - Jun 27 | Q2 early export |
| `2025-q2b_apr01-jun29` | Apr 1 - Jun 29 | Q2 extended |
| `2025-q3a_jun30-sep26` | Jun 30 - Sep 26 | Q3 early export |
| `2025-q3b_jul01-sep26` | Jul 1 - Sep 26 | Q3 alternate start |
| `2025-q4a_sep29-dec26` | Sep 29 - Dec 26 | Q4 early export |
| `2025-q4b_oct02-dec27` | Oct 2 - Dec 27 | Q4 alternate start |
| `2025-q4c_dec27-dec31` | Dec 27 - Dec 31 | Q4 year-end |

Multiple files per quarter exist due to overlapping export dates from TikTok Shop.
