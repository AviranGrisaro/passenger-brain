---
name: ui-design-review
description: Review UI code against design principles, or apply design taste when building interfaces. Use when building, reviewing, or improving any frontend UI — components, pages, layouts, forms, navigation. References the comprehensive UI/UX Design Principles manual.
disable-model-invocation: false
user-invocable: true
---

## Quick Start

```
/ui-design-review                → Review current UI changes against design principles
/ui-design-review <file>         → Review a specific component/page
/ui-design-review checklist      → Run the full anti-pattern checklist
/ui-design-review guide <topic>  → Get specific guidance (e.g., "buttons", "forms", "colors", "spacing")
```

## Source Reference

All rules come from the **UI/UX Design Principles for AI Agents** manual, vendored in-repo at:
`passenger-brain/design/reference/ui-ux-design-principles-manual.md`
(path is relative to the workspace root; this replaced a stale hardcoded home-dir path that no longer resolved.)

Read the relevant chapter(s) from this file before giving guidance. The manual has 15 chapters — use the Quick Lookup below to find the right one.

**For Passenger (native iOS) work, read the platform-adapted quick-reference first:**
`passenger-brain/design/design-principles.md` — the same laws translated into SwiftUI/HIG terms (Dynamic Type instead of px scales, semantic color sets instead of HSL hex, thumb-zone/44pt targets, VoiceOver on map annotations). Fall back to the full manual above for depth on any chapter.

## Quick Lookup

| Topic | Chapter | Key Rules |
|-------|---------|-----------|
| Element importance, layout | Ch 3: Visual Hierarchy & Layout | 3-tier importance, grayscale-first, axis of interaction |
| Fonts, sizes, text spacing | Ch 4: Typography System | Type scale, line length 45-75ch, line-height |
| Color palette, contrast | Ch 5: Color System | HSL, 9 shades per color, 4.5:1 contrast |
| Spacing, shadows, depth | Ch 6: Spacing & Depth | 16px base scale, 5 shadow levels, owl selector |
| UI components | Ch 7: Component Patterns | Button hierarchy, cards, modals, tables, badges |
| Navigation, IA | Ch 8: Navigation & IA | 5-7 nav items, LATCH, trunk test |
| Cognitive load, attention | Ch 9: Cognitive Load | Hick's Law, <400ms response, progressive disclosure |
| Engagement, microinteractions | Ch 10: Interaction & Feedback | Hook cycle, feedback hierarchy, signature moments |
| Persuasion, trust | Ch 11: Persuasion & Trust | Cialdini's 6, social proof, dark pattern audit |
| Forms, inputs, errors | Ch 12: Form Design | One-column, validate on blur, Poka-Yoke |
| Responsive, mobile | Ch 13: Responsive Design | Mobile-first, breakpoints, thumb zone |
| Accessibility | Ch 14: Accessibility | WCAG AA, keyboard nav, screen readers |
| Anti-patterns | Ch 15: Anti-Pattern Catalog | 35+ categorized mistakes with corrections |

## How to Use This Skill

### When BUILDING UI (proactive mode)

Before writing any UI code, internalize these critical values:

**Typography**
- Type scale: 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72px — no arbitrary sizes
- Body: 16px min, line-height 1.5, max-width 45-75 characters
- Headlines: line-height 1-1.25, letter-spacing -0.01 to -0.03em
- Weight: 400-500 body, 600-700 headings, never below 400

**Colors**
- Body text: #222-#333 (never pure #000)
- Background: #f5f5f5-#eee (never pure #fff)
- Text contrast: 4.5:1 normal, 3:1 large (18px+)
- 9 shades per color (100-900), greys have slight saturation
- Never color-only meaning — always pair with icon/text

**Spacing (base 16px)**
- Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px
- Start with too much whitespace, then reduce
- Labels closer to their content than adjacent elements
- Between-group spacing >= 2x within-group spacing

**Components**
- Buttons: 1 primary (solid) per view, outline secondary, text tertiary
- Cards: shadow OR border, not both. border-radius: 8-12px
- Inputs: consistent style, labels above, validate on blur
- Modals: overlay 50% black, max-width 500px, focus trap, Escape closes
- Tables: zebra OR bottom borders, not both. Left-align text, right-align numbers
- Badges: pill shape, soft/tinted background, 12px font
- Empty states: illustration + description + CTA, hide filters

