# Passenger V1 — Map Rendering Spec

**Owner:** designer (drafted for Aviran)
**Date:** 2026-07-27
**Status:** Draft — awaiting Aviran's read
**Source:** `strategy/decisions.md` #12 (neighborhood + spot granularity), #17 (no gradients), #18 (three vibe tags) + `design/design-principles.md` §2/§3/§5 + Aviran's direct pushback on tag-layer density, relayed 2026-07-27.
**Relationship to `design/ux-flows.md`:** §6 of that doc states the structural rules this spec implements — tag renders progressively by zoom, Mix is silent, the busy+Tourist warning replaces rather than stacks. This doc is the rendering detail underneath those rules: what's actually drawn, how pins cluster, and the exact accessibility labels. Read §6 first for the *why*; this doc is the *how*. No PRD exists yet to trace against, and this doc doesn't need its own high-fidelity mockup — it's a rendering-rules reference for whoever builds the map layer, not a flow a reviewer clicks through.

---

## 1. Why this doc exists

Aviran's pushback, verbatim: *"how do you show tag layer on every location on the map? its gonna be too much information on one layer."* The original design badged every close-zoom pin with a tag, then stacked a warning badge on top of that for the worst case — heat fill + tag badge + warning badge, once per pin, in a neighborhood that might have forty pins on screen at once. That doesn't survive contact with Florentin at 8pm. This spec is the rendering-level fix: tag gets the same progressive disclosure heat already has, and spot-level tag comes off the map surface entirely.

---

## 2. What renders at each zoom

| Zoom | Heat | Tag | Pins |
|---|---|---|---|
| **City-wide** | Neighborhood-scale blobs, stepped bands | None | None |
| **Neighborhood** | Zone-level stepped-band fill | **One badge per zone**, anchored at the zone's centroid | None |
| **Close** | Area-level fill, unchanged from neighborhood zoom | **None** — tag never renders on a pin, at any zoom | Individual markers, category only |

Heat and tag never share a visual channel, at any zoom: heat is always the area/fill treatment; tag, where it renders at all, is always a discrete badge sitting on top of that fill, independent of its hue (design-principles.md §3 — never rely on color alone).

---

## 3. Zone badge (neighborhood zoom)

