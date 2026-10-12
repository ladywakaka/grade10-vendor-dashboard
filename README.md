# Grade10 Vendor Dashboard

A password-protected dashboard of the trading card vendors Grade10 has met at card shows. The data comes from the **Vendors** database in Notion (Grade10 / Card Shows / Trading Card Vendor Database).

## How it works

1. A GitHub Action (`.github/workflows/deploy.yml`) runs every day at 02:00 HKT, on every push to `main`, and whenever you click **Run workflow**.
2. `scripts/fetch_notion.py` pulls every vendor from Notion.
3. `scripts/build.py` puts the data into `src/template.html`.
4. [StatiCrypt](https://github.com/robinmoisson/staticrypt) encrypts the page with the team password, and the encrypted page is published to GitHub Pages.

No vendor data is stored in this repository. Only the encrypted page is published.

## Secrets (Settings > Secrets and variables > Actions)

| Name | What it is |
|---|---|
| `NOTION_TOKEN` | Internal integration secret from notion.so/my-integrations. The Vendors database must be shared with that integration. |
| `DASHBOARD_PASSWORD` | The password the team types to open the dashboard. Change it here, then run the workflow again. |

## Updating the dashboard now

Actions tab > **Build and publish dashboard** > **Run workflow**.
