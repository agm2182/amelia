# Vendors & Contractors

Business relationships for Cherri - contractors, service providers, and suppliers.

## Quick Reference

See `index.yaml` for searchable vendor data.

## Structure

```
vendors/
├── index.yaml           # All vendors: name, type, status, contact
├── ldc-coop.md          # Detailed profile with history/notes
└── documents/
    └── ldc-coop/        # Contracts, invoices, correspondence
```

## Status Values

| Status | Meaning |
|--------|---------|
| `active` | Ongoing relationship, in good standing |
| `inactive` | No current work, relationship intact |
| `disputed` | Active disagreement or performance issues |
| `terminated` | Relationship ended |

## Adding a Vendor

1. Add entry to `index.yaml`
2. Create `[vendor-slug].md` with relationship details
3. Create `documents/[vendor-slug]/` for contracts and invoices