**Layout**
- 3-tier hierarchy: Primary (#111827, 600-700 weight), Secondary (#4B5563, 400-500), Tertiary (#9CA3AF, 400)
- Design in grayscale first, add color after hierarchy works
- Max content width: 600-800px text, 400-500px forms
- Don't fill the whole screen — give elements their natural width

**Interaction**
- Response < 400ms (Doherty threshold)
- 3-5 options per decision (Hick's Law)
- Progressive disclosure: show 80% use case first
- Undo over confirmation dialogs
- Touch targets: 44-48px mobile, 32px desktop

**Accessibility**
- `<html lang="en">` always
- Semantic HTML first (`<nav>`, `<main>`, `<button>`, etc.)
- Visible focus states (background-color, not thin outline)
- Never disable pinch-to-zoom
- `prefers-reduced-motion` respected
- Skip navigation link

### When REVIEWING UI (review mode)

Read the file(s) being reviewed, then check against these categories:

1. **Visual Hierarchy** — Are there 3 clear tiers? Does it work in grayscale?
2. **Typography** — Sizes from the scale? Line length constrained? Proper weights?
3. **Color** — Contrast passing? No color-only meaning? Near-black on near-white?
4. **Spacing** — Values from the scale? Labels close to content? Enough whitespace?
5. **Components** — Following the correct patterns? Only 1 primary button?
6. **Navigation** — Current location indicated? 5-7 items? Descriptive link text?
7. **Forms** — Single column? Labels above? Validate on blur? Smart defaults?
8. **Responsiveness** — Mobile-first? Thumb zone? Touch targets sized?
9. **Accessibility** — Semantic HTML? Focus states? Alt text? Keyboard navigable?
10. **Anti-patterns** — Check against Ch 15 catalog

### Output Format

For reviews, output:

```
## UI Design Review: [Component/Page Name]

### Passes
- [What's done well, referencing specific principles]

### Issues
1. **[Category]**: [What's wrong] → [What to do instead] (Ch X reference)
2. ...

### Quick Wins
- [Easy fixes that would have the biggest impact]
```

For guidance, output the relevant rules with specific values — no vague advice. Every recommendation must include a concrete number, CSS value, or testable criterion.

## Key Decision Trees

### Which Button Style?
- Primary action on screen? → Solid/filled with brand color (max 1 per view)
- Secondary action? → Outline/ghost button
- Tertiary/cancel? → Text-only link style

### How Many Options to Show?
- 1-5 → Show all, highlight recommended
- 6-12 → Group into 2-3 categories
- 13-30 → Show top 5 + "Show more"
- 30+ → Search + categorized browse

### How to Handle Errors?
- Preventable by system? → Prevent it (constrained controls, smart defaults)
- Slip (right goal, wrong action)? → Make similar actions distinct, add undo
- Mistake (wrong goal)? → Better feedback, show system state, undo
- User blocked? → Full-screen: what happened + why + how to recover
- User not blocked? → Toast with undo, auto-dismiss 5s

### What Shadow Level?
- Buttons/inputs → xs: `0 1px 2px rgba(0,0,0,0.05)`
- Cards/sections → sm: `0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)`
- Dropdowns/popovers → md: `0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06)`
- Modals/dialogs → lg: `0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)`
- Notifications/toasts → xl: `0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)`

## Tailwind CSS Mapping

Since the project uses Tailwind, here are the principle-to-Tailwind mappings:

| Principle | Tailwind Classes |
|-----------|-----------------|
| Primary text #111827 | `text-gray-900` |
| Secondary text #4B5563 | `text-gray-600` |
| Tertiary text #9CA3AF | `text-gray-400` |
| Body text #222-#333 | `text-gray-800` or `text-gray-900` |
| Near-white bg | `bg-gray-50` or `bg-gray-100` |
| Spacing scale | `p-1`(4) `p-2`(8) `p-3`(12) `p-4`(16) `p-6`(24) `p-8`(32) `p-12`(48) `p-16`(64) |
| Shadow xs | `shadow-sm` |
| Shadow sm | `shadow` |
| Shadow md | `shadow-md` |
| Shadow lg | `shadow-lg` |
| Shadow xl | `shadow-xl` |
| Card radius | `rounded-lg` (8px) or `rounded-xl` (12px) |
| Badge pill | `rounded-full` |
| Max text width | `max-w-prose` (~65ch) |
| Type scale | `text-xs`(12) `text-sm`(14) `text-base`(16) `text-lg`(18) `text-xl`(20) `text-2xl`(24) `text-3xl`(30) `text-4xl`(36) |

## Anti-Pattern Quick Check (Pre-Ship)

Before shipping, verify NONE of these are present:

- [ ] Equal visual weight on all elements (no 3-tier hierarchy)
- [ ] Pure #000 text or pure #fff background
- [ ] Scaled-up small icons (use container instead)
- [ ] Color-only meaning (no icon/text supplement)
- [ ] Multi-column forms (except name/address pairs)
- [ ] Placeholder-only labels (labels must persist)
- [ ] Validate on keystroke (should be on blur)
- [ ] "Click here" link text
- [ ] More than 1 primary button per view
- [ ] Card with both border AND shadow
- [ ] Missing focus states on interactive elements
- [ ] `outline: none` without replacement focus style
- [ ] Walls of text without visual entry points
- [ ] Confirmation dialog as only safety net (prefer undo)
- [ ] Desktop-first responsive approach

---

## Surface Classifier (run FIRST before any review)

Decide which rule set applies before evaluating anything. Product OS is mostly App UI; Passenger marketing pages and PRD HTML exports are Landing.

- **MARKETING / LANDING** (hero-driven, brand-forward, conversion-focused) → Landing Page Rules below
- **APP UI** (workspace-driven, data-dense, task-focused: dashboards, admin, settings, internal tools — including Product OS) → App UI Rules below
- **HYBRID** (marketing shell with app-like sections) → Landing rules to hero/marketing, App UI rules to functional sections

### Hard Rejection Criteria (instant-fail — flag if ANY apply)

1. Generic SaaS card grid as first impression
2. Beautiful image with weak brand
3. Strong headline with no clear action
4. Busy imagery behind text
5. Sections repeating the same mood statement
6. Carousel with no narrative purpose
7. App UI made of stacked cards instead of layout

### Litmus Checks (answer YES / NO — score consensus across reviewers)

1. Brand/product unmistakable in first screen?
2. One strong visual anchor present?
3. Page understandable by scanning headlines only?
4. Each section has one job?
5. Are cards actually necessary?
6. Does motion improve hierarchy or atmosphere?
7. Would design feel premium with all decorative shadows removed?

### Landing Page Rules (apply when MARKETING/LANDING)

- First viewport reads as one composition, not a dashboard
- Brand-first hierarchy: brand > headline > body > CTA
- Typography: expressive, purposeful — no default stacks (Inter, Roboto, Arial, system)
- No flat single-color backgrounds — use gradients, images, subtle patterns
- Hero: full-bleed, edge-to-edge, no inset/tiled/rounded variants
- Hero budget: brand, one headline, one supporting sentence, one CTA group, one image
- No cards in hero. Cards only when card IS the interaction
- One job per section: one purpose, one headline, one short supporting sentence
- Motion: 2-3 intentional motions minimum (entrance, scroll-linked, hover/reveal)
- Color: define CSS variables, avoid purple-on-white defaults, one accent color
- Copy: product language not design commentary. "If deleting 30% improves it, keep deleting."

### App UI Rules (apply when APP UI — default for Product OS)

- **Calm surface hierarchy, strong typography, few colors**
- Dense but readable, minimal chrome
- Organize: primary workspace, navigation, secondary context, one accent
- **Avoid: dashboard-card mosaics, thick borders, decorative gradients, ornamental icons**
- Copy: utility language — orientation, status, action. Not mood / brand / aspiration.
- **Cards only when the card IS the interaction.** Information that's read, not clicked, doesn't need a card.
- Section headings state what the area is or what the user can do ("Selected KPIs", "Plan status") — never marketing-style mood headers
- Density beats decoration: real product data > generated card patterns

### Universal Rules (apply to all surfaces)

- Define CSS variables for color system (Tailwind tokens count)
- No default font stacks (Inter, Roboto, Arial, system) as the PRIMARY display/body font
- One job per section
- "If deleting 30% of the copy improves it, keep deleting"
- Cards earn their existence — no decorative card grids
- NEVER body text < 16px or contrast ratio < 4.5:1 on body text
- NEVER labels-inside-fields as the only label (placeholder-as-label)
- ALWAYS preserve visited vs unvisited link distinction
- NEVER float headings between paragraphs — heading must sit closer to the section it introduces than to the preceding section

---

## AI Slop Blacklist (the 11 patterns that scream "AI-generated")

Cross-check every new UI surface against this list. Flag any match as a high-severity finding — these are the patterns that immediately read as "Claude wrote this." Aviran's Product OS dashboard is App UI; most of these are death sentences for it.

1. **Purple / violet / indigo gradient backgrounds** or blue-to-purple color schemes
2. **The 3-column feature grid:** icon-in-colored-circle + bold title + 2-line description, repeated 3x symmetrically. THE most recognizable AI layout — if you see it, kill it.
3. Icons in colored circles as section decoration (SaaS starter template look)
4. Centered everything (`text-align: center` on all headings, descriptions, cards)
5. Uniform bubbly border-radius on every element (same large radius on everything)
6. Decorative blobs, floating circles, wavy SVG dividers (if a section feels empty, it needs better content, not decoration)
7. Emoji as design elements (rockets in headings, emoji as bullet points, sparkles next to "AI-powered")
8. Colored left-border on cards (`border-left: 3px solid <accent>`)
9. Generic hero copy ("Welcome to [X]", "Unlock the power of...", "Your all-in-one solution for...")
10. Cookie-cutter section rhythm (hero → 3 features → testimonials → pricing → CTA, every section same height)
11. `system-ui` or `-apple-system` as the PRIMARY display/body font — the "I gave up on typography" signal. Pick a real typeface.

### How to apply

- Run before merging any UI PR. One match = ask before proceeding. Two+ matches = redesign before merging.
- The 3-column-feature-grid pattern is the highest-precision detector. If a screen has it, it's almost certainly AI slop regardless of polish.
- "This feels off" is not a finding — name the specific blacklist item or the Universal Rule being broken. Taste is debuggable, not subjective.

Source: gstack `/design-review` (`design-review/SKILL.md:1586-1656`) + OpenAI "Designing Delightful Frontends with GPT-5.4" + the App UI rule set adapted for Product OS.
