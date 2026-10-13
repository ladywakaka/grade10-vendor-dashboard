# G10 Partner and Exhibitor Pipelines

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

## Second page: G10 Shop Launch Tracker (`/launch/`)

A password-protected tracker for the Causeway Bay shop launch, at https://ladywakaka.github.io/grade10-vendor-dashboard/launch/ (same team password).

- **Data:** Notion page **Grade10 › G10 Shop Launch Tracker**, with three databases: **Activations** (Status, dates, open items; the plan from the deck is in each row's page), **KOL Invitations** (Reply Status, Note) and **Green Light Decisions** (Status, Needed By).
- **Updating:** change a status or note in Notion. The page rebuilds every night at 02:00 HKT, or straight away with **Run workflow**.
- **Crossed-out names:** in an activation's **Crossed Out** field, write `Name: reason` (one per line). The name is shown struck through wherever it appears on that activation.
- **Do not change** the **Key** fields; they link rows to the page.
- `scripts/fetch_launch.py` pulls the three databases (the integration needs access to the G10 Shop Launch Tracker page), `scripts/build_launch.py` fills `src/launch.html`, and the workflow encrypts it into `dist/launch/`. If the launch fetch fails, the vendor dashboard still publishes.
