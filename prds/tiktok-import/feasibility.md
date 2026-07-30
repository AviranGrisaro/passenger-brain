# Feasibility note — TikTok import

**Owner:** data-engineer
**Date:** 2026-07-30
**Status:** Scoping complete. PRD-writing still held on Aviran's ToS/access sign-off, not on this note — see Recommendation.
**Authorizing line:** `strategy/passenger-strategy.md` V1 scope — `"TikTok import... user saves a TikTok video into Passenger... the app extracts places mentioned or shown in the video and adds them to Saved Places"` (decision #34).
**Source:** This note ports the findings of `passenger-brain/data-eng/scenic-walk-tiktok-feasibility.md` §2 (Linear `PAS-7`, closed 2026-07-30) into the PRD-gate location `product` reads before writing PRDs. It is not new research — read the source doc for full derivation; this is the feature-scoped summary plus the go/no-go/slip call.

## Recommended approach

Combine three signals into one LLM-based extraction pass, skip frame-based visual place recognition entirely:

- **Caption text / on-screen OCR** — many recommendation-style TikToks overlay the place name as on-screen text, or name it in the caption/location tag directly. Apple's on-device Vision framework does OCR natively; Google Cloud Vision/AWS Textract as cloud fallback. **Highest ROI-per-effort of the three signals** — primary, not supporting.
- **Audio transcription + NLP entity extraction** — transcribe narration (Whisper API or equivalent ASR), run entity extraction (NER or an LLM prompt) over transcript + caption text, geocode candidate names against a places API scoped to Tel Aviv. Buildable with commodity tooling, no novel research.
- **Frame-based visual/object/landmark detection — not recommended.** Generic landmark-detection APIs work for famous global landmarks, not small unmarked local venues, which is exactly what this product cares about. No maintained image database of local Tel Aviv businesses exists to match against.

Feed OCR + caption + transcript into one LLM extraction pass, geocode the candidates, confidence-score them, and require a **mandatory confirm-before-save step** in the UI — not silent auto-add. Accuracy is genuinely uneven (see below), so the UX has to carry that, not the pipeline.

## Effort estimate

**~2–4 weeks** for a working v1 pipeline (OCR + transcription + LLM extraction + geocoding + confidence-gated user-confirmation step), assembling off-the-shelf APIs rather than building any component from scratch — assuming the ToS/access question below is resolved quickly. Tuning down false positives further is realistic post-launch iteration, not a Phase 1 blocker in itself.

## Key risks / unknowns

- **ToS/access risk — the real blocker, not a technical one.** Fetching the full video content of an arbitrary shared TikTok (not the uploader's own account) via unofficial means carries genuine ToS exposure. This needs Aviran's explicit sign-off before a TRD is written — noted here because it blocks the build, not because it's mine to decide. Per the data-engineer role file, ToS sign-off is Aviran's call.
- **Extraction accuracy is unbenchmarked. [ASSUMPTION]** No benchmark data exists for this; the following is a professional estimate, not a sourced number: combined caption+OCR+audio signal probably surfaces an extractable, geocodable place name in a minority-to-roughly-half of recommendation-style videos. Many videos never name the specific place (relying on the viewer already knowing it, or vague framing like "this hidden gem"), and geocoding accuracy drops further for generic/ambiguous names or chains. V1 cannot promise reliable extraction — it needs confirm-before-save, not silent auto-add.
- **Ingestion surface (share-extension vs. in-app paste) is not scoped here.** That's an iOS build-surface question for a TRD once the ToS question clears, not a data/algorithm feasibility question.

## Recommendation: GO, gated on Aviran's ToS/access sign-off

**Buildable in the Phase 1 window** as a v1 pipeline with mandatory confirm-before-save — this is the more tractable of the two features `data-engineer` was asked to scope (Scenic Walk's heavier version is not buildable in Phase 1; see `prds/scenic-walk/feasibility.md`), since it's mostly assembling existing commodity AI APIs rather than inventing a new algorithm.

The real risk isn't algorithmic feasibility — it's (a) the TikTok ToS/access question, which needs Aviran's explicit call before a TRD gets written, and (b) accuracy will be genuinely uneven, which is a UX/design constraint (confirm-before-save) more than a build blocker. This is a recommendation to build, not a resolution of the open sign-off — Linear `PAS-6` item 9 ("ToS/legal sign-off needed before a TRD") is still open and is Aviran's call. `product` should hold the PRD until that sign-off lands, same as before this note; what changes is that the technical feasibility question itself is now answered (yes).

---

## Data/schema needs — addendum by `product`, 2026-07-30

Added under the standing data/schema rule (founder-direct 2026-07-30, `agent-os/PROGRESS.md`). **This is not a PRD and does not resolve `PAS-6` item 9** — it records the data model this feature implies, so it exists in writing before someone builds against an assumed one. `data-engineer`'s text above is unchanged.

**What the extraction pipeline needs stored, none of which exists:**

- **Extraction candidate** — one row per place the LLM pass proposes from a video: the raw extracted string, which signal produced it (caption / OCR / transcript), the geocoded coordinates, and the source video reference.
- **Confidence score** per candidate, and the threshold that decides whether it is shown at all. §"Key risks" above says accuracy is unbenchmarked and confirm-before-save is mandatory, so the threshold is a product decision with a falsifiable pass condition, not a tuning constant.
- **Confirmation state** per candidate — proposed / confirmed / rejected. Required because the confirm step is mandatory and because a rejected candidate must not be re-proposed from the same video.

**The unasked question, and it is a schema collision, not a detail.** Strategy says the app *"adds them to Saved Places."* But `places-been-saved`'s store is **device-local and keyed on `place_id`** — a reference into the curated public `places` table. An extracted place that is not already in `places` has no id to save. That leaves three shapes, and nobody has chosen one:

1. Import only matches **existing** curated places, and anything unmatched is dropped. Cheapest, and quietly guts the feature — the interesting TikTok find is precisely the one not already curated.
2. Imported places live **device-local only**, as rows with no `places` id. Needs a second place representation in the client, and such a place has no Hood, no category, no keywords, no flag — so it appears in Places and nowhere else on the map.
3. Confirmed imports **write into the shared `places` table**. This is a **user-write surface into curated public data** and opens moderation, quality and abuse questions. Strategy has already refused this shape once, in a different place: *"Legend may unlock submitting your own recommendations… Floated, not decided — that's a new user-write surface into a currently curated+algorithmic pipeline (moderation, quality, abuse questions all open) and needs its own call, not an assumed inclusion."*

Option 3 needs an explicit Aviran call on the same grounds that line already states. **Whichever option is chosen, the extraction/geocoding/confidence store above is substantial enough to be its own supporting PRD** — write it alongside the feature PRD, not inside it, once `PAS-6` item 9 clears.
