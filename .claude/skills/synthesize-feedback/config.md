# synthesize-feedback — config

Values the skill reads in Step 0. Fill in the placeholders (`<…>`). If a value is still a
placeholder when the skill runs, it will ask you once, then note the gap in the report.

## App-store reviews (best-effort web)
- **App Store app id:** `<APP_STORE_APP_ID>`  <!-- numeric id from the App Store URL, e.g. id1234567890 -->
- **App Store country:** `us`
- **Reviews RSS:** `https://itunes.apple.com/us/rss/customerreviews/page=1/id=<APP_STORE_APP_ID>/sortby=mostrecent/json`
- **Google Play package:** `<PLAY_PACKAGE_NAME>`  <!-- e.g. com.ampfit.app -->

## Social (best-effort web search)
- **Search terms:** `"Amp Fit"`, `Amp Fitness app`, `@ampfit`
- **Where:** Reddit, X/Twitter, Google Play reviews

## Slack channels to scan
<!-- bare channel names; the collector also keyword-searches workspace-wide for feedback -->
- `<#support-channel>`
- `<#product-feedback>`
- `<#voice-of-customer>`

## Gmail queries
<!-- the {window} token is replaced with a Gmail date filter, e.g. newer_than:7d -->
- `subject:(feedback OR NPS OR review OR "feature request") {window}`
- `(cancel OR refund OR "not working" OR bug) {window}`

## Defaults
- **Window:** last 7 days
- **Urgent triggers:** outage, data loss, billing/refund, churn/cancellation, legal, safety, sharp negative-sentiment spike
