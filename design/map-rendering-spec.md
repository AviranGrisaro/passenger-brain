# Passenger V1 — Map Rendering Spec

**Owner:** designer (drafted for Aviran)
**Date:** 2026-07-27 (terminology/flag pass 2026-07-30 — see the new note below and §3's flag; rendering logic itself untouched)
**Status:** Draft — awaiting Aviran's read
**Source:** `strategy/decisions.md` #12 (neighborhood + spot granularity), #17 (no gradients), #18 (three vibe tags), #25 (category chips move into the search sheet), #26 (Saved/Visited merge, auto-save into V1) + `design/design-principles.md` §2/§3/§5 + Aviran's direct pushback on tag-layer density (relayed 2026-07-27) and on the resulting self-contradiction — tag was left with zero rendering at city-wide zoom while `ux-flows.md` §2 still claimed it was visible at 0 taps. **2026-07-30 founders-meeting reconciliation** (decisions #27–36) touches this doc only at the margins — see the terminology note and §3's flag immediately below.
**Relationship to `design/ux-flows.md`:** §6 of that doc states the structural rules this spec implements — tag renders progressively by zoom, Mix is silent, the busy+Tourist warning replaces rather than stacks. This doc is the rendering detail underneath those rules: what's actually drawn, how pins cluster, and the exact accessibility labels. Read §6 first for the *why*; this doc is the *how*. No PRD exists yet to trace against, and this doc doesn't need its own high-fidelity mockup — it's a rendering-rules reference for whoever builds the map layer, not a flow a reviewer clicks through.

**Terminology note, 2026-07-30 (decision #27):** "Hoods" is now the confirmed product-facing term for what this doc calls "zone" / "neighborhood" throughout — decision #12's granularity is unchanged, only the external name is confirmed. Same equivalence note as `design/ux-flows.md` §0 — not repeated in full here; read every "zone"/"neighborhood" below as synonymous with "Hood." Not swept word-for-word in this pass.

**[FLAGGED, 2026-07-30, PAS-6 — not applied below.]** The 2026-07-29 founders-meeting brief proposes a boolean tourist-trap flag (decision #28) that may replace the three-way **Local · Mix · Tourist** tag this entire spec renders. Whether "no local tags" means the graduated tag disappears entirely, or something narrower survives, isn't certain — and every rule below (§§2–3) has already been through two real revisions with Aviran. **This spec is not rewritten against an unconfirmed reversal** — everything below still describes the locked three-tag model. See `ux-flows.md` §6's identical flag and §9 Q18.

---

## 1. Why this doc exists

Aviran's pushback, verbatim: *"how do you show tag layer on every location on the map? its gonna be too much information on one layer."* The original design badged every close-zoom pin with a tag, then stacked a warning badge on top of that for the worst case — heat fill + tag badge + warning badge, once per pin, in a neighborhood that might have forty pins on screen at once. That doesn't survive contact with Florentin at 8pm. This spec is the rendering-level fix: tag gets the same progressive disclosure heat already has, and spot-level tag comes off the map surface entirely.

**Revised again this round — the first fix over-corrected.** Moving tag to neighborhood-zoom-only badges solved the density problem but broke something else: it left tag with *zero* rendering at city-wide zoom, the zoom a cold open actually shows. `ux-flows.md` §2 still claimed the tag layer was "on by default, the first thing you see," 0 taps — true of heat, false of tag, a direct contradiction between that doc and this one. Aviran caught it: heat alone at cold open is the half of this product anyone already gets from Google Maps. Section 2 below fixes this by moving tag to a channel that was never in use — the zone's **outline**, not a badge — so it can be visible at every zoom, including city-wide, without reopening the density problem the first fix solved.

---

## 2. What renders at each zoom

| Zoom | Heat | Tag | Pins |
|---|---|---|---|
| **City-wide** | Neighborhood-scale blobs, stepped bands | Zone **outline stroke** — color + weight/dash — but **only on Local zones**; Mix and Tourist zones render unstroked | None |
| **Neighborhood** | Zone-level stepped-band fill | Outline stroke on **Local or Tourist** zones (Mix still unstroked), **plus a word label** at the zone's centroid spelling out the tag — this is the only zoom where the word appears | None |
| **Close** | Area-level fill, unchanged from neighborhood zoom | Outline stroke persists at zone boundaries still in view, same rule as neighborhood zoom, but **no word label** — **pins themselves carry no tag signal**, at any zoom | Individual markers, category only, plus a personal-place ring accent where it applies (§6) |

Heat and tag never share a visual channel, at any zoom: heat is always the area/fill treatment; tag, wherever it renders, is always the zone's outline stroke, independent of the fill's hue (design-principles.md §3 — never rely on color alone). **Tag is visible at zero taps at every zoom now, including city-wide — the contradiction with `ux-flows.md` §2 is resolved by giving tag a channel that scales, not by giving it back the badge that didn't.**

---

## 3. Zone tag rendering — stroke, plus a label at neighborhood zoom

The badge from the previous draft is gone. What carries the signal now is the zone's outline; the word is a label on top of that signal, not the signal itself.

- **Appearance:** the zone shape's boundary line — color-coded, with weight and/or dash pattern distinguishing states so the signal survives never-color-alone even before a viewer reads the color (design-principles.md §3). Never the whole shape recolored — the fill is heat's job, not tag's.
- **States, at neighborhood zoom and closer:**
  - **Local** — plain stroke, plus the word "Local" at the centroid (neighborhood zoom only).
  - **Tourist** — plain stroke, same weight as Local, different color; plus the word "Tourist" (neighborhood zoom only).
  - **Tourist + busy** (heat crosses the "busy" threshold for the zone's current slider hour) — the stroke switches to a distinct warning form (different weight or dash, not color alone) and the label reflects it. **This replaces the plain Tourist stroke outright — one treatment, never two stacked**, the same rule the badge version had.
  - **Local + busy** — no warning treatment, ever. Renders exactly like plain Local. The absence of a warning here is what makes the warning meaningful on the Tourist side (design-principles.md §2, Von Restorff: only one "special" element per view).
  - **Mix** — **no stroke, no label,** at any zoom. Blank is the visual encoding for Mix; it's the unmarked, most-common middle value, and marking it would be clutter with no information in it.
  - **Not yet curated** — also **unstroked**, visually identical to Mix. Deliberate trade-off, not a gap: the map doesn't pre-announce "no data here," the same way heat doesn't pre-announce "nothing relevant at this hour" (`ux-flows.md` Journey 2's unhappy path) — tapping in resolves it via the zone sheet's existing empty state.
- **At city-wide zoom specifically, only Local zones get the stroke.** **[design call]** Tourist stays unstroked at this zoom too, not just Mix — extending the existing Mix-is-silent discipline one level further rather than carving out an exception. Two reasons: first, legibility — a handful of green pockets across the city is a glance; a fully outlined city in two colors is a map you have to parse. Second, coherence with what "busy" even means — heat itself is only coarse "neighborhood-scale blobs" at city-wide (§2), not the zone-level precision "busy" needs, so the busy+Tourist warning has no real city-wide granularity to attach to anyway; it's a neighborhood-zoom-and-closer construct by nature, not a rule being suppressed. City-wide becomes a map of where to trust, not a map of everything — consistent with the north star's actual question ("where's actually local"), not a liability map.
- **Zone-level tag is its own curated/algorithmic value**, not an aggregate of the zone's spots. Decision #12 already treats neighborhood and spot as separate granularities of curated data — this spec doesn't invent an aggregation function on top of that; the stroke just displays the neighborhood-level value directly.
- **Density bound:** decision #12 keeps Tel Aviv at dozens of neighborhoods total. Strokes at city scale read as a handful of legible outlines, not thousands of hairlines — the same bound that made neighborhood-zoom badges legible applies here too, and a stroke is cheaper to render at scale than a badge ever was.

---

## 4. Spot pins (close zoom)

- **No tag encoding of any kind** — not a badge, not a colored fill, not a shaped outline that varies by tag. This was an open call in `ux-flows.md` §6 and it's resolved here as **no, never**: even a tag-colored pin shape still asks the eye to individually parse every pin in a dense block, which is the exact failure mode Aviran flagged. Tag lives in the spot sheet as a word, full stop.
- **What a pin does carry:** a shape/icon that encodes **category** (Food & drinks vs. Things to do) — e.g., a fork-and-knife glyph vs. a generic landmark glyph — so that with both categories showing at once (the default), a user can tell them apart without relying on color alone (design-principles.md §3, §5).
- **This got more load-bearing, not less, after decision #25.** With category chips off the map and into the search sheet, both categories are mixed together on the base map at all times outside of a deliberate search session — there's no lightweight way to pre-filter to just one category while casually browsing anymore. The pin's category glyph is now the *only* way to visually tell categories apart during ordinary browsing, not a nice-to-have alongside a chip-filtered view. Get this shape/icon distinction wrong and there's no fallback for the common case.
- **Touch target:** ≥44pt regardless of how small the glyph renders visually (design-principles.md §2, Fitts's Law) — the tappable area is never just the drawn glyph's bounding box if that's smaller than 44pt.
- **Tap behavior:** unchanged from `ux-flows.md` — opens the spot sheet directly. A pin is never a two-step disclosure (no "tap once to preview, tap again to open").
- **Why the personal-place ring in §6 doesn't reopen this rule.** Decision #26 puts a marker back on pins — a ring for places in the viewer's own Places list. This isn't the same risk tag-per-pin was, because the two scale completely differently: tag would have needed a distinction on *every* pin in view, unbounded by anything except how many spots exist in the dataset. The personal-place ring only ever applies to the handful of pins a specific person has actually saved, visited, or dwelled at — bounded by one person's own history, not by the city's spot count. A crowded block still shows zero tag signal on its pins; it might show one or two personal rings, because that's genuinely all there are.

---

## 5. Pin clustering

Unspecified anywhere until now, and load-bearing for exactly this problem — clustering is what keeps close zoom usable once pin density (not tag density) gets high on its own.

- **Rule:** pins within a fixed **screen-distance threshold** (points, not real-world meters — so clustering behavior is consistent regardless of zoom-implied real-world scale) merge into a single cluster marker.
- **Cluster marker appearance:** a plain circular badge with a count (e.g., "12"). **Neutral styling — never heat- or tag-colored.** A cluster is a rendering convenience representing an ambiguous mix of underlying spots, not a data signal; coloring it would imply a meaning (a dominant tag, an average heat) this spec deliberately avoids computing or claiming.
- **Tap behavior:** tapping a cluster **zooms and recenters the map on it** — it never opens a sheet directly, since a cluster doesn't represent one place. As the user zooms further, clusters break apart automatically, converging on individual pins once spacing exceeds the threshold.
- **The neighborhood button (`ux-flows.md` §2) is the other way to beat density** — a user doesn't have to wait for pins to fully declutter to see everything in an area; the button's zone sheet lists every tagged spot regardless of how tightly its pins are clustered on the map at that moment. Clustering and the button solve the same underlying problem (too much at once) from two different angles — one keeps the map itself legible, the other gives a full-list escape hatch.
- **Category-chip results cluster identically to text-query results.** Since decision #25 makes tapping a category chip inside the search sheet produce the same kind of result set a typed query does (`ux-flows.md` §6), a "Things to do" result set that's still dense at the current zoom clusters exactly the same way an unfiltered view would — clustering doesn't get a separate ruleset for a search-driven subset of pins.
- **Clusters stay neutral even when they contain a personal place.** No exception for "this cluster has one of yours inside" — that would mean computing and rendering a fourth kind of cluster state on top of the plain count, the same instinct that made tag-per-pin a problem in the first place. She'll see the ring once she zooms enough for the cluster to resolve, or she can reach the same place instantly through the Places list (§6 below) without waiting on the map to declutter — the list is already the fast path, the same role it plays for zone density via the neighborhood button.

---

## 6. Personal places on the map

Decision #26: Saved and Visited merge into one list — called **Places** (`ux-flows.md` §2) — fed by manual save, auto-save (dwell 20+ minutes), and geofence detection, and it renders on the map, not only as a list.

- **What renders:** a **ring accent** around the existing pin, at close zoom only, wherever that pin belongs to a place already in the viewer's Places list. Not a new pin, not a badge riding beside it — an accent on the marker that would already be there.
- **Binary, not provenance-differentiated.** The ring shows "this is in your Places" or it doesn't — it does **not** distinguish manually-**Saved** from dwell-triggered **Been** (renamed from "auto-saved" 2026-07-30, decision #30, same mechanic) from merely-**Visited**. That distinction lives in the Places list itself (`ux-flows.md` §2, §4), where there's room for a word — decision #30's requirement that Saved and Been read as visually/functionally distinct is satisfied there, by the provenance word, not by adding a second map accent here. Encoding three states on a map accent is exactly the instinct that turned tag into a density problem; the map gets a yes/no, the list gets the nuance.
- **Color:** reuses the same accent already used for the save icon's filled state in a spot sheet, rather than inventing a new hue that would need its own legend entry — "this pin is yours" reads as the same color as "you saved this," everywhere in the product.
- **Zoom scope, deliberately narrow.** Close zoom only, same as where pins themselves exist. **[design call]** No equivalent mark at neighborhood zoom (e.g., "this zone contains one of your places") — neighborhood zoom already carries heat fill, tag stroke, and the tag word label; adding a fourth thing there on the theory that it's usually sparse is the same reasoning that produced the original density problem. The cost of this restraint: she won't see at a glance, zoomed out, that a zone holds one of her places — she'll find out by opening that zone's sheet, opening the Places list directly, or zooming to close. All three already exist; nothing new needs building to cover the gap.
- **Touch target unaffected:** the ring sits around the existing pin's tap target, never shrinking it below the 44pt minimum in §4.

---

## 7. Accessibility

Design-principles.md §3 and §5: never rely on color alone, and every map annotation needs a VoiceOver label. Two things in this spec create real accessibility gaps that the visual design alone doesn't solve, and this section resolves both.

- **The Mix-is-silent problem.** A sighted user reads "no stroke" as Mix (§3 above) — but VoiceOver can't read an absence. If a zone's accessibility label simply omits any mention of tag when there's no visual stroke, a VoiceOver user gets *nothing*, not "Mix." **Resolution:** a zone's accessibility label always states its tag explicitly in speech, regardless of whether anything renders visually — "Florentin, busy, Mix" or "Florentin, quiet, Local." This means VoiceOver output is strictly more precise than the visual layer in this one respect, which is the right direction for a gap to run (more information for a user who can't see the map, not less). Unaffected by the badge-to-stroke change — this was always about the accessibility tree, never about which visual channel carried the signal.
- **The unrated-vs-Mix problem, resolved the same way.** Since VoiceOver doesn't suffer the same "clutter" pressure that justifies staying silent on the map surface, a genuinely not-yet-curated zone's accessibility label can say so directly — "Florentin, busy, no local rating yet" — rather than reading identically to Mix the way it deliberately does for sighted users. VoiceOver users get a distinction the visual design intentionally declines to make.
- **The busy + Tourist warning** needs its own explicit label, separate from the plain Tourist label it replaces — e.g., "Florentin, busy and touristy, worth a second look" — rather than expecting VoiceOver to read heat and tag as two separate announcements and leaving the user to infer the combination (this is `ux-flows.md` §9's Q5, kept coherent with this resolution rather than answered twice).
- **Cluster markers** announce a count and a rough area, not individual spot names — "12 places near Rothschild Boulevard" — since the underlying spots aren't individually meaningful until the cluster resolves. Never announces whether a personal place is inside (§6) — the same restraint as the visual rule.
- **Pins** announce name and category ("Port Said, Food & drinks") — never tag, since a pin never carries tag visually either; tag is available once the spot sheet opens, same as for sighted users.
- **Personal-place pins (§6)** append one clause — "Port Said, Food & drinks, in your Places" — rather than requiring a separate gesture or menu to discover that a pin is already saved.

---

## 8. Explicitly out of scope

Hex grids, fog-of-war / reveal-as-you-walk, and friend leaderboards are not addressed anywhere above and shouldn't be inferred from anything here. The zoom-based disclosure in §2 is a standard cartographic pattern (the same thing any map app does as you zoom in) — it is not an exploration or reveal mechanic tied to where a user has physically been, and nothing in this spec persists per-user map state. `SALVAGE.md` marks fog-of-war BURN and decision #12 already rules out hex granularity by name; this spec doesn't reopen either.
