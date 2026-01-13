# Cherri SEO & Growth Research

Claude Code-powered SEO research infrastructure for Cherri (underwear e-commerce).

## Structure

```
cherri/
├── research/
│   ├── audits/          # Technical SEO audit outputs
│   ├── keywords/        # Keyword research data
│   ├── competitors/     # Competitor analysis
│   └── content-briefs/  # Content planning docs
├── data/                # Raw data exports (gitignored)
├── skills/
│   └── cherri-seo/      # Custom Claude skills
└── .claude/
    └── settings.local.json
```

## MCP Servers

| Server | Purpose | Status |
|--------|---------|--------|
| Semrush | Keywords, competitors, trends | Configured |
| Shopify Dev | API docs, GraphQL schema | Configured |
| Google Search Console | Search performance data | Requires GCP setup |
| Google Analytics | GA4 data | Requires GCP setup |
| Google Ads | Keyword planning | Requires GCP setup |

## Setup

### 1. MCP Servers (Already configured)

```bash
# Semrush - requires SEO Business plan + API subscription
claude mcp add semrush https://mcp.semrush.com/v1/mcp -t http

# Shopify Dev - no auth required
claude mcp add shopify -- npx -y @shopify/dev-mcp@latest
```

### 2. Google Cloud Setup (Manual)

1. Create GCP project: `cherri-seo-research`
2. Enable APIs:
   - Search Console API
   - Analytics Data API
   - Google Ads API
3. Create service account with read-only access
4. Download JSON credentials
5. Add to Claude:

```bash
claude mcp add gsc -e GOOGLE_APPLICATION_CREDENTIALS=/path/to/creds.json -- npx -y mcp-server-gsc
claude mcp add ga4 -- npx -y @anthropic/google-analytics-mcp
```

### 3. Ahrefs

Store API key in `.env`:
```
AHREFS_API_KEY=your_key_here
```

## Custom Skills

- `cherri-keyword-research` - Find keyword opportunities
- `cherri-competitor-analysis` - Track competitor SEO
- `cherri-shopify-seo` - Audit and optimize storefront
- `cherri-content-brief` - Generate SEO content briefs

## Usage

```bash
# Start Claude Code in this directory
cd /path/to/cherri
claude

# Example queries:
# "Analyze top organic keywords for cherri.com"
# "Find striking distance queries from GSC"
# "Generate content brief for 'sustainable underwear'"
# "Audit product page SEO for top 10 products"
```
