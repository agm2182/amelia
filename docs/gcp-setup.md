# Google Cloud Platform Setup for Cherri SEO

This guide walks through setting up GCP service accounts for Google Search Console, Google Analytics 4, and Google Ads MCP servers.

## Prerequisites

- Google account with access to Cherri's GSC, GA4, and Google Ads
- Admin access to grant permissions

## Step 1: Create GCP Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" > "New Project"
3. Name: `cherri-seo-research`
4. Click "Create"

## Step 2: Enable APIs

In the GCP Console, go to "APIs & Services" > "Library" and enable:

1. **Search Console API**
   - Search for "Google Search Console API"
   - Click "Enable"

2. **Analytics Data API**
   - Search for "Google Analytics Data API"
   - Click "Enable"

3. **Google Ads API**
   - Search for "Google Ads API"
   - Click "Enable"
   - Note: Requires approved developer token for production use

## Step 3: Create Service Account

1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name: `claude-code-seo`
4. Description: "Read-only access for Claude Code SEO research"
5. Click "Create and Continue"
6. Skip the role assignment (permissions granted at service level)
7. Click "Done"

## Step 4: Create Key

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select "JSON"
5. Click "Create"
6. Save the downloaded file as `cherri-seo-credentials.json`
7. Store securely (never commit to git)

## Step 5: Grant Access to Services

### Google Search Console

1. Go to [Search Console](https://search.google.com/search-console/)
2. Select Cherri's property
3. Go to "Settings" > "Users and permissions"
4. Click "Add user"
5. Enter the service account email (e.g., `claude-code-seo@cherri-seo-research.iam.gserviceaccount.com`)
6. Set permission to "Restricted" (read-only)
7. Click "Add"

### Google Analytics 4

1. Go to [Google Analytics](https://analytics.google.com/)
2. Select Cherri's GA4 property
3. Go to "Admin" > "Property Access Management"
4. Click "+" > "Add users"
5. Enter the service account email
6. Set role to "Viewer"
7. Click "Add"

### Google Ads

1. Go to [Google Ads](https://ads.google.com/)
2. Select Cherri's account
3. Go to "Tools & Settings" > "Access and security"
4. Click "+" to add user
5. Enter the service account email
6. Set access level to "Read only"
7. Click "Send invitation"

## Step 6: Add MCP Servers to Claude Code

Store your credentials in a secure location (e.g., `~/.config/cherri/`):

```bash
mkdir -p ~/.config/cherri
mv ~/Downloads/cherri-seo-credentials.json ~/.config/cherri/
chmod 600 ~/.config/cherri/cherri-seo-credentials.json
```

Then add the MCP servers:

```bash
# Google Search Console
claude mcp add gsc \
  -e GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/cherri/cherri-seo-credentials.json \
  -- npx -y mcp-server-gsc

# Google Analytics 4
claude mcp add ga4 \
  -e GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/cherri/cherri-seo-credentials.json \
  -- npx -y @anthropic/google-analytics-mcp

# Google Ads (when available)
claude mcp add google-ads \
  -e GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/cherri/cherri-seo-credentials.json \
  -- npx -y @anthropic/google-ads-mcp
```

## Step 7: Verify Setup

Restart Claude Code and test each integration:

```
# Test GSC
"Show me Cherri's top 10 queries by impressions from the last 28 days"

# Test GA4
"What were Cherri's top landing pages by sessions last week?"

# Test Google Ads
"Show keyword ideas for 'sustainable underwear'"
```

## Troubleshooting

### "Permission denied" errors
- Verify the service account email was added correctly
- Check that the JSON credentials file path is correct
- Ensure APIs are enabled in GCP Console

### "API not enabled" errors
- Go to GCP Console > APIs & Services > Library
- Search for and enable the required API

### "Invalid credentials" errors
- Regenerate the JSON key file
- Update the `GOOGLE_APPLICATION_CREDENTIALS` path

## Security Notes

- Never commit credentials to git
- Use read-only permissions where possible
- Rotate keys periodically
- Consider using Workload Identity Federation for production