- **Appearance:** small badge, anchored at the zone's centroid or label point — not the whole shape recolored, since the shape's fill is already doing heat's job.
- **States:**
  - **Local** — plain badge, the tag's normal treatment.
  - **Tourist** — plain badge, same visual weight as Local, different color/label.
  - **Tourist + busy** (heat crosses the "busy" threshold for the zone's current slider hour) — the badge switches to a distinct warning form. **This replaces the plain Tourist badge outright — one element, never two stacked.**
  - **Local + busy** — no warning treatment, ever. Renders exactly like plain Local. The absence of a warning here is what makes the warning meaningful on the Tourist side (design-principles.md §2, Von Restorff: only one "special" element per view).
  - **Mix** — **no badge.** Blank is the visual encoding for Mix; it's the unmarked, most-common middle value, and marking it would be clutter with no information in it.
  - **Not yet curated** — also **no badge**, visually identical to Mix on the map. This is a deliberate trade-off, not a gap: the map surface doesn't try to pre-announce "no data here," the same way heat doesn't pre-announce "nothing relevant at this hour" (`ux-flows.md` Journey 2's unhappy path) — tapping in resolves it, via the zone sheet's existing empty state.
- **Zone-level tag is its own curated/algorithmic value**, not an aggregate of the zone's spots. Decision #12 already treats neighborhood and spot as separate granularities of curated data — this spec doesn't invent an aggregation function on top of that; the badge just displays the neighborhood-level value directly.
- **Density bound:** decision #12 keeps Tel Aviv at dozens of neighborhoods total, and any single viewport at neighborhood zoom shows a handful of them at once — a legible badge count by construction, not something this spec needs to additionally cap or cluster.

---

## 4. Spot pins (close zoom)

- **No tag encoding of any kind** — not a badge, not a colored fill, not a shaped outline that varies by tag. This was an open call in `ux-flows.md` §6 and it's resolved here as **no, never**: even a tag-colored pin shape still asks the eye to individually parse every pin in a dense block, which is the exact failure mode Aviran flagged. Tag lives in the spot sheet as a word, full stop.
- **What a pin does carry:** a shape/icon that encodes **category** (Food & drinks vs. Things to do) — e.g., a fork-and-knife glyph vs. a generic landmark glyph — so that with both categories showing at once (the default), a user can tell them apart without relying on color alone (design-principles.md §3, §5).
- **Touch target:** ≥44pt regardless of how small the glyph renders visually (design-principles.md §2, Fitts's Law) — the tappable area is never just the drawn glyph's bounding box if that's smaller than 44pt.
- **Tap behavior:** unchanged from `ux-flows.md` — opens the spot sheet directly. A pin is never a two-step disclosure (no "tap once to preview, tap again to open").

---

## 5. Pin clustering

Unspecified anywhere until now, and load-bearing for exactly this problem — clustering is what keeps close zoom usable once pin density (not tag density) gets high on its own.

- **Rule:** pins within a fixed **screen-distance threshold** (points, not real-world meters — so clustering behavior is consistent regardless of zoom-implied real-world scale) merge into a single cluster marker.
- **Cluster marker appearance:** a plain circular badge with a count (e.g., "12"). **Neutral styling — never heat- or tag-colored.** A cluster is a rendering convenience representing an ambiguous mix of underlying spots, not a data signal; coloring it would imply a meaning (a dominant tag, an average heat) this spec deliberately avoids computing or claiming.
- **Tap behavior:** tapping a cluster **zooms and recenters the map on it** — it never opens a sheet directly, since a cluster doesn't represent one place. As the user zooms further, clusters break apart automatically, converging on individual pins once spacing exceeds the threshold.
- **The neighborhood button (`ux-flows.md` §2) is the other way to beat density** — a user doesn't have to wait for pins to fully declutter to see everything in an area; the button's zone sheet lists every tagged spot regardless of how tightly its pins are clustered on the map at that moment. Clustering and the button solve the same underlying problem (too much at once) from two different angles — one keeps the map itself legible, the other gives a full-list escape hatch.

---

## 6. Accessibility

Design-principles.md §3 and §5: never rely on color alone, and every map annotation needs a VoiceOver label. Two things in this spec create real accessibility gaps that the visual design alone doesn't solve, and this section resolves both.

- **The Mix-is-silent problem.** A sighted user reads "no badge" as Mix (§3 above) — but VoiceOver can't read an absence. If a zone's accessibility label simply omits any mention of tag when there's no visual badge, a VoiceOver user gets *nothing*, not "Mix." **Resolution:** a zone's accessibility label always states its tag explicitly in speech, regardless of whether anything renders visually — "Florentin, busy, Mix" or "Florentin, quiet, Local." This means VoiceOver output is strictly more precise than the visual layer in this one respect, which is the right direction for a gap to run (more information for a user who can't see the map, not less).
- **The unrated-vs-Mix problem, resolved the same way.** Since VoiceOver doesn't suffer the same "clutter" pressure that justifies staying silent on the map surface, a genuinely not-yet-curated zone's accessibility label can say so directly — "Florentin, busy, no local rating yet" — rather than reading identically to Mix the way it deliberately does for sighted users. VoiceOver users get a distinction the visual design intentionally declines to make.
- **The busy + Tourist warning badge** needs its own explicit label, separate from the plain Tourist label it replaces — e.g., "Florentin, busy and touristy, worth a second look" — rather than expecting VoiceOver to read heat and tag as two separate announcements and leaving the user to infer the combination (this is `ux-flows.md` §9's Q5, kept coherent with this resolution rather than answered twice).
- **Cluster markers** announce a count and a rough area, not individual spot names — "12 places near Rothschild Boulevard" — since the underlying spots aren't individually meaningful until the cluster resolves.
- **Pins** announce name and category ("Port Said, Food & drinks") — never tag, since a pin never carries tag visually either; tag is available once the spot sheet opens, same as for sighted users.

---

## 7. Explicitly out of scope

Hex grids, fog-of-war / reveal-as-you-walk, and friend leaderboards are not addressed anywhere above and shouldn't be inferred from anything here. The zoom-based disclosure in §2 is a standard cartographic pattern (the same thing any map app does as you zoom in) — it is not an exploration or reveal mechanic tied to where a user has physically been, and nothing in this spec persists per-user map state. `SALVAGE.md` marks fog-of-war BURN and decision #12 already rules out hex granularity by name; this spec doesn't reopen either.
