# Chapter 1: How to Use This Book

This is a reference manual for AI agents building web and mobile user interfaces. Every chapter is a self-contained module of concrete, actionable rules — read any chapter independently without needing context from others.

---

## What This Book Is

A systematic collection of UI/UX design rules with specific thresholds, values, and anti-patterns. This is not a design philosophy book. It is an instruction set. Each rule tells you exactly what to do, when to do it, and what to avoid.

The rules are derived from established design systems, accessibility standards, and production-tested patterns. They prioritize correctness and usability over novelty.

---

## How to Use It

**Each chapter is independent.** You do not need to read chapters in order. Jump to the chapter that matches your current task. If a concept from another chapter is relevant, it is briefly restated in context — no cross-referencing required.

**Each rule follows a consistent format:**

```
### Rule: [Name]

**When:** The condition or context that triggers this rule.
**Do:** The specific action to take.
**Values:** Concrete numbers, measurements, or thresholds.
**Don't:** The anti-pattern to avoid.
```

- **When** defines scope. A rule only applies when its condition is met.
- **Do** is the directive. It uses imperative language with no hedging.
- **Values** are specific. "Use 16px" not "use an appropriate size."
- **Don't** is the failure mode. It describes what happens when the rule is ignored.

---

## Conventions

**Priority Levels:**
- **Critical** — Violating this rule causes usability failures or accessibility violations.
- **Recommended** — Following this rule produces measurably better interfaces.
- **Optional** — Context-dependent; apply when it fits.

**Platform Notation:**
- **Web** — Browser-based interfaces (HTML/CSS/JS frameworks).
- **iOS** — Native or hybrid iOS applications.
- **Android** — Native or hybrid Android applications.
- **All** — Applies to every platform.

**Measurement Units:**
- Use `px` for absolute values in web contexts.
- Use `pt` for iOS, `dp` for Android.
- Conversion: 1pt = 1dp = 1px at 1x density.

---

## Quick Lookup

| If you need to... | Go to |
|---|---|
| Decide element importance and layout structure | Chapter 3: Visual Hierarchy & Layout |
| Choose fonts, sizes, and text spacing | Chapter 4: Typography System |
| Build a color palette with proper contrast | Chapter 5: Color System |
| Apply spacing, shadows, and depth | Chapter 6: Spacing & Depth |
| Implement specific UI components | Chapter 7: Component Patterns |
| Choose between design approaches for a scenario | Chapter 2: Decision Matrix |
| Handle responsive layout and images | Chapter 8: Responsive Design |
| Handle interaction states and feedback | Chapter 9: Interaction & Feedback |
| Meet accessibility requirements | Chapter 10: Accessibility |
| Apply platform-specific conventions | Chapter 11: Platform-Specific Patterns |
| Optimize performance perception | Chapter 12: Performance & Perceived Speed |

---

## Key Principle

Every rule in this book is falsifiable. If a rule says "use 16px base font size," you can verify whether your implementation uses 16px. Vague guidance like "make it readable" does not appear here. When you apply a rule, you should be able to check a specific value, ratio, or structural property to confirm compliance.

Start with the chapter that matches your immediate task. Apply rules in order within each chapter — they are sequenced from foundational to specific.

---
---

---

---

---

---

# Chapter 2: Quick Reference — Decision Matrix

Use this chapter as a lookup table. Find your current task, then jump to the chapter and rule that applies.

---

## Master Decision Matrix

| I need to... | Chapter | Key Rule | Critical Value |
|-------------|---------|----------|----------------|
| Establish visual importance | Ch 3 | Assign primary/secondary/tertiary | 2-3 colors, 2 font weights |
| Align asymmetric elements | Ch 3 | Area Alignment | Align by visual weight, not edges |
| Place interactive elements | Ch 3 | Axis of Interaction | CTAs on visual alignment edges |
| Crop photos of people | Ch 3 | Face-ism Ratio | Face fills 60-80% for trust |
| Size text elements | Ch 4 | Type Scale | 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72px |
| Choose a font | Ch 4 | Font Selection | 5+ weights, system font stack as default |
| Set line length | Ch 4 | Line Length | 45-75 chars, 20-35em |
| Set root font size | Ch 4 | Relative Units at Root | `html { font-size: 100% }`, use rem throughout |
| Load web fonts | Ch 4 | Web Fonts as Enhancement | Async load, never render-blocking, 100-150KB budget |
| Check readability | Ch 4 | Content Readability | Flesch score 60+, grade level 8 or below |
| Build a color palette | Ch 5 | Three Categories | Primary + Neutrals + Supporting, 9 shades each |
| Check color contrast | Ch 5 | Contrast Requirements | 4.5:1 normal text, 3:1 large text (18px+) |
| Temper maximum contrast | Ch 5 | Near-Black on Near-White | Body text #222-#333, background #f5f5f5-#eee |
| Choose emotional tone | Ch 5 | Emotional Priming | Rounded + warm = friendly; sharp + cool = professional |
| Set spacing values | Ch 6 | Spacing System | Base 16px: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px |
| Space flow content | Ch 6 | Owl Selector | `* + * { margin-top: 1.5rem }` for content areas |
| Add depth/elevation | Ch 6 | Shadow System | 5 levels: small -> medium -> large |
| Design a button | Ch 7 | Button Hierarchy | Solid primary, outline secondary, text tertiary |
| Make elements feel clickable | Ch 7 | Affordances & Signifiers | Every interactive element needs a visible signifier |
| Build a component library | Ch 7 | Atomic Design Hierarchy | Atoms > Molecules > Organisms > Templates > Pages |
| Audit UI consistency | Ch 7 | Interface Inventory | Screenshot every component variant, group by type |
| Define product personality | Ch 7 | Design Persona | Brand traits as "X, but not Y" format |
| Create memorable interactions | Ch 7 | Signature Moments | 1-3 high-frequency interactions with extra polish |
| Design navigation | Ch 8 | Persistent Nav | Logo home, 5-7 items, search, utilities |
| Organize content | Ch 8 | Five Hat Racks (LATCH) | Category, Time, Location, Alphabet, Continuum |
| Optimize for user behavior | Ch 8 | Browsing vs Searching vs Discovery | Three layouts for three behaviors |
| Write UI text | Ch 8 | Omit Needless Words | Cut 50%, then cut 50% again |
| Build navigation markup | Ch 8 | List Markup in Nav | `<nav><ul><li>` for semantic structure |
| Reduce complexity | Ch 9 | Progressive Disclosure | 3-5 options visible, rest behind "Advanced" |
| Choose number of options | Ch 9 | Hick's Law | 3-5 per decision, max 7 before categorization |
| Set response time | Ch 9 | Doherty Threshold | < 400ms interactive, spinner at 400ms, progress at 1s+ |
| Make CTA stand out | Ch 9 | Von Restorff Effect | Unique color, 1.5x size of secondary actions |
| Show progress | Ch 9 | Zeigarnik Effect | Progress bar, 10-20% pre-filled start |
| Bridge intent to action | Ch 9 | Gulf of Execution | Match UI labels to user vocabulary |
| Design for skill levels | Ch 9 | Perpetual Intermediates | Optimize for intermediate users, the largest group |
| Prioritize design effort | Ch 9 | Maslow for Interfaces | Functional > Reliable > Usable > Pleasurable |
| Build engagement loop | Ch 10 | Hook Cycle | Trigger -> Action -> Variable Reward -> Investment |
| Design a microinteraction | Ch 10 | Microinteraction Architecture | Trigger > Rules > Feedback > Loops & Modes |
| Choose feedback channel | Ch 10 | Feedback Hierarchy | Visual (default) > Auditory > Haptic |
| Design notifications | Ch 10 | Trigger Strategy | 1 tap from trigger to core action |
| Build trust | Ch 11 | Authority + Reciprocity | Give before asking, display credentials |
| Add social proof | Ch 11 | Show Similar Others | Real user counts, segmented testimonials |
| Prime user perceptions | Ch 11 | Priming | Positive stimuli 1-3 steps before target action |
| Avoid dark patterns | Ch 11 | 13 Red Flags | See Anti-Pattern Catalog (Ch 15) |
| Design a form | Ch 12 | One-Column Layout | Top-aligned labels, inline validation on blur |
| Prevent form errors | Ch 12 | Poka-Yoke | Constrain inputs at control level, not validation |
| Set smart defaults | Ch 12 | Context-Aware Defaults | Correct for 80%+ of users using device/history/social data |
| Handle errors | Ch 12 | Slips vs Mistakes | Different solutions for wrong-action vs wrong-goal |
| Protect against catastrophe | Ch 12 | Forcing Functions | Interlocks, lock-ins, lock-outs scaled to severity |
| Size touch targets | Ch 12 | Fitts's Law | 48px recommended, 44px min mobile, 32px min desktop |
| Set breakpoints | Ch 13 | Breakpoint Scale | 640, 768, 1024, 1280, 1536px |
| Design for mobile | Ch 13 | Thumb Zone | Primary actions in bottom 1/3 of screen |
| Size containers for i18n | Ch 13 | Factor of Safety | 1.5x text containers, 50% button label growth |
| Set viewport meta | Ch 13 | Never Disable Zoom | `width=device-width, initial-scale=1.0` only |
| Match UI density to usage | Ch 13 | Posture-Based Design | Sovereign (dense), Transient (simple), Daemonic (quiet) |
| Check accessibility | Ch 14 | WCAG Checklist | Contrast, keyboard nav, screen reader, focus states |
| Set document language | Ch 14 | Language Declaration | `<html lang="en">`, BCP 47 tags |
| Style focus states | Ch 14 | Background Color Focus | Solid fill, not thin outline (GOV.UK pattern) |
| Hide content visually only | Ch 14 | Visually Hidden Class | `.visually-hidden` utility, never `display: none` |
| Audit accessibility | Ch 14 | Pattern-Based Auditing | Group by component, not WCAG principle |
| Avoid common mistakes | Ch 15 | Anti-Pattern Catalog | 35+ categorized anti-patterns with corrections |

---

## Measurement Reference

| Property | Value | Notes |
|----------|-------|-------|
| Base font size | 16px / 100% | Never below 16px for body; set root as `100%` not `16px` |
| Type scale | 12-14-16-18-20-24-30-36-48-60-72px | Hand-crafted, not modular ratio |
| Line height (body) | 1.5 | Up to 2 for wide content |
| Line height (headlines) | 1-1.2 | No extra spacing needed |
| Line length | 45-75 chars / 20-35em | Optimal reading width |
| Font weight (normal) | 400-500 | Most text |
| Font weight (emphasis) | 600-700 | Headlines, bold |
| Min font weight | 400 | Never below for UI text |
| Web font budget | 100-150KB total | Subset to needed character ranges |
| Readability score | Flesch 60+ | Grade 8 or below for general content |
| Spacing scale | 4-8-12-16-24-32-48-64-96-128px | Base 16, no two values < 25% apart |
| Flow content spacing | `* + * { margin-top: 1.5rem }` | Owl selector for content areas |
| Color shades per hue | 9 (labeled 100-900) | 500 = base |
| Hue rotation limit | 20-30 degrees max | Beyond this reads as different color |
| Contrast (normal text) | 4.5:1 | WCAG AA |
| Contrast (large text 18px+) | 3:1 | WCAG AA |
| Contrast (UI components) | 3:1 | Against adjacent colors |
| Body text color | #222-#333 | Near-black, not pure black |
| Background color | #f5f5f5-#eee | Near-white, not pure white |
| Touch target (mobile) | 44-48px | 48px recommended |
| Touch target (desktop) | 32px | Minimum |
| Nav items | 5-7 max | Primary navigation |
| Working memory | 4 +/- 1 items | Max visible groups |
| Hick's Law sweet spot | 3-5 options | Per decision point |
| Response time | < 400ms | Doherty threshold |
| Attention span | 7-10 minutes | Per segment |
| Search box width | 27 chars visible | Minimum |
| Breadcrumb separator | `>` | With 8px spacing |
| Shadow levels | 5 | Small -> Extra large |
| Angle distinction | 30 degrees min | For distinguishable diagonal elements |
| Text container buffer | 1.5x expected length | Factor of safety for content |
| Button label i18n buffer | 30-50% growth | For internationalization |
| Face-ism ratio (trust) | 60-80% face in frame | For testimonials, profiles |
| Trigger discoverability | 4 levels | Labeled > Icon > Hidden conventional > Hidden unconventional |
| Feedback timing | < 100ms | For direct manipulation |
| Surprise frequency | 1 per 20-50 interactions | Prevents habituation |
| Microinteraction channels | Visual > Auditory > Haptic | Routine: 1 channel; Critical: 2+ |
| Error prevention priority | Prevent > Detect > Recover | Poka-yoke principle |

---

## Decision Trees

### Which Button Style?

```
Is it the primary action on this screen?
+-- YES -> Solid/filled button with brand color
|   +-- Is it destructive? -> Confirmation step first, then destructive action becomes primary
+-- NO -> Is it a secondary action?
    +-- YES -> Outline/ghost button
    +-- NO -> Text link style (tertiary)
```

### How Many Options to Show?

```
How many options exist?
+-- 1-5 -> Show all, highlight recommended
+-- 6-12 -> Group into 2-3 categories of 3-4 each
+-- 13-30 -> Progressive disclosure: show top 5, "Show more" for rest
+-- 30+ -> Search + categorized browse
```

### Which Navigation Pattern?

```
Platform?
+-- Desktop Web -> Horizontal top nav (5-7 items), search top-right
+-- Mobile Web -> Hamburger (text + icon + border) + bottom tab bar (3-5 primary actions)
+-- iOS -> Bottom tab bar (max 5), back button top-left
+-- Android -> Top app bar + bottom navigation bar
```

### How to Handle This Error?

```
Is the error preventable by the system?
+-- YES -> Prevent it (Poka-Yoke: constrained controls, smart defaults, disable invalid options)
+-- NO -> Is it a slip or a mistake?
    +-- SLIP (right goal, wrong action) -> Make similar actions visually distinct, add undo
    +-- MISTAKE (wrong goal) -> Improve feedback, show system state, provide undo
    +-- Either way -> Is the user blocked?
        +-- YES -> Full-screen error: what happened + why + how to recover
        +-- NO -> Toast with undo option, auto-dismiss after 5s
```

### How to Organize This Content?

```
What best serves the user's goal?
+-- Finding by category -> Group by type/similarity (shopping, documentation)
+-- Finding by time -> Sort chronologically (activity feeds, history, logs)
+-- Finding by location -> Arrange spatially (store finders, maps)
+-- Finding by name -> Alphabetize (directories, reference lists with 20+ items)
+-- Comparing options -> Sort by magnitude/continuum (price, rating, popularity)
```

### What App Posture to Use?

```
How long will users interact per session?
+-- Hours (IDE, email, dashboard) -> Sovereign: maximize density, keyboard shortcuts, persistent toolbars
+-- Seconds (dialog, search, settings) -> Transient: large controls, zero learning, auto-dismiss
+-- Background (sync, notifications) -> Daemonic: minimize interruption, batch alerts, never steal focus
```

---

## Platform Quick Reference

| Property | Web (Desktop) | Web (Mobile) | iOS | Android |
|----------|--------------|-------------|-----|---------|
| Navigation | Horizontal top bar | Hamburger + bottom tabs | Bottom tab bar | Top app bar + bottom nav |
| Touch target | 32px min | 44-48px | 44pt | 48dp |
| Primary font | System stack / custom | System stack / custom | SF Pro | Roboto |
| Back navigation | Breadcrumbs, browser | Browser, back arrow | < Back (top-left) | <- (top-left) or gesture |
| Search | Visible input field | Icon expanding to field | Search bar or pull-down | Search icon in app bar |
| Scrolling | Vertical, with anchor links | Vertical, pull-to-refresh | Vertical, bounce effect | Vertical, overscroll glow |
| Safe areas | N/A | Viewport meta tag | Top notch + home indicator | Status bar + nav bar |
| Viewport zoom | N/A | Never disable pinch-to-zoom | System-controlled | System-controlled |
| Document lang | `<html lang="en">` | `<html lang="en">` | System language | System language |

---

# Chapter 3: Visual Hierarchy & Layout

Establish clear visual importance so users process information in the intended order. Visual hierarchy determines what users see first, second, and last — without requiring them to read everything.

**When to Use:**
- Starting any new page or screen layout
- Arranging multiple elements that compete for attention
- Deciding element sizes, colors, and positions
- Building action-oriented interfaces with multiple CTAs

---

## Quick Reference

| Concept | Key Value |
|---|---|
| Importance levels | 3: Primary, Secondary, Tertiary |
| Base spacing unit | 16px |
| Spacing scale | 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px |
| Max content width | 600-800px for text, component-specific otherwise |
| Button hierarchy | Solid (primary), Outline (secondary), Text (tertiary) |
| Font size for emphasis | 2x difference minimum between levels |
| Color for emphasis | 2-3 levels of grey (dark, medium, light) |
| Initial scan point | ~30% from top, ~30% from left edge |
| Minimum angular difference | 30 degrees between distinct linear elements |

---

## Importance Assignment

### Rule: Not All Elements Are Equal

**When:** A page or section contains more than 3 visible elements.
**Do:** Assign every element to one of three tiers: Primary (1-2 elements per view), Secondary (supporting content), Tertiary (metadata, timestamps, fine print). Style each tier distinctly using size, weight, and color.
**Values:** Primary: largest size, darkest color (#111827), heaviest weight (600-700). Secondary: medium size, medium grey (#4B5563), weight 400-500. Tertiary: smallest size, lightest grey (#9CA3AF), weight 400.
**Don't:** Give all elements equal visual weight. If everything looks the same, nothing stands out and users scan randomly.

### Rule: Size Isn't Everything

**When:** You need to make an element more prominent than its neighbors.
**Do:** Use a combination of font weight, color darkness, and contrast — not just increased size. A bold, dark 16px label can dominate a light, thin 20px label.
**Values:** Weight difference of at least 200 (e.g., 400 vs 600). Color lightness difference of at least 30% in HSL. Combine 2+ properties for clear separation.
**Don't:** Rely on size alone to create hierarchy. Scaling up creates awkward proportions and wastes space.

### Rule: Emphasize by De-emphasizing

**When:** You want one element to stand out but increasing its size or weight would look excessive.
**Do:** Reduce the visual weight of competing elements instead. Soften their color to a lighter grey, reduce their font weight, or decrease their size.
**Values:** Competing text: use #9CA3AF or lighter. Competing icons: use 60% opacity. Competing borders: use 1px #E5E7EB or remove entirely.
**Don't:** Keep adding emphasis to the target element. Over-emphasized elements look like errors or ads.

### Rule: Labels Are a Last Resort

**When:** Displaying data where the format is self-evident (email addresses, phone numbers, prices, dates, URLs, images).
**Do:** Omit the label. Display the value directly. An email address does not need a "Email:" label. A profile photo does not need a "Photo:" label.
**Values:** Remove labels when the data format has fewer than 2 plausible interpretations. Keep labels when the same format could mean different things (e.g., two date fields: "Created" vs "Modified").
**Don't:** Label every field by default. Unnecessary labels add clutter and slow scanning.

### Rule: Separate Visual Hierarchy from Document Hierarchy

**When:** Semantic HTML heading levels (h1-h6) conflict with the visual importance you need.
**Do:** Use the correct semantic heading level for document structure, then override the visual styling independently. An h3 can look larger than an h2 if the layout demands it.
**Values:** Semantic: follow DOM order (h1 > h2 > h3). Visual: apply classes independently (text-2xl on an h3 is valid).
**Don't:** Let semantic heading levels dictate visual sizes. Document structure and visual hierarchy serve different purposes.

---

## Weight and Contrast

### Rule: Balance Weight and Contrast

**When:** Laying out a page with text, icons, images, and interactive elements.
**Do:** Distribute visual weight across the layout. Heavy elements (dark colors, large sizes, images) anchor sections. Light elements (muted text, whitespace) provide breathing room. No single quadrant should contain all the heavy elements.
**Values:** Each section should have 1 heavy element maximum. Maintain at least 32px of whitespace between heavy elements. Use the squint test: blur your vision and check if weight is balanced.
**Don't:** Cluster all bold/dark elements in one area. This creates an unbalanced layout that feels lopsided.

### Rule: Design in Grayscale First

**When:** Starting a new layout or component design.
**Do:** Build the entire layout using only shades of grey. Establish hierarchy through size, weight, spacing, and grey values before adding any color. Add color only after the hierarchy works in greyscale.
**Values:** Use 5 grey values: #111827 (primary text), #374151 (secondary text), #6B7280 (tertiary text), #D1D5DB (borders), #F9FAFB (backgrounds).
**Don't:** Start with color. Color can mask hierarchy problems — a layout that only works because of color will fail in edge cases (printing, low vision, dark mode).

### Rule: Faces Demand Attention

**When:** Designing hero sections, testimonials, or trust-building areas.
**Do:** Use human faces to draw attention to key content. Position faces looking toward CTAs. The fusiform face area in the brain fires automatically — users cannot ignore faces.
**Values:** Face images increase dwell time 2-3x. Faces gazing at CTA increase conversion vs faces looking at camera. Real photos outperform illustrations for trust.
**Don't:** Place faces competing with primary actions. Don't use stock photos with fake smiles (users detect them).

### Rule: Face-ism Ratio for Photo Cropping

**When:** Displaying photos of people in profiles, testimonials, or team pages.
**Do:** Crop photos tight to the face to encourage emotional response and emphasize personality. Wider cropping emphasizes physical appearance over personality. Choose the ratio deliberately based on the goal of the section.
**Values:** High face-ism ratio (face fills 60-80% of frame): use for testimonials, profiles, trust-building. Low face-ism ratio (full body): use for product/fashion shots where physical context matters.
**Don't:** Use inconsistent cropping ratios within the same component type. Don't use low face-ism ratios when the goal is to build empathy or trust.

---

## Attention and Scan Patterns

### Rule: Initial Scan Point Is Off-Center

**When:** Placing primary content and CTAs.
**Do:** Position the most important content ~30% from top and 30% from left edge. Eye-tracking shows users don't start at top-left corner — they begin slightly inward.
**Values:** Primary CTA zone: 20-40% from left, 20-40% from top. Hero headline sweet spot: centered horizontally, top third vertically.
**Don't:** Assume top-left is always first seen. Don't place critical actions at extreme edges/corners.

### Rule: Proximity Increases Perceived Value

**When:** Positioning pricing, product images, or value-communicating elements.
**Do:** Place product/value representation close to the user's primary interaction zone. Physical proximity increases perceived value.
**Values:** Product image near checkout button. Pricing near the feature list. Preview/thumbnail near the action that generates it.
**Don't:** Separate value display from action point. Don't place pricing on a separate page from features.

### Rule: Orientation Sensitivity — The 30-Degree Rule

**When:** Using angled or diagonal lines, decorative elements, or directional indicators in a layout.
**Do:** Ensure angular differences between distinct linear elements are at least 30 degrees. Favor horizontal and vertical orientations as primary layout axes — they are processed faster and perceived as more aesthetic.
**Values:** Minimum distinguishable angle difference: 30 degrees. Horizontal and vertical lines are perceived ~20% more accurately than oblique lines.
**Don't:** Use subtle angular differences (< 30 degrees) to distinguish elements — users cannot reliably perceive them. Don't use oblique primary axes when horizontal/vertical alternatives exist.

---

## Alignment and Visual Weight

### Rule: Area Alignment — Align by Visual Weight, Not Edges

**When:** Centering or aligning asymmetric elements (icons of different shapes, mixed-size images, pull quotes, bullet lists).
**Do:** Align based on visual weight/area, not geometric edges. For asymmetric icons, position them so equal visual mass falls on each side of the alignment axis. Hang pull quotes on the text margin (quotation marks extend into the gutter). Hang bullet points and numbers outside the text margin.
**Values:** Pull quote marks: hang outside the left text edge. Numbered lists: align on text start, not on numbers. Icon alignment: center on visual mass, not bounding box.
**Don't:** Use software center-alignment for asymmetric elements without manual adjustment. Don't align bulleted text on the bullet character — align on the text.

### Rule: Line Tension and Edge Tension

**When:** Arranging repeated elements in a layout (icon rows, feature grids, navigation items, image galleries).
**Do:** Use the implicit lines created by aligned repeated elements to guide the user's eye toward a focal point. Break the line or pattern at the point where you want maximum attention. Arrange elements to form implied shapes (rectangles, paths) that create visual cohesion without adding borders.
**Values:** 3+ aligned elements create a perceptible line. A gap or changed element in a line steals focus from the rest. Corner elements of a grid create an implied rectangle, making content inside feel contained.
**Don't:** Break alignment accidentally — it disrupts the implicit line and looks disordered. Don't add visible borders when line/edge tension achieves the same grouping effect with less visual noise.

### Rule: Common Fate — Motion Grouping

**When:** Animating UI elements or displaying elements that move (loading indicators, carousel items, expanding panels, drag-and-drop).
**Do:** Make related elements move at the same time, velocity, and direction. Elements that move together are perceived as a single group. When elements within a container move, move the container's edges in the same direction to keep them perceived as foreground.
**Values:** Simultaneous start time, identical velocity, same direction = strongest grouping. If elements flicker (e.g., skeleton loaders), synchronize timing and frequency.
**Don't:** Animate related elements with staggered timing unless deliberately communicating sequence. Don't keep a container static while its children animate in a direction — it breaks figure-ground.

---

## Interaction Placement

### Rule: Axis of Interaction

**When:** Deciding where to place interactive elements (buttons, links, CTAs) within a layout.
**Do:** Identify the visual edges and alignment lines created by text blocks, images, and content groups. Place interactive elements on or near these axes — users' eyes follow axes and cannot click what they don't see. Move low-priority or destructive actions off-axis.
**Values:** Primary CTA: on the dominant vertical or horizontal axis. Secondary actions: on a secondary axis. Tertiary/dangerous actions: off any axis, in a less prominent position.
**Don't:** Place the primary action far from any alignment edge. Don't place destructive actions (delete, cancel) on the same axis as constructive actions (save, submit).

### Rule: Propositional Density

**When:** Designing logos, icons, illustrations, or key visual elements for a product.
**Do:** Favor simple visual elements that carry multiple layers of meaning. Calculate propositional density: PD = deep meanings / surface elements. Elements with PD > 1 are perceived as more interesting and memorable. Ensure that multiple meanings are complementary, not contradictory.
**Values:** PD > 1 = engaging and memorable. PD < 1 = bland, forgettable. Strong brand logos typically PD 1.5-3.
**Don't:** Add visual complexity to increase meaning — add meaning to simple forms. Don't stack contradictory associations into a single element.

---

## Button and Action Hierarchy

### Rule: Button/Action Hierarchy

**When:** A view contains more than one interactive action.
**Do:** Apply three button tiers: Primary = solid filled background with white text (1 per view). Secondary = outline with border, transparent background (1-2 per view). Tertiary = text-only, no border or background (unlimited).
**Values:** Primary: background-color: brand color, color: #FFFFFF, padding: 12px 24px, border-radius: 6px, font-weight: 600. Secondary: border: 1px solid #D1D5DB, color: #374151, same padding. Tertiary: color: brand color, padding: 8px 16px, no border, no background.
**Don't:** Use more than one primary button per view. Two solid buttons create a competing-actions problem where users hesitate.

---

## Spacing and Layout

### Rule: Start with Too Much White Space

**When:** Placing elements on a page or within a component.
**Do:** Begin with generous spacing, then selectively reduce only where elements feel disconnected. It is easier to remove space than to add it later.
**Values:** Start with 32-48px between sections, 16-24px between related elements, 8-12px between tightly coupled elements (label and input). Reduce by one step on the scale if too loose.
**Don't:** Start with tight spacing and try to add breathing room later. Cramped layouts are harder to fix than spacious ones.

### Rule: Establish Spacing and Sizing System

**When:** Setting up a new project or design system.
**Do:** Use a base unit of 16px and a constrained scale. Apply spacing values only from this scale — no arbitrary values like 13px or 22px.
**Values:** Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px. Use 4px for tight gaps (icon to label). 8px for related elements. 16px for standard padding. 24-32px for section separation. 48-64px for major sections. 96-128px for page-level spacing.
**Don't:** Use arbitrary spacing values. Inconsistent spacing creates visual noise even when users cannot articulate why the design feels "off."

### Rule: Don't Fill the Whole Screen

**When:** Laying out content areas, forms, cards, or media.
**Do:** Give each element only the width it needs, not the full available width. A 600px-wide form in the center of a 1440px screen is correct. A form stretched to 1440px is not.
**Values:** Text content: max-width 600-800px (45-75 characters). Forms: max-width 400-500px. Cards in grid: fixed widths of 280-350px. Sidebar: 240-300px fixed. Main content: flex-grow with max-width.
**Don't:** Set everything to width: 100%. Elements that are wider than their optimal reading/interaction width become harder to use.

### Rule: Grids Are Overrated

**When:** Deciding between CSS Grid with equal columns vs. component-specific sizing.
**Do:** Use fixed widths for elements that have an optimal size (sidebars, cards, form fields). Use flex-grow only for the main content area that should absorb remaining space.
**Values:** Sidebar: width: 280px (fixed). Main content: flex: 1, min-width: 0, max-width: 800px. Cards: width: 320px in a flex-wrap container with gap: 24px. Do not force a 12-column grid on everything.
**Don't:** Default to a 12-column grid system for every layout. Grids force compromises where elements stretch or compress to fit column math instead of their natural size.

### Rule: Relative Sizing Doesn't Scale

**When:** Building responsive layouts across multiple breakpoints.
**Do:** Define element sizes independently for each breakpoint. A heading that is 36px on desktop should not automatically become 24px on mobile because of a ratio — it should be explicitly set to 24px (or whatever looks right) at that breakpoint.
**Values:** Define at least 3 breakpoints: mobile (<640px), tablet (640-1024px), desktop (>1024px). Set font sizes, padding, and widths independently at each breakpoint.
**Don't:** Use percentage-based or ratio-based scaling (e.g., font-size: 2.5vw) expecting it to work across all screen sizes. Ratios that work at 1440px produce unreadable text at 375px.

### Rule: Avoid Ambiguous Spacing

**When:** Placing a label, heading, or divider between two content blocks.
**Do:** Ensure the element is visually closer to the block it belongs to. Use more space above a section heading than below it. Use more space between groups than within groups.
**Values:** Space above heading: 32-48px. Space below heading: 12-16px. Space within a group: 8-12px. Space between groups: 24-32px. The between-group spacing should be at least 2x the within-group spacing.
**Don't:** Use equal spacing above and below section headings or dividers. Equal spacing creates ambiguity about which section an element belongs to.

---

## Platform Notes

| Platform | Spacing base | Grid system |
|---|---|---|
| Web | 16px (1rem) | CSS Flexbox + Grid |
| iOS | 16pt | UIStackView, Auto Layout |
| Android | 16dp | ConstraintLayout, Material grid |

---

## Checklist

- [ ] Every element assigned to Primary, Secondary, or Tertiary tier
- [ ] Hierarchy works in greyscale (no color dependency)
- [ ] Maximum 1 primary button per view
- [ ] All spacing values from the defined scale
- [ ] Content areas have max-width constraints
- [ ] Section headings are closer to their content than to previous section
- [ ] Labels removed where data format is self-evident
- [ ] Visual weight balanced across layout quadrants
- [ ] Primary content positioned in the initial scan zone (~30% from top-left)
- [ ] Value-communicating elements placed near their associated actions
- [ ] Human faces (if used) directed toward CTAs, not competing with them
- [ ] Photo cropping uses deliberate face-ism ratio (tight for trust, wide for context)
- [ ] Angular differences between linear elements are at least 30 degrees
- [ ] Asymmetric elements aligned by visual weight, not bounding box
- [ ] Related animated elements move in sync (same time, velocity, direction)
- [ ] Implicit alignment lines guide the eye toward focal points
- [ ] Primary CTAs placed on dominant visual axes
- [ ] Logos and icons carry high propositional density (PD > 1)

---
---

# Chapter 4: Typography System

Define a systematic approach to typeface selection, sizing, and spacing that ensures readability and hierarchy across all text content.

**When to Use:**
- Setting up a new project's text styles
- Choosing fonts for headings, body, and UI elements
- Debugging readability issues
- Building a type scale for a design system

---

## Quick Reference

| Property | Value |
|---|---|
| Type scale | 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72px |
| Base body size | 16px |
| Line length | 45-75 characters (20-35em) |
| Body line-height | 1.5 |
| Heading line-height | 1-1.25 |
| Normal weight range | 400-500 |
| Emphasis weight range | 600-700 |
| System font stack | -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif |
| Preference-optimized line length | 45-72 cpl |
| Speed-optimized line length | 80-100 cpl |
| Root font-size | 100% (never px) |
| Readability target | Flesch reading ease 60+ |

---

## Type Scale

### Rule: Establish a Type Scale

**When:** Setting up text styles for a project.
**Do:** Choose font sizes only from a predefined scale. Do not invent sizes. Use the following scale, selecting the sizes you need (you will not use all of them in every project).
**Values:** 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72px. Minimum: use at least 4 sizes (body, small, one heading, one large heading). Typical: 5-7 sizes covers most interfaces.
**Don't:** Use arbitrary sizes like 13px, 15px, or 22px. Off-scale sizes create inconsistency and make the type system harder to maintain.

### Rule: Don't Use Em Units for Font Size

**When:** Setting font-size in CSS.
**Do:** Use px or rem. 1rem = the root font size (typically 16px). Pixel values are predictable and debuggable.
**Values:** `font-size: 16px` or `font-size: 1rem`. For responsive: use rem with a root size change at breakpoints, or explicit px values per breakpoint.
**Don't:** Use em units for font-size. Em compounds through nesting — a 0.875em inside a 0.875em container produces 0.766em (12.25px instead of 14px). This creates unpredictable sizing.

### Rule: Font Size in Relative Units at Root

**When:** Setting base font size for a document.
**Do:** Set root font-size as `100%` (not a pixel value) on the `<html>` element to respect user-configured font sizes. Use `rem` for font-size, padding, and margin so everything scales proportionately. For fluid typography, use `calc(1em + 1vw)` to combine viewport units with em units, preserving zoom capability.
**Values:** `html { font-size: 100%; }` — never `font-size: 16px` on root. Body text: `1rem`. Headings: multiples of rem (e.g., `2rem`, `1.5rem`). Line-height: unitless `1.5`. Media queries: use `em` units (not `px` or `rem`) for breakpoints.
**Don't:** Set root font-size in pixels — this overrides user preferences. Don't use viewport units alone (`vw`) for text — they cannot be zoomed. Don't convert rem to px in a preprocessor.

---

## Font Selection

### Rule: Use Good Fonts

**When:** Choosing a typeface for a project.
**Do:** Select fonts that have at least 5 font weights available. This gives you enough range for hierarchy. Filter font libraries by weight count before browsing styles.
**Values:** Minimum weights needed: 400 (normal), 500 (medium), 600 (semibold), 700 (bold). Ideal: also 300 (light) and 800 (extrabold) for display use. Sources: Google Fonts (filter by "Number of styles" > 10), Font Squirrel, commercial foundries.
**Don't:** Choose a font with only 1-2 weights. You will be unable to create hierarchy within a single typeface and will need to introduce a second font unnecessarily.

### Rule: Font Recommendations

**When:** You need specific typeface suggestions rather than browsing.
**Do:** Use these tested combinations:

| Use | Fonts |
|---|---|
| Headlines (geometric) | Inter, Poppins, Raleway, Montserrat |
| Headlines (serif) | Playfair Display, Lora, Merriweather |
| Body text | Inter, Source Sans Pro, IBM Plex Sans, Nunito Sans |
| UI elements | Inter, SF Pro (Apple), Roboto (Google), Segoe UI (Microsoft) |
| Monospace/Code | JetBrains Mono, Fira Code, Source Code Pro, IBM Plex Mono |
| System stack | -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif |

**Values:** Limit to 2 typefaces per project: one for headings, one for body/UI. If using a single typeface, Inter and Source Sans Pro both work for all contexts.
**Don't:** Use more than 2 typefaces. Each additional font increases page weight, visual complexity, and maintenance burden.

### Rule: Web Fonts as Progressive Enhancement

**When:** Loading custom web fonts.
**Do:** Treat web fonts as an enhancement, not a requirement. Avoid FOIT (flash of invisible text) — users on slow networks may see no text at all if fonts block rendering. Load fonts asynchronously. Choose system font fallbacks with similar metrics to minimize FOUT (flash of unstyled text).
**Values:** Font loading strategy: async (never render-blocking). Fallback: system font with similar x-height and width metrics. Subset fonts to needed character ranges (e.g., Basic Latin only) to reduce file size. Maximum web font budget: 100-150KB total.
**Don't:** Let web fonts block text rendering (FOIT). Don't load entire font families when you only need 1-2 weights. Don't skip fallback fonts for users without JavaScript.

### Rule: Font Weight Rules

**When:** Assigning font-weight to text elements.
**Do:** Use 400-500 for normal body text. Use 600-700 for emphasis, headings, and labels. Reserve 800-900 for large display text only (36px+).
**Values:** Body text: 400. UI labels and nav: 500. Section headings: 600. Page titles: 700. Hero/display text (48px+): 700-800.
**Don't:** Use font-weight below 400 for any UI text. Weights 100-300 are illegible at small sizes and on low-resolution displays. Light/thin weights are acceptable only for display text above 36px.

### Rule: Font Difficulty Transfers to Task Difficulty

**When:** Choosing fonts for instructions, forms, onboarding, or any task the user must complete.
**Do:** Use clean, highly legible fonts for actionable content. Research: hard-to-read fonts make users perceive the described task as harder and less likely to attempt it.
**Values:** Body text for instructions: system font stack or clean sans-serif. Minimum 16px. High contrast 4.5:1+. Reserve decorative fonts for non-actionable branding.
**Don't:** Use decorative, condensed, or light-weight fonts for form labels, error messages, instructions, or CTAs.

---

## Readability

### Rule: Line Length

**When:** Setting the width of any text container (paragraphs, articles, descriptions).
**Do:** Constrain line length to 45-75 characters per line. Set this via max-width on the text container.
**Values:** Optimal: 65 characters (~32.5em at 16px). Range: 20-35em max-width. For 16px base: max-width: 560px (35em). For wider layouts, use columns or increase margins — do not stretch lines.
**Don't:** Allow lines to exceed 75 characters. Long lines cause readers to lose their place when moving to the next line. Lines under 45 characters cause too many line breaks and choppy reading.

### Rule: Line Length Speed vs Preference Tradeoff

**When:** Setting content column width.
**Do:** Users READ FASTER with longer lines (100 cpl) but PREFER shorter lines (45-72 cpl). Use preference-optimized range by default; consider wider columns for dashboards/logs.
**Values:** Preference-optimized: 45-72 cpl (default). Speed-optimized: 80-100 cpl (dashboards, code). Multi-column: 40-60 cpl per column.
**Don't:** Exceed 100 characters per line.

### Rule: Optimize for Screen Reading

**When:** Designing long-form content (docs, articles, settings pages).
**Do:** Users read 25% slower on screens and scan rather than read linearly. Use shorter paragraphs (3-4 sentences max), more subheadings, bullet lists, and bold key terms.
**Values:** Paragraph max: 3-4 sentences. Subheading every 2-3 paragraphs. Bold first instance of key terms. Bullet lists for 3+ related items.
**Don't:** Write wall-of-text paragraphs. Don't use print-optimized layouts.

### Rule: Content Readability Testing

**When:** Writing body text, help text, error messages, or any user-facing copy.
**Do:** Test content readability using Flesch-Kincaid tests. Aim for a reading ease score of 60-70+ (easily understood by 13-15 year olds). Use readability as an early warning system, not a definitive measure — also test with real users.
**Values:** Flesch reading ease: 60+ for general content, 70+ for critical instructions. Grade level: 8th grade or below. Flag words > 4 syllables and sentences > 35 words.
**Don't:** Use readability scores as the sole measure — they cannot detect confusing structure or misleading content. Don't write for artificially low reading levels if technical precision is needed.

### Rule: Line-Height is Proportional

**When:** Setting line-height for any text element.
**Do:** Use tighter line-height for large text and looser line-height for small text. Body text needs more vertical space between lines than headlines.
**Values:** Body text (14-18px): line-height: 1.5 (24px for 16px text). Sub-headings (20-30px): line-height: 1.3-1.4. Headlines (36-72px): line-height: 1-1.15. Small/caption text (12px): line-height: 1.6-1.75. Wide content (over 65 chars/line): up to line-height: 2.
**Don't:** Use a single line-height value (e.g., 1.5) for all text sizes. A 72px headline with line-height 1.5 produces 108px of line height — 36px of unnecessary gap between lines.

### Rule: Baseline Alignment for Mixed Sizes

**When:** Placing text of different sizes on the same horizontal line (e.g., a heading with a badge, a price with a currency symbol).
**Do:** Align text to the baseline (bottom of the text's x-height), not to the vertical center of the container.
**Values:** CSS: `align-items: baseline` on the flex container. Avoid `align-items: center` when mixing font sizes.
**Don't:** Vertically center text of different sizes. Center alignment makes smaller text appear to float above the visual line, creating a misaligned appearance.

---

## Text Styling

### Rule: Not Every Link Needs a Color

**When:** Displaying links within navigation, cards, or other clearly interactive contexts.
**Do:** Use the default text color and a heavier font weight for links in contexts where clickability is already implied (navigation menus, card titles, list items). Reserve colored/underlined links for inline text where they must be distinguished from surrounding content.
**Values:** Navigation links: color: inherit, font-weight: 500-600, text-decoration: none. Inline text links: color: brand blue, text-decoration: underline. Hover state: underline or color shift for all link types.
**Don't:** Apply link color (blue, underline) to every anchor tag. In navigation and card contexts, colored links add visual noise without aiding comprehension.

### Rule: Underlines for Inline Links Are Mandatory

**When:** Styling inline links within paragraph text.
**Do:** Keep underlines on inline links — they are the universal affordance for clickability within text. Color alone is insufficient because color-blind users cannot differentiate links from surrounding text. For improved readability, replace browser default underlines with CSS gradient-based underlines that avoid crossing descenders.
**Values:** Default `text-decoration: underline` is acceptable. Enhanced: use `background-image: linear-gradient()` with positioning to protect descenders. Call-to-action links styled as buttons are exempt from this rule.
**Don't:** Remove underlines from inline links with `text-decoration: none` unless providing an equivalent visual indicator. Don't rely on color change alone to indicate links.

### Rule: Visited vs Unvisited Link Colors

**When:** Styling text links in content areas.
**Do:** Use different colors for visited vs unvisited links. The distinction is automatic in browsers but often overridden by CSS resets.
**Values:** Two noticeably different colors. Default browser behavior is a good starting point. Most useful on pages with multiple links to explore.
**Don't:** Style visited and unvisited links identically.

### Rule: Align with Readability

**When:** Setting text-align on any text block.
**Do:** Left-align body text, descriptions, and any content longer than 2 lines. Center-align only short text blocks (headings, labels, single-line captions) that are visually centered in their container. Right-align numbers in tables for decimal alignment.
**Values:** Left-align: all body text, lists, form labels, descriptions. Center: headings in hero sections, single-line captions, empty state text (max 3 lines). Right-align: numeric table columns, prices, quantities.
**Don't:** Center-align paragraphs or multi-line text. Centered text with ragged left edges is significantly harder to scan, because the eye cannot predict where the next line starts.

### Rule: Letter-Spacing

**When:** Styling headlines, ALL-CAPS text, or large display text.
**Do:** Tighten letter-spacing on headlines (they look too loose at default spacing). Widen letter-spacing on ALL-CAPS text (capitals have no descenders/ascenders to create natural spacing).
**Values:** Headlines (24px+): letter-spacing: -0.01em to -0.03em. ALL-CAPS text: letter-spacing: 0.05em to 0.1em. Body text: leave at default (letter-spacing: normal).
**Don't:** Tighten letter-spacing on body text (reduces readability) or leave ALL-CAPS at default spacing (letters feel cramped because uniform height removes natural rhythm).

---

## Platform Notes

| Platform | Base size | System font | Scale method |
|---|---|---|---|
| Web | 16px (1rem) | System font stack | rem or px |
| iOS | 17pt (Body) | SF Pro | Dynamic Type |
| Android | 16sp (Body) | Roboto | sp units |

---

## Checklist

- [ ] Type scale defined with specific px values from the standard scale
- [ ] Maximum 2 typefaces selected
- [ ] All chosen fonts have 5+ weights available
- [ ] Body text line length constrained to 45-75 characters
- [ ] Line-height varies by text size (tighter for headlines, looser for body)
- [ ] No font-weight below 400 used for UI text
- [ ] ALL-CAPS text has increased letter-spacing
- [ ] Headlines have slightly tightened letter-spacing
- [ ] No em units used for font-size
- [ ] Mixed-size text uses baseline alignment, not center
- [ ] Actionable content uses clean, legible fonts (no decorative fonts for instructions/CTAs)
- [ ] Screen-optimized text: short paragraphs, frequent subheadings, bolded key terms
- [ ] Visited and unvisited links have distinct colors
- [ ] Root font-size set to 100%, not a pixel value
- [ ] Web fonts load asynchronously with system font fallbacks
- [ ] Content readability tested (Flesch reading ease 60+)
- [ ] Inline links have visible underlines, not color alone

---
---

# Chapter 5: Color System

Build a complete, accessible color palette using HSL, with systematic shade generation and proper contrast ratios for all text and interactive elements.

**When to Use:**
- Creating a color palette for a new project
- Adding semantic colors (success, warning, error, info)
- Fixing contrast or accessibility issues
- Building dark mode or themed variations
- Designing for international audiences

---

## Quick Reference

| Concept | Value |
|---|---|
| Color model | HSL (Hue 0-360, Saturation 0-100%, Lightness 0-100%) |
| Grey shades needed | 8-10 |
| Primary color shades | 5-10 (100-900 scale) |
| Text contrast (normal) | 4.5:1 minimum (WCAG AA) |
| Text contrast (large, 18px+) | 3:1 minimum (WCAG AA) |
| Hue rotation range | Max 20-30 degrees |
| Accent colors | 1 per semantic state (success, warning, error, info) |
| Safest global colors | Blue and grey (fewest negative cultural associations) |
| Body text | #222-#333 (never pure #000) |

---

## Color Model

### Rule: Use HSL Not Hex

**When:** Defining any color value in your system.
**Do:** Use HSL (Hue, Saturation, Lightness) as your mental model and authoring format. HSL makes it intuitive to generate lighter/darker variants by adjusting the L value, and to create harmonious palettes by rotating the H value.
**Values:** Format: `hsl(H, S%, L%)`. H: 0-360 (color wheel position). S: 0-100% (grey to vivid). L: 0-100% (black to white). Example: a medium blue is `hsl(210, 80%, 50%)`.
**Don't:** Author colors in hex (#3B82F6) or RGB (rgb(59, 130, 246)) as your primary system. Hex values are not human-readable — you cannot glance at #3B82F6 and know how to make it 20% lighter. Convert to hex only for implementation if required by your framework.

---

## Palette Structure

### Rule: Three Color Categories

**When:** Setting up a project's color palette.
**Do:** Define three categories: (1) Primary brand color — used for buttons, active states, links. (2) Neutrals — greys used for text, borders, backgrounds. (3) Supporting/Accent — semantic colors for success (green), warning (amber/yellow), error (red), info (blue).
**Values:** Primary: 1 hue with 5-10 shades. Neutrals: 8-10 shades from near-white to near-black. Accent colors: 1 hue per semantic meaning, each with 3-5 shades (light bg, medium border, dark text).
**Don't:** Define colors ad hoc. Every color in the interface should trace back to one of these three categories.

### Rule: You Need More Colors Than You Think

**When:** Building a palette from a single brand color.
**Do:** Generate a full shade range for every color. You will need light shades for backgrounds, medium shades for borders and icons, and dark shades for text. A single blue is not enough — you need blue-50 through blue-900.
**Values:** Per primary hue: 9 shades minimum (100, 200, 300, 400, 500, 600, 700, 800, 900). Grey palette: 10 shades (50, 100, 200, 300, 400, 500, 600, 700, 800, 900). Accent colors: 5 shades minimum (100, 300, 500, 700, 900).
**Don't:** Define only 2-3 shades per color. You will end up inventing one-off colors when you need a light background or subtle border, breaking the system.

---

## Shade Generation

### Rule: Define 9 Shades Per Color

**When:** Generating a shade range from a chosen hue.
**Do:** Start by picking shade 500 (your base, the color you "think of" when you think of this hue). Then pick shade 900 (darkest usable, for text on light backgrounds). Then pick shade 100 (lightest, for tinted backgrounds). Fill in the gaps so each step has a perceptible difference.
**Values:** Lightness values (approximate for HSL): 100: L=95%. 200: L=90%. 300: L=80%. 400: L=65%. 500: L=50%. 600: L=42%. 700: L=35%. 800: L=25%. 900: L=18%. Adjust saturation down slightly for very light shades and up for mid-range shades.
**Don't:** Generate shades by simply adjusting lightness in equal steps. Perceptual uniformity requires unequal lightness steps — the difference between L=90% and L=80% is less visible than between L=30% and L=20%.

### Rule: Hue Rotation for Perceived Saturation

**When:** Creating lighter and darker shades of a color that look vivid and natural rather than washed out.
**Do:** Rotate the hue slightly when generating shades. To lighten: rotate toward the nearest "bright" hue (yellow at 60, cyan at 180, magenta at 300). To darken: rotate toward the nearest "dark" hue (red at 0, green at 120, blue at 240).
**Values:** Maximum rotation: 20-30 degrees across the full shade range. Example for blue (H=210): lightest shades rotate toward cyan (H=195-200), darkest shades rotate toward blue-violet (H=225-230).
**Don't:** Keep the same hue across all shades. Uniform-hue shades look dull and artificial compared to hue-rotated shades. Compare Tailwind CSS's blue palette (hue-rotated) to a simple lightness ramp.

---

## Greys

### Rule: Greys Don't Have to Be Grey

**When:** Defining your neutral/grey palette.
**Do:** Add a slight saturation (3-8%) with a deliberate hue to your greys. Choose blue for a cool, professional feel. Choose yellow/tan for a warm, friendly feel. All greys in the palette should share the same hue.
**Values:** Cool greys: hsl(210, 5-8%, L%). Warm greys: hsl(40, 4-6%, L%). True grey (no temperature): hsl(0, 0%, L%). Apply the chosen hue to all 10 grey shades consistently.
**Don't:** Mix warm and cool greys in the same palette. Inconsistent grey temperature makes surfaces look like they belong to different designs.

### Rule: No True Black

**When:** Setting the darkest color for text or backgrounds.
**Do:** Use a very dark grey or saturated dark color instead of #000000. True black against white creates maximum contrast that feels harsh and unnatural.
**Values:** Darkest text: hsl(210, 15%, 10%) or #111827 (Tailwind gray-900). Darkest background (dark mode): hsl(210, 15%, 8%) or #0F172A. Reserve #000000 only for images or borders at 1px where the difference is imperceptible.
**Don't:** Use #000000 for text or large background areas. The stark contrast causes eye strain during extended reading.

---

## Contrast and Accessibility

### Rule: Contrast Requirements

**When:** Placing text on any background, or using color to convey meaning in UI elements.
**Do:** Verify contrast ratios meet WCAG AA standards. Use a contrast checker tool (browser DevTools, WebAIM, Stark plugin).
**Values:** Normal text (under 18px, or under 14px bold): 4.5:1 minimum. Large text (18px+ regular, or 14px+ bold): 3:1 minimum. UI components and graphical objects: 3:1 minimum against adjacent colors. AAA (enhanced): 7:1 normal text, 4.5:1 large text.
**Don't:** Assume light grey text on white meets contrast requirements. Common failures: #9CA3AF on #FFFFFF is only 2.9:1 — it fails AA. Use #6B7280 or darker for readable grey text on white.

### Rule: Temper Maximum Contrast

**When:** Setting body text and background colors.
**Do:** Use near-black on near-white rather than pure `#000` on `#fff`. Very high contrast can diminish readability for users with scotopic sensitivity syndrome (Irlen syndrome), causing text to appear to blur or move. Slightly tempered contrast is comfortable for everyone while still exceeding WCAG AAA.
**Values:** Body text: `#222` to `#333`. Background: `#f5f5f5` to `#eee`. This still passes WCAG AAA contrast requirements (7:1+) while reducing glare. Maintain minimum 4.5:1 for normal text, 3:1 for large text per WCAG.
**Don't:** Default to pure black (#000000) on pure white (#ffffff). The maximum possible contrast is not the optimal contrast for reading comfort.

### Rule: Flip the Contrast

**When:** Designing colored sections, cards, or banners with a saturated background.
**Do:** Instead of white text on a dark/saturated background, consider dark text on a lighter tint of the color. Lighter backgrounds with dark text are more readable and accessible.
**Values:** Instead of: white (#FFF) text on hsl(210, 80%, 45%) background. Try: hsl(210, 80%, 18%) text on hsl(210, 80%, 92%) background. The light-background version is easier to read and always passes contrast.
**Don't:** Default to white text on brand-color backgrounds. White-on-color often fails contrast (especially with medium-lightness colors like orange, green, cyan) and is harder to read than the inverted version.

### Rule: Constancy — Perceptual Constancy

**When:** Choosing colors for elements that appear on varying backgrounds or in light/dark mode.
**Do:** Test colors against their actual backgrounds, not in isolation. The same hex color will appear different on light vs. dark backgrounds due to perceptual constancy correction errors. Adjust hue and saturation to compensate.
**Values:** A circle on a warm background appears cooler; on a cool background, warmer. Grey on white appears darker than grey on black. Always verify contrast ratios in context, not on a neutral canvas.
**Don't:** Pick colors from a swatch palette without placing them on the actual design background. Don't assume the same color will look identical on both light and dark mode without adjustment.

### Rule: Don't Rely on Color Alone

**When:** Using color to indicate status, errors, categories, or required fields.
**Do:** Supplement color with a secondary indicator: an icon, a text label, a pattern, or a shape change. Approximately 8% of men have color vision deficiency.
**Values:** Error fields: red border + error icon + error text message (all three). Status badges: colored background + text label ("Active," "Pending"). Charts: color + pattern fills (stripes, dots) + direct labels.
**Don't:** Use color as the sole differentiator. A red/green status indicator is meaningless to users with protanopia or deuteranopia.

### Rule: Cultural Color Meanings

**When:** Choosing semantic colors for international audiences.
**Do:** Verify color choices don't conflict with cultural meanings. Red = danger in West but luck in China. White = purity in West but mourning in parts of Asia.
**Values:** Global products: pair color with icons/text, never color alone. Blue and grey have fewest negative cultural associations. Research target market color associations.
**Don't:** Assume Western color semantics are universal.

---

## Emotional Color

### Rule: Biophilia Effect — Nature in UI

**When:** Designing backgrounds, empty states, loading screens, or wellness/productivity interfaces.
**Do:** Incorporate nature imagery (landscapes, plants, water, sky gradients) to reduce user stress and enhance focus. Even abstract nature-inspired patterns (organic shapes, green/blue palettes, gradient skies) confer partial benefits. Use nature imagery in waiting states, error pages, and rest screens.
**Values:** Nature-view backgrounds reduce stress markers. Green/blue nature palettes are most effective. Works with photos, illustrations, or even abstract organic patterns. Most effective in environments requiring sustained concentration.
**Don't:** Use nature imagery as decoration that competes with content. Don't use it in place of fixing actual UX problems — it reduces stress, not confusion.

### Rule: Emotional Priming Through Aesthetics

**When:** Making aesthetic decisions that seem "merely visual" — choosing between rounded vs. sharp corners, warm vs. cool colors, illustration style, photography treatment.
**Do:** Aesthetic choices prime emotional responses before the user consciously evaluates the content. Apply deliberately: (1) Rounded corners + warm colors = approachable, friendly, safe. (2) Sharp angles + cool colors = professional, precise, authoritative. (3) Organic shapes + natural colors = calm, trustworthy, sustainable. (4) High contrast + bold typography = confident, modern, energetic. Every visual choice is an emotional signal, whether intentional or not.
**Values:** Rounded corners: 4-8px for friendly products, 0-2px for professional products. Color temperature: warm (oranges, yellows) for consumer/social, cool (blues, greys) for enterprise/tools. Consistency matters more than any single choice — a product that mixes rounded and sharp aesthetics feels confused.
**Don't:** Use framework defaults without considering their emotional signal. Don't choose aesthetics based solely on trends — align with your product's personality. Don't mix conflicting aesthetic signals (playful illustrations + corporate typography = confusing). Don't ignore the emotional weight of whitespace — generous whitespace signals premium/luxury, dense layouts signal utility/efficiency.

---

## Example Palette

### Rule: Example Palette Values (Blue Grey)

**When:** You need a reference palette to start from.
**Do:** Use or adapt this tested blue-grey palette:

| Shade | Hex | HSL |
|---|---|---|
| 50 | #F8FAFC | hsl(210, 40%, 98%) |
| 100 | #F1F5F9 | hsl(210, 40%, 96%) |
| 200 | #E2E8F0 | hsl(214, 32%, 91%) |
| 300 | #CBD5E1 | hsl(213, 27%, 84%) |
| 400 | #94A3B8 | hsl(215, 20%, 65%) |
| 500 | #64748B | hsl(215, 16%, 47%) |
| 600 | #475569 | hsl(215, 19%, 35%) |
| 700 | #334155 | hsl(215, 25%, 27%) |
| 800 | #1E293B | hsl(217, 33%, 17%) |
| 900 | #0F172A | hsl(222, 47%, 11%) |

**Values:** Note how saturation increases at darker shades and hue shifts slightly (210 to 222). This produces a rich, not flat, grey scale.
**Don't:** Use this palette as-is without checking contrast in your specific layout. Always verify text-on-background combinations meet 4.5:1.

---

## Platform Notes

| Platform | Color format | System colors |
|---|---|---|
| Web | HSL, hex, RGB, CSS custom properties | prefers-color-scheme media query |
| iOS | UIColor / SwiftUI Color (RGB or P3) | .systemBackground, .label, .secondaryLabel |
| Android | ARGB hex in themes | MaterialTheme.colorScheme |

---

## Checklist

- [ ] All colors defined in HSL as the source of truth
- [ ] 8-10 grey shades defined with consistent hue temperature
- [ ] Primary color has 9 shades (100-900)
- [ ] Each accent/semantic color has at least 5 shades
- [ ] All normal text passes 4.5:1 contrast ratio
- [ ] All large text passes 3:1 contrast ratio
- [ ] No #000000 used for text or large areas
- [ ] Body text uses tempered contrast (#222-#333 on near-white, not pure black on white)
- [ ] Color is never the only indicator (icons/labels supplement)
- [ ] Greys have slight saturation (not pure grey)
- [ ] Hue rotation applied across shade range
- [ ] Semantic colors verified against target market cultural associations
- [ ] Colors tested on actual backgrounds, not swatches in isolation
- [ ] Aesthetic choices (corners, temperature, shapes) deliberately aligned with product personality
- [ ] Nature-inspired palettes considered for stress-reduction contexts

---
---

# Chapter 6: Spacing & Depth

Use shadows, borders, backgrounds, and layering to create visual depth and spatial relationships between elements without relying on flat 2D decoration alone.

**When to Use:**
- Adding shadows or elevation to cards, modals, dropdowns
- Designing empty states and background treatments
- Choosing between borders, shadows, and spacing for separation
- Creating layered interfaces with overlapping elements
- Spacing flow content in articles and content areas

---

## Quick Reference

| Concept | Value |
|---|---|
| Shadow levels | 5 (xs, sm, md, lg, xl) |
| Shadow light source | Top-left (lighter top edge, darker bottom) |
| Max border use | Borders are a last resort; prefer shadows or spacing |
| Background gradient max hue | 30 degrees apart |
| Accent border width | 3-4px |
| Flow spacing selector | `* + *` (lobotomized owl) |

---

## Shadows and Elevation

### Rule: Emulate a Light Source

**When:** Adding visual depth to any raised element (buttons, cards, modals, tooltips).
**Do:** Apply shading as if a light source exists above and slightly in front of the interface. Raised elements have a lighter top edge and a shadow cast downward.
**Values:** Light edge: 1px inset shadow or border using rgba(255,255,255,0.1-0.2) at the top. Shadow direction: offset-y always positive (shadow goes down). Offset-x: 0 or slightly positive (light from upper-left). Never use upward shadows (negative offset-y) on standard elements.
**Don't:** Apply shadows inconsistently — one card with shadow going down, another going right. Inconsistent light direction breaks the spatial metaphor.

### Rule: Use Shadows to Convey Elevation — 5 Levels

**When:** Differentiating interactive layers (e.g., page surface, raised card, dropdown, modal, tooltip).
**Do:** Define 5 shadow levels and assign them semantically based on how "raised" an element should feel.

**Values:**

| Level | Name | CSS box-shadow | Use for |
|---|---|---|---|
| 1 | xs | 0 1px 2px rgba(0,0,0,0.05) | Buttons, form inputs |
| 2 | sm | 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06) | Cards, raised sections |
| 3 | md | 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06) | Dropdowns, popovers |
| 4 | lg | 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05) | Modals, dialogs |
| 5 | xl | 0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04) | Notifications, toasts |

**Don't:** Use arbitrary shadow values per component. Without a defined elevation system, the interface has no consistent spatial model.

### Rule: Shadows Have Two Parts

**When:** Creating any shadow (levels 2-5).
**Do:** Combine two shadows: a large, soft shadow for ambient depth and a small, tight shadow for a crisp bottom edge. The large shadow creates atmosphere; the small shadow anchors the element.
**Values:** Large shadow: 6-25px blur, 0.05-0.1 opacity. Small shadow: 1-4px blur, 0.04-0.06 opacity. Both use offset-x: 0 and positive offset-y. Example: `box-shadow: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)`.
**Don't:** Use a single shadow with high blur and high opacity. Single-shadow elements look like they are floating in a void rather than resting on a surface.

---

## Depth Without Shadows

### Rule: Even Flat Designs Have Depth

**When:** Building a flat/minimal interface where drop shadows feel too heavy.
**Do:** Create depth using color instead of shadows. Use lighter backgrounds for raised elements and darker backgrounds for recessed areas. Use solid-color offset shadows for a graphic style.
**Values:** Raised element: background #FFFFFF on page background #F3F4F6 (one shade lighter). Recessed element: background #F3F4F6 on page #FFFFFF (one shade darker). Solid shadow (flat style): `box-shadow: 4px 4px 0 #000000` with a border.
**Don't:** Build a completely flat interface with no depth cues. Without any depth, users cannot distinguish interactive elements from static content.

### Rule: Overlap Elements to Create Layers

**When:** A section or card layout feels flat despite proper shadows.
**Do:** Offset elements so they partially overlap adjacent sections or break out of their containers. Images that extend beyond a card edge, or cards that overlap a section divider, create strong depth.
**Values:** Overlap: 16-32px beyond the parent container using negative margins or absolute positioning. Use z-index: 10 for the overlapping element. Add a shadow (level 2-3) to the overlapping element to reinforce the layer.
**Don't:** Overlap without z-index and shadow. Overlapping elements that appear to be on the same plane create visual confusion rather than depth.

---

## Borders and Separation

### Rule: Use Fewer Borders

**When:** Separating cards, list items, form sections, or sidebar from content.
**Do:** Try these alternatives before reaching for a border: (1) Use a box shadow. (2) Use different background colors for adjacent sections. (3) Increase spacing between elements. Borders add visual noise; these alternatives separate content more cleanly.
**Values:** Instead of `border: 1px solid #E5E7EB` between list items, try: `padding: 16px 0` with no border. Or: alternating backgrounds #FFFFFF and #F9FAFB. Or: `box-shadow: 0 1px 2px rgba(0,0,0,0.05)` on cards. Use borders only when the above three options are insufficient.
**Don't:** Default to borders for every separation need. An interface with borders on every card, list item, section, and sidebar looks like a wireframe.

### Rule: Accent Borders for Visual Interest

**When:** A card, alert, nav item, or section needs a subtle decorative emphasis beyond background and shadow.
**Do:** Add a short, thick, colored border on one side only. Top of cards, left side of active navigation items, left of alerts, bottom of tab indicators.
**Values:** Width: 3-4px. Color: brand primary color for active states; semantic color for alerts (red for error, green for success). Position: `border-left: 4px solid hsl(210, 80%, 50%)` or `border-top: 3px solid hsl(210, 80%, 50%)`. The accent border replaces a full border — do not combine with a 1px border on all sides.
**Don't:** Add accent borders on multiple sides. A card with both a left and top accent border looks broken, not decorated.

---

## Flow Spacing

### Rule: Owl Selector Flow System

**When:** Spacing flow content (paragraphs, headings, images, blockquotes) in article/content areas.
**Do:** Use the "lobotomized owl" selector (`* + *`) to apply consistent vertical spacing only between successive elements. Set spacing as a multiple of line-height. Use `em` on headings so they appear closer to the content they introduce. Remove empty elements from the flow.
**Values:** `main * + * { margin-top: 1.5rem; }` (matching line-height). Exceptions: `li, dt, dd, br, th, td { margin-top: 0; }`. Headings: `* + h2, * + h3 { margin-top: 1.5em; }` (em, not rem — scales with heading size). Non-paragraph elements: `main * + *:not(p) { margin: 3rem 0; }`. Empty elements: `main :empty { display: none; }`.
**Don't:** Apply margin directly to individual elements (causes doubling with container padding). Don't use inconsistent spacing units across flow content. Don't manually space each element type when a single flow rule handles it.

---

## Backgrounds and Decoration

### Rule: Decorate Backgrounds

**When:** A section feels visually empty or monotonous despite correct content and spacing.
**Do:** Apply one of these background treatments: (1) A subtle color change (white section alternating with #F8FAFC section). (2) A subtle gradient spanning 2 adjacent colors. (3) A geometric pattern at low opacity (5-10%).
**Values:** Color change: use adjacent shades (50 and 100 from your grey palette). Gradient: max 30 degrees of hue difference (e.g., hsl(210, 60%, 50%) to hsl(230, 60%, 45%)). Pattern opacity: 5-10% max. SVG patterns work well (diagonal lines, dots, crosses).
**Don't:** Use high-contrast or busy patterns. Backgrounds should be felt, not seen — if the user's eye is drawn to the background instead of the content, it is too strong.

### Rule: Don't Overlook Empty States

**When:** A list, table, dashboard, or gallery can display zero items.
**Do:** Design a specific empty state with: (1) A simple illustration or icon (64-128px). (2) A brief description of what will appear here. (3) A primary action CTA to add the first item. (4) Hide filters, sort controls, and column headers when there is no content to filter or sort.
**Values:** Illustration: 64-128px, muted colors (use grey-400 or brand-100). Text: 16-18px, color grey-600, max 2 lines, center-aligned. CTA button: primary style, centered below text, 16px gap from text. Remove empty table headers and filter bars.
**Don't:** Show an empty table with column headers and zero rows, or a blank white area with no explanation. Users interpret empty containers as bugs.

---

## Platform Notes

| Platform | Shadow system | Depth convention |
|---|---|---|
| Web | box-shadow (CSS) | 5-level elevation scale |
| iOS | layer.shadow* properties | UIKit defines 3 elevation levels |
| Android | elevation property (dp) | Material Design: 0-24dp elevation |

---

## Checklist

- [ ] 5 shadow levels defined with two-part shadows
- [ ] Consistent light source direction (top-left) across all shadows
- [ ] Borders used only when spacing/shadows/backgrounds are insufficient
- [ ] Accent borders are single-sided, 3-4px width
- [ ] Empty states have illustration + description + CTA
- [ ] Background decorations are subtle (5-10% opacity patterns, adjacent shade colors)
- [ ] Gradients span max 30 degrees of hue
- [ ] Overlapping elements have proper z-index and shadow
- [ ] Flow content uses owl selector (`* + *`) for consistent vertical spacing

---
---

---

# Chapter 7: Component Patterns

Concrete implementation patterns for common UI components. Each component includes the correct pattern and the anti-pattern to avoid. Values are specific and implementation-ready. Components should follow orchestration principles: related actions use consistent patterns, controls cluster near the content they affect, and the interface recedes so the user's task stays in focus.

**When to Use:**
- Building any standard UI component from scratch
- Reviewing existing components for correctness
- Choosing between component variations
- Fixing components that "look off" without a clear reason
- Establishing or auditing a design system

---

## Quick Reference

| Component | Key decision | Default |
|---|---|---|
| Buttons | 3-tier hierarchy | Solid primary, outline secondary, text tertiary |
| Form inputs | Border style | 1px border or soft bg + bottom border |
| Cards | Container style | Subtle shadow, no border |
| Navigation | Active indicator | Bottom border (tabs), left bar (vertical) |
| Modals | Overlay | Dark overlay, centered, max-width 500px |
| Tables | Row separation | Subtle zebra striping or border-bottom |
| Alerts | Structure | Icon + accent border + message |
| Badges | Shape | Pill (border-radius: 9999px) |
| Component hierarchy | 5 levels | Atoms > Molecules > Organisms > Templates > Pages |

---

## Design System Foundations

### Rule: Atomic Design Component Hierarchy

**When:** Building or organizing a component library, design system, or any reusable UI architecture.
**Do:** Structure components in five levels of increasing complexity: (1) Atoms — indivisible UI elements: buttons, inputs, labels, icons, colors, fonts. (2) Molecules — simple groups of atoms functioning as a unit: a search field (label + input + button), a media object (image + text). (3) Organisms — complex groups of molecules forming a distinct section: a header (logo + nav + search molecule), a product card grid. (4) Templates — page-level structures showing content areas with placeholder content. (5) Pages — templates with real content, showing the final result and edge cases.
**Values:** Atoms should be maximally reusable — no business logic, pure presentation. Molecules combine 2-5 atoms with a single responsibility. Organisms represent a self-contained UI region. Templates validate layout relationships. Pages catch edge cases (long names, missing images, empty states). Build bottom-up: atoms first, then molecules, then organisms.
**Don't:** Skip levels — don't jump from atoms to full pages. Don't put business logic in atoms or molecules. Don't treat this as a rigid taxonomy — the value is in thinking about component composition, not in labeling everything perfectly.

### Rule: Interface Inventory Before Design System

**When:** Starting a design system, refactoring an existing UI, or auditing visual consistency across a product.
**Do:** Before building a design system, conduct an Interface Inventory: screenshot every unique instance of each component type across your entire product. Group screenshots by category: buttons, form fields, navigation, headings, modals, cards, icons, colors. The inventory will reveal inconsistency — you likely have 5 button styles and 8 shades of grey when you thought you had 1-2 of each.
**Values:** Categories to inventory: global elements (header, footer), navigation, image styles, icon styles, form elements, button styles, headings, text blocks, list styles, interactive components, colors, animations. Present the inventory as a visual wall — the inconsistency becomes immediately obvious. Use findings to prioritize which components to standardize first (most-used, most-inconsistent).
**Don't:** Skip the inventory and jump straight to building a design system. Don't do the inventory alone — include developers, designers, and product managers. Don't treat it as a one-time exercise — repeat quarterly as the product evolves.

### Rule: Single Responsibility for Interactive Components

**When:** Scoping what a single UI component, control, or interactive element should do.
**Do:** Each interactive component should do exactly one thing well. A toggle mutes/unmutes. A search bar searches. A like button likes. When a component tries to do multiple things, it becomes confusing and error-prone. If you find yourself explaining "this button does X, but also Y, and sometimes Z," the component needs to be split.
**Values:** One component = one verb (save, send, delete, toggle, search, filter, sort). If a component needs to do two things, it is two components (or a molecule composed of two atomic components). Test: can you name the component with a single verb? If not, it is too complex.
**Don't:** Create multi-function buttons that change behavior based on context without clear indication. Don't combine unrelated actions into a single control. Don't build "god components" that handle many interaction types — decompose them.

### Rule: Component Composition Over Configuration

**When:** Deciding whether to add props/variants to an existing component or compose a new one from simpler parts.
**Do:** Prefer composing complex components from simpler ones over adding configuration flags to a single component. A card with an image is not a "Card with imageVariant=true" — it is a Card organism composed of an Image atom, a Heading atom, and a Text atom. Each piece can be tested, styled, and replaced independently.
**Values:** If a component has more than 5 configuration props, consider decomposing it into composable parts. Atoms need few or no props beyond content and variant (size, color). Molecules compose atoms and add interaction logic.
**Don't:** Create components with 15+ props that produce wildly different outputs depending on configuration. Don't use boolean flags to show/hide sections of a component — compose with or without those sections instead. Don't build monolithic "page components" that accept all data as props.

### Rule: Pattern Lab Testing — Real Content, All States

**When:** Testing components in a design system or component library before integrating into production.
**Do:** Test every component with real content, not just ideal placeholder content. For each component, verify: (1) Ideal content — the "happy path" with expected-length text. (2) Too-long content — 200-character name, 3-paragraph description, title that wraps to 4 lines. (3) Too-short content — single-character inputs, one-word titles. (4) Missing content — null images, empty descriptions, undefined optional fields. (5) Internationalized content — German (longer words), Japanese (different character width), RTL languages.
**Values:** Create a "stress test" dataset for every component: shortest, longest, weirdest, and most realistic content variants. Test at all breakpoints with each variant. The component is not done until it handles edge-case content gracefully (truncation with ellipsis, responsive wrapping, meaningful fallbacks for missing data).
**Don't:** Test only with "Lorem ipsum" or ideal-length placeholder content. Don't assume names are 10-20 characters. Don't assume images always exist. Don't ship components that break with real production data.

---

## Affordances and Interaction Idioms

### Rule: Affordances and Signifiers

**When:** Designing any interactive element (button, handle, link, draggable item, toggle).
**Do:** Distinguish between affordance (what an object CAN do) and signifier (what TELLS the user it can do it). Make every interactive element's action perceivable through visual signifiers: underlines for links, shadows for draggables, raised appearance for buttons. If it looks clickable, it must be clickable; if it looks draggable, it must be draggable.
**Values:** Buttons: filled + shadow for primary, outlined for secondary. Links: underline or primary color in text context. Draggable: 6-dot grip icon. Toggles: clear on/off with color + position change.
**Don't:** Create "mystery meat" navigation — elements with no visible indication of interactivity. Don't rely on cursor change as the only affordance (touch has no hover). Don't remove signifiers for aesthetic minimalism at the cost of usability.

### Rule: Idiomatic Design over Intuitive Design

**When:** Choosing interaction patterns, control types, and UI conventions.
**Do:** Prefer established idioms (hamburger menu = navigation, X = close, swipe-to-delete, pull-to-refresh) — they are learned once and recognized everywhere. Use platform-native idioms: follow iOS conventions on iOS, Android on Android, web conventions on web. New idioms must be simple enough to learn in one encounter.
**Values:** Learnability, cross-application consistency, reduced cognitive overhead. When introducing a new interaction, teach it once with a tooltip on first encounter, then rely on the user remembering.
**Don't:** Invent novel interaction patterns when a standard idiom exists (custom scrollbars, non-standard gestures). Don't claim an interface should be "intuitive" — almost nothing is; it is either learned (idiomatic) or analogous to the physical world (metaphoric). Don't use the same visual idiom for different actions across your app.

### Rule: Uncanny Valley — Anthropomorphic UI

**When:** Adding avatars, illustrations, chatbot personas, or AI character representations to an interface.
**Do:** Favor abstract or stylized representations over photorealistic ones. If the likeness is very close to human but not perfect, it triggers discomfort. Use simple illustrations, geometric avatars, or clearly-stylized characters for AI assistants and bots.
**Values:** Abstract (cartoon/icon) = safe. Stylized (illustrated human) = safe. Near-photorealistic but artificial = uncanny valley (avoid). Indistinguishable from real = safe but costly.
**Don't:** Use AI-generated photorealistic faces for avatars or personas — they trigger uncanny valley. Don't animate chatbot avatars with jerky or slightly-off facial expressions. Don't use stock photos with artificial smiles as placeholder avatars.

---

## Product Personality

### Rule: Signature Moments as Product Differentiators

**When:** Identifying which interactions in your product should receive extra design investment to become memorable, brand-defining moments.
**Do:** Choose 1-3 interactions that users encounter frequently and invest disproportionate design effort into making them delightful. These are "Signature Moments" — interactions so well-crafted they become synonymous with your product. Candidates: the primary action (sending a message, completing a task), the first-use moment, the success/completion state.
**Values:** Criteria for selecting Signature Moments: (1) High frequency — users encounter it daily. (2) Emotional peak — the moment of accomplishment or delight. (3) Brand-aligned — expresses your product's personality. Invest 10x the design time on Signature Moments vs. routine interactions.
**Don't:** Try to make every interaction a Signature Moment — if everything is special, nothing is. Don't copy another product's Signature Moment. Don't prioritize delight over usability — the interaction must work perfectly first. Don't add Signature Moments to error states.

### Rule: Design Persona Document

**When:** Starting a new product or redesigning an existing one — defining the personality and voice of the interface.
**Do:** Create a Design Persona document that defines the brand's personality as if it were a person. Include: (1) Brand name and overview — what your product does in human terms. (2) Personality image — a real person or character who represents the tone. (3) Brand traits — 5-7 adjectives formatted as "X, but not Y" (e.g., "Fun, but not childish. Powerful, but not complicated"). (4) Personality map — where you fall on spectrums (formal-casual, serious-playful). (5) Voice — copy examples for success, error, and failure states. (6) Anti-voice — what the persona would never say.
**Values:** Minimum 3 copy examples covering success, error, and critical failure states. The persona must be authentic — reflect who you actually are, not who you wish you were. Test persona fit: would this voice feel natural in a billing page? In a celebration moment?
**Don't:** Skip the "trait to avoid" — it prevents personality drift. Don't let the persona override usability — clarity always beats personality. Don't use the persona to justify unprofessional copy in serious contexts (billing errors, data loss, security alerts need formal clarity regardless of persona).

### Rule: Personality Gradient

**When:** Implementing personality/humor in an application with both marketing pages and task-focused workflows.
**Do:** Apply personality on a gradient: heavy on marketing/landing pages, moderate in admin/dashboard, minimal-to-none in core task workflows. The user should never feel personality interferes with getting work done.
**Values:** Marketing pages: full personality. Dashboard/admin: moderate (informal tone, occasional humor). Core workflow (forms, checkout, data entry): professional, clear, personality-free.
**Don't:** Apply uniform personality density across all contexts. Don't use humor in error states of critical workflows. Don't assume that playful copy works everywhere just because it works on the landing page.

---

## Buttons

### Rule: Button Hierarchy

**When:** Any view contains clickable actions.
**Do:** Implement three tiers with distinct visual treatments.

| Tier | Background | Border | Text color | Use |
|---|---|---|---|---|
| Primary | Brand color solid | None | #FFFFFF | 1 per view, main CTA |
| Secondary | Transparent | 1px solid #D1D5DB | #374151 | Supporting actions |
| Tertiary | None | None | Brand color | Cancel, minor actions |

**Values:** All buttons: font-weight: 600, border-radius: 6px, cursor: pointer. Sizes: Small: padding 6px 12px, font 14px. Medium: padding 10px 20px, font 14px. Large: padding 12px 24px, font 16px. Min-width: 80px for small, 100px for medium, 120px for large.
**Don't:** Use two primary buttons side by side. Use outline for destructive secondary actions, not red solid (reserve red solid for delete confirmations only).

### Rule: Button Icon Placement

**When:** A button includes an icon alongside text.
**Do:** Place leading icons (before text) for actions where the icon represents the object (+ Add, trash Delete). Place trailing icons (after text) for directional actions (Next arrow-right, Open external-link). Center the icon vertically with the text.
**Values:** Icon size: 16px for small buttons, 20px for medium/large. Gap between icon and text: 8px. Icon color: inherit from text color. Do not use icons without text labels unless the icon is universally understood (close X, hamburger menu, search magnifier).
**Don't:** Use both a leading and trailing icon on the same button. One icon per button maximum.

---

## Form Inputs

### Rule: Input Border Styles

**When:** Styling text inputs, selects, and textareas.
**Do:** Choose one style and apply it consistently across all form elements.

| Style | CSS | Best for |
|---|---|---|
| Standard border | border: 1px solid #D1D5DB, border-radius: 6px | Most applications |
| Soft background | background: #F3F4F6, border: none, border-bottom: 2px solid #D1D5DB | Modern/minimal |
| Underline only | border: none, border-bottom: 1px solid #D1D5DB | Dense forms |

**Values:** Height: 40px (medium), 36px (small), 48px (large). Padding: 8px 12px. Font-size: 14-16px. Focus state: border-color: brand color, box-shadow: 0 0 0 3px rgba(brand, 0.15). Error state: border-color: #EF4444, box-shadow: 0 0 0 3px rgba(239,68,68,0.1).
**Don't:** Mix input styles within the same form. A border input next to an underline input looks like a bug.

### Rule: Label Positions

**When:** Pairing labels with form inputs.
**Do:** Place labels above inputs for most forms (best scan pattern, works on all screen widths). Use inline/left labels only for very short forms (login, search) or settings pages with toggle switches.
**Values:** Above label: font-size: 14px, font-weight: 500, color: #374151, margin-bottom: 6px. Left-aligned label: width: 120-160px, text-align: right, padding-right: 16px, same height as input. Placeholder text: color: #9CA3AF, never use as a label replacement.
**Don't:** Use placeholder text as the only label. Placeholders disappear on input, leaving users without context. Always include a visible label.

### Rule: Don't Put Labels Inside Form Fields

**When:** Deciding label placement for form fields.
**Do:** Use visible, persistent labels above or beside inputs. Never use placeholder text as the only label — it disappears on input, fails on autofill, and is an accessibility problem.
**Values:** Persistent labels: always visible even when field has content. Placeholder: supplementary only (format hints), never the primary label.
**Don't:** Replace labels with placeholder text to save space. Don't use floating labels as sole label mechanism.

---

## Cards

### Rule: Card Structure

**When:** Displaying a content item in a collection (product, article, user profile, project).
**Do:** Use a consistent card structure: optional image (top or left), content area (title + description + metadata), optional action area (bottom). Apply a subtle shadow (level 2) or a 1px border for containment.

| Layout | Image position | Best for |
|---|---|---|
| Vertical card | Top (full width) | Product grids, blog posts |
| Horizontal card | Left (fixed 120-200px) | List views, search results |
| No image | N/A | Settings, data items |

**Values:** Border-radius: 8-12px. Padding: 16-24px (content area). Shadow: 0 1px 3px rgba(0,0,0,0.1). Image: use object-fit: cover with a fixed aspect ratio (16:9 or 4:3). Hover state: shadow level up one step, or translate-y: -2px with transition: 150ms.
**Don't:** Use both a border and a shadow on the same card. Choose one containment method. Combining them looks heavy and outdated.

---

## Navigation

### Rule: Horizontal Tab Navigation

**When:** Switching between views or content sections within a page.
**Do:** Use a bottom border indicator for the active tab. Keep tabs on a single row (use a dropdown or "More" menu if tabs exceed the width).

**Values:** Tab item: padding: 8px 16px, font-weight: 500, color: #6B7280. Active tab: color: #111827 (or brand color), border-bottom: 2px solid brand color, font-weight: 600. Hover: color: #374151, background: #F3F4F6, border-radius: 6px (top corners only). Tab bar: border-bottom: 1px solid #E5E7EB. Gap between tabs: 0-4px.
**Don't:** Use background color alone for active state (it is ambiguous — could be hover). Always include the bottom border indicator for active tabs.

### Rule: Vertical Navigation

**When:** Building a sidebar navigation for apps, dashboards, or admin panels.
**Do:** Highlight the active item with a left accent border or a filled background. Include an icon (20px) + text label for each item.

**Values:** Nav item: padding: 8px 12px, font-size: 14px, color: #374151, border-radius: 6px. Active: background: #EFF6FF (brand-50), color: brand-700, font-weight: 600, border-left: 3px solid brand-500 OR background: brand-50 with no border. Hover: background: #F3F4F6. Icon-to-text gap: 12px. Section divider: 24px vertical spacing + optional section label in 12px, font-weight: 600, color: #9CA3AF, text-transform: uppercase, letter-spacing: 0.05em.
**Don't:** Use indentation alone to show nested items — combine with a lighter weight or smaller size. Do not exceed 2 nesting levels in sidebar nav.

---

## Modals

### Rule: Modal Implementation

**When:** Displaying content that requires user attention or a decision before continuing.
**Do:** Use a dark semi-transparent overlay behind the modal. Center the modal vertically and horizontally. Trap focus within the modal. Close on overlay click and Escape key.

**Values:** Overlay: background: rgba(0, 0, 0, 0.5), position: fixed, z-index: 50. Modal: background: #FFFFFF, border-radius: 12px, max-width: 500px (small), 700px (medium), 900px (large), padding: 24px, box-shadow: level 4 (lg). Margin from viewport edge: min 16px on all sides. Max-height: 85vh with overflow-y: auto for content.
**Don't:** Use a modal when a slide-over panel, inline expansion, or new page would work. Modals interrupt flow — reserve them for confirmations, short forms, and decisions that block the main task.

### Rule: Modal Button Placement

**When:** A modal has confirm/cancel actions.
**Do:** Place buttons at the bottom-right of the modal. Primary action (Confirm, Save, Submit) on the right. Secondary action (Cancel) on the left of the primary button.
**Values:** Button container: display: flex, justify-content: flex-end, gap: 12px, padding-top: 24px, border-top: 1px solid #E5E7EB, margin-top: 24px. Destructive confirms: use red primary button with confirmation text ("Delete 3 items" not just "Delete").
**Don't:** Place buttons at the top of the modal, centered, or full-width stacked. Bottom-right is the established convention — users expect it there.

---

## Tables

### Rule: Table Styling

**When:** Displaying structured data in rows and columns.
**Do:** Use subtle row separation (zebra striping or bottom borders, not both). Left-align text, right-align numbers. Include adequate cell padding.

**Values:** Header row: background: #F9FAFB, font-weight: 600, font-size: 12px, text-transform: uppercase, letter-spacing: 0.05em, color: #6B7280, padding: 12px 16px. Body row: padding: 12px 16px, font-size: 14px, color: #111827. Zebra stripe: every other row background: #F9FAFB. OR border-bottom: 1px solid #F3F4F6 (not both). Hover row: background: #F3F4F6.
**Don't:** Use heavy borders (1px solid #000) on all cells. Grid-style borders make tables look like spreadsheets. Use subtle separation only.

### Rule: Table Content Enhancement

**When:** A table row contains an image, avatar, or combines multiple pieces of information.
**Do:** Combine related data in a single column to reduce column count. Show an avatar + name + email in one cell. Use small text (12px, grey) for secondary information stacked below the primary value.

**Values:** Avatar in table: 32-40px, border-radius: 50%, margin-right: 12px, vertically centered. Name + email cell: Name in 14px #111827, email in 12px #6B7280, stacked vertically with 2px gap. Status in table: use a badge component (see Badges below).
**Don't:** Create separate columns for first name, last name, and email when they could be one "User" column. Excessive columns force horizontal scrolling or cramped cells.

---

## Alerts

### Rule: Alert Structure

**When:** Showing a status message, validation feedback, or system notification inline on the page.
**Do:** Use a colored left accent border, a matching background tint, an icon, and text. Structure: icon (left) + title (bold, optional) + description.

| Severity | Border color | Background | Icon |
|---|---|---|---|
| Info | hsl(210, 80%, 50%) | hsl(210, 80%, 96%) | info-circle |
| Success | hsl(142, 70%, 40%) | hsl(142, 70%, 96%) | check-circle |
| Warning | hsl(38, 90%, 50%) | hsl(38, 90%, 96%) | exclamation-triangle |
| Error | hsl(0, 80%, 55%) | hsl(0, 80%, 96%) | x-circle |

**Values:** Border-left: 4px solid [severity color]. Border-radius: 6px (right side only, or all corners). Padding: 12px 16px. Icon: 20px, color matching border. Title: 14px, font-weight: 600, color: [severity-800]. Description: 14px, font-weight: 400, color: [severity-700].
**Don't:** Use only color to differentiate severity levels. Always include an icon and a text description for accessibility.

---

## Badges

### Rule: Badge Styling

**When:** Displaying status labels, counts, tags, or categories inline.
**Do:** Use pill-shaped badges with a soft (tinted) background and darker text of the same hue. Avoid solid saturated backgrounds with white text for inline badges — they are too visually heavy.

**Values:** Shape: border-radius: 9999px (pill). Padding: 2px 10px. Font-size: 12px. Font-weight: 500. Soft style: background: hsl(H, S%, 92%), color: hsl(H, S%, 30%). Example: blue badge: background: #DBEAFE, color: #1E40AF. Line-height: 1.5 (so badge height is consistent at ~20px). For counts: min-width: 20px, text-align: center.
**Don't:** Use large badges (over 14px font) or solid saturated badges inline with body text. Oversized badges pull attention away from the content they annotate.

---

## Empty States

### Rule: Empty State Design

**When:** A list, table, grid, or dashboard section has zero items to display.
**Do:** Replace the empty container with a centered composition: illustration/icon + headline + description + CTA button. Hide all filters, sort controls, column headers, and pagination.

**Values:** Container: text-align: center, padding: 48px 24px. Illustration/icon: 64-128px, color: #9CA3AF or brand-200. Headline: 18px, font-weight: 600, color: #111827, margin-top: 16px. Description: 14px, color: #6B7280, max-width: 320px, margin: 8px auto 0. CTA: primary button, margin-top: 24px.
**Don't:** Show a table with column headers and zero rows. Do not show filter/sort controls when there is nothing to filter. Do not show just the text "No results" without a path forward.

---

## Images and Icons

### Rule: User-Uploaded Image Containers

**When:** Displaying user-uploaded images (avatars, product photos, covers) where dimensions are unpredictable.
**Do:** Use a fixed-size container with `object-fit: cover` to crop images to a consistent shape. Add a subtle inner shadow or border to prevent images with white/light edges from bleeding into the background.

**Values:** Container: fixed width and height, overflow: hidden, border-radius: 8px (cards) or 50% (avatars). Image: width: 100%, height: 100%, object-fit: cover. Inner shadow: box-shadow: inset 0 0 0 1px rgba(0,0,0,0.08). Avatar sizes: 24px (inline), 32px (list), 40px (table), 64px (profile card), 96-128px (profile page).
**Don't:** Let user-uploaded images set their own dimensions. Uncontrolled images break layouts with unexpected aspect ratios or sizes.

### Rule: Icon Scaling

**When:** You need a larger icon than the icon set provides (e.g., you have 16-24px icons but need a 48px icon for an empty state or feature section).
**Do:** Do not scale up a small icon — it will look blurry or have inconsistent stroke widths. Instead, place the icon at its native size inside a shaped container (circle or rounded square) with a tinted background.
**Values:** Icon: keep at 20-24px. Container: 48-64px, background: brand-100 or grey-100, border-radius: 12px (rounded square) or 50% (circle). Center the icon in the container using flexbox. Container adds visual weight without distorting the icon.
**Don't:** Scale a 16px icon to 48px. Stroke-based icons designed for 16px have 1-2px strokes that become blurry 3-6px strokes at 3x scale. The proportions look wrong.

---

## Platform Notes

| Component | Web | iOS | Android |
|---|---|---|---|
| Buttons | border-radius: 6px | cornerRadius: 10 | cornerRadius: 8dp |
| Modals | position: fixed | UIViewController.present | DialogFragment |
| Navigation | flexbox tabs | UITabBarController | BottomNavigationView |
| Cards | box-shadow | layer.shadow | CardView elevation |
| Alerts | div with role="alert" | UIAlertController (system) | Snackbar / custom view |

---

## Checklist

- [ ] Only 1 primary (solid) button per view
- [ ] All interactive elements have visible affordances (no mystery meat)
- [ ] Form inputs use a single consistent border style
- [ ] Labels are above inputs (or intentionally inline for short forms)
- [ ] Labels are never replaced by placeholder text alone
- [ ] Cards use either shadow or border, not both
- [ ] Active navigation state has a clear indicator (border or background)
- [ ] Modals have overlay, max-width, focus trap, and escape-to-close
- [ ] Tables use either zebra striping or bottom borders, not both
- [ ] Alerts include icon + accent border + text (not color alone)
- [ ] Badges use soft/tinted backgrounds, not solid saturated fills
- [ ] Empty states have illustration + description + CTA, with filters hidden
- [ ] User-uploaded images are in fixed containers with object-fit: cover
- [ ] Icons are not scaled up — enclosed in shaped containers instead
- [ ] Established idioms used over novel interaction patterns
- [ ] AI/bot avatars use stylized representations, not near-photorealistic
- [ ] Components follow atomic hierarchy (atoms > molecules > organisms)
- [ ] Each interactive component has a single responsibility (one verb)
- [ ] Complex components use composition over configuration (< 5 props per atom)
- [ ] Components tested with real content: long, short, missing, and internationalized
- [ ] Interface inventory conducted before building design system
- [ ] 1-3 Signature Moments identified and invested in
- [ ] Design Persona document created with traits, voice, and anti-voice
- [ ] Personality applied on a gradient: heavy on marketing, minimal in workflows

---

---

# Chapter 8: Navigation & Information Architecture

Every page must be self-evident. If users have to think about where they are, how they got there, or what to do next, the navigation has failed. Good information architecture makes the right path obvious and every other path discoverable.

**When to Use:**
- Designing site-wide navigation systems
- Structuring content hierarchies and page layouts
- Building search interfaces
- Creating landing pages or home screens
- Auditing existing IA for usability problems

| Quick Reference | Value |
|----------------|-------|
| Max primary nav items | 5-7 |
| Max navigation depth | 3 levels before users lose context |
| Search box min width | 27 characters visible |
| Breadcrumb separator | `>` (not `/`, not `>>`) |
| Page load for navigation | < 1 second perceived |
| Home link | Logo in top-left, always |
| Trunk test items | 6 (site ID, page name, sections, local nav, "you are here", search) |
| Organization strategies | 5: Category, Time, Location, Alphabet, Continuum |

---

## Self-Evident Pages

### Rule: Don't Make Me Think

**When:** Designing any page or screen.
**Do:** Make every page self-explanatory. A user arriving on any page should immediately know: what site this is, what page they're on, what their options are, and how to use them.
**Values:** Target 0 seconds of deliberation for primary actions. If a user pauses to figure out what's clickable, the design has failed.
**Don't:** Rely on instructions, tooltips, or onboarding tours to explain navigation. If you need to explain it, redesign it.

### Rule: Users Scan, They Don't Read

**When:** Laying out any page with text content.
**Do:** Design for F-pattern and Z-pattern scanning. Use clear visual hierarchy: large headings, bold key phrases, bulleted lists, short paragraphs (3-4 lines max). Place critical information in the first two words of headings and list items.
**Values:** Users read 20-28% of words on an average page. Headlines get 80% attention, body text gets 20%.
**Don't:** Write walls of text. Don't bury key information in the middle of paragraphs. Don't use uniform text styling that gives no visual entry points.

### Rule: Billboard Design Model

**When:** Designing any page that users might see for the first time.
**Do:** Communicate the page's purpose in under 3 seconds. Use a clear headline, a dominant visual element, and a single obvious action. Think of each page as a billboard seen at highway speed.
**Values:** 3 seconds to communicate purpose. 50 milliseconds for first impression (aesthetic judgment).
**Don't:** Crowd the page with competing messages. Don't use clever or ambiguous headlines that require interpretation.

### Rule: Trunk Test

**When:** Auditing or reviewing navigation on any page.
**Do:** The acid test: pick any page at random, squint, and verify you can instantly identify: (1) Site ID, (2) Page name, (3) Sections (primary nav), (4) Local navigation, (5) "You are here" indicators, (6) Search. All 6 must be identifiable without close reading.
**Values:** 6 items must be findable at a glance. Apply to deep pages, not just the home page.
**Don't:** Only test the home page. Don't rely on subtle visual cues.

---

## Visual Hierarchy & Content Structure

### Rule: Create Effective Visual Hierarchies

**When:** Organizing content on any page.
**Do:** Use size, color, contrast, spacing, and indentation to signal relationships. Nest related content visually. More important = larger, higher contrast, more whitespace. Use established conventions (blue underlined = link, X = close).
**Values:** 3-4 levels of hierarchy maximum. Each level must be visually distinct: heading (24px+), subheading (18-20px), body (16px), secondary (14px).
**Don't:** Create more than 4 levels of visual hierarchy. Don't use subtle differences (14px vs 15px) to signal different levels. Don't break conventions unless you have a measurably better alternative.

### Rule: Omit Needless Words

**When:** Writing any UI text — navigation labels, headings, descriptions, instructions, error messages.
**Do:** Cut 50% of the text, then cut 50% again. Remove happy-talk (introductory text that says nothing), instructions that are obvious from context, and marketing fluff in functional areas.
**Values:** Navigation labels: 1-2 words. Button text: 1-3 words. Instructional text: 1 sentence max. Page descriptions: 15 words max.
**Don't:** Write "Welcome to our search feature, where you can find anything on our site" when a search box with placeholder text "Search" does the job.

### Rule: Mindless Choices Are Free

**When:** Users must navigate through multiple steps or click through layers.
**Do:** Make each click require zero thought. A sequence of 5 mindless, obvious clicks is better than 1 click that requires deliberation. Label each choice clearly so the correct path is immediately apparent.
**Values:** 0 seconds of deliberation per click. Number of clicks matters less than cognitive cost per click.
**Don't:** Collapse navigation depth to reduce clicks if it makes choices ambiguous. Don't create mega-menus with 50+ options to eliminate a navigation level.

---

## Information Organization

### Rule: Five Hat Racks (LATCH)

**When:** Organizing any collection of items, navigation options, or data for display.
**Do:** Choose one of exactly five organizational strategies: **Category** (by similarity), **Time** (chronological), **Location** (geographical/spatial), **Alphabet** (A-Z), or **Continuum** (ranked by magnitude like price, rating, popularity). These are the only five ways to organize information. Select the one that best matches user intent.
**Values:** Category for shopping/browsing (e.g., product types). Time for activity feeds and history. Alphabet for reference lists with 20+ items. Continuum for comparison (sort by price, rating). Location for maps or store finders.
**Don't:** Mix organizational strategies within the same level of a hierarchy. Don't default to alphabetical when category or continuum would serve users better.

### Rule: Browsing vs Searching vs Discovery

**When:** Designing product listings, content feeds, or any page with multiple items to explore.
**Do:** Identify which user behavior the page primarily serves, and optimize for it:
  - **Browsing** (exploring without a goal): Use visual, scannable layouts with emotional appeal. Grid of images. Don't overcrowd.
  - **Searching** (looking for something specific): Use structured, filterable layouts with clear attributes. Consistent item cards with key specs visible. Avoid staggered/Pinterest layouts.
  - **Discovery** (finding things they didn't know they wanted): Place new/recommended items alongside items the user is already looking for. Do NOT rely on menu items, banners, or site-wide promotions.
**Values:** Browsing = emotional imagery first. Searching = attributes and filters first. Discovery = contextual recommendations ("You might also like") placed adjacent to active content, not in banners.
**Don't:** Use banner ads to drive discovery — banner blindness makes them invisible. Don't expect experienced users to explore menus for new features — they only use features they already know.

---

## User Behavior Patterns

### Rule: Satisficing (First Reasonable Option Wins)

**When:** Designing any page with multiple options, links, or actions.
**Do:** Users don't choose the best option — they pick the first reasonable one. Place the optimal/recommended option first in the scan path and make it visually dominant.
**Values:** Position and visual prominence determine which option gets chosen. Users satisfice — they pick the first reasonable match.
**Don't:** Assume users will compare all options. Don't bury the best option in the middle.

### Rule: Muddling Through

**When:** Designing any multi-step flow or complex interface.
**Do:** Users form vague, often incorrect mental models and persist with them. Ensure the interface works even when users take suboptimal paths. Make recovery from wrong turns easy.
**Values:** The muddling-through path must work. If users need instructions, redesign the interface.
**Don't:** Design only for the ideal user path. Don't assume users read onboarding.

### Rule: Users Don't Go Backward

**When:** Designing multi-step flows, site navigation, or content hierarchies.
**Do:** Design navigation as forward-only loops: Page A links to B, B links to C, C links back to A. Every screen should provide clear forward navigation options. If users need to revisit earlier content, provide explicit forward links, not reliance on the back button.
**Values:** If >15% of users hit the back button in testing, the current page is failing to provide clear next steps. Every page must answer: "What do I do next?" with visible forward options.
**Don't:** Design hierarchies that require the back button to navigate between siblings. Don't assume users will retrace their steps — each back-button press increases abandonment probability.

### Rule: Desire Line (Follow the Worn Path)

**When:** Redesigning existing interfaces or analyzing user behavior patterns.
**Do:** Study actual usage data (heatmaps, click tracking, session recordings) before redesigning. Treat unexpected user behaviors as design input, not as errors to prevent. If users consistently use a feature in an unintended way, redesign to support that usage pattern.
**Values:** Use heatmaps to identify "hot" and "cold" zones. If >20% of users take an unexpected path, the design should accommodate it. If a search query appears in >5% of searches, it should be surfaced in navigation.
**Don't:** Redesign based on assumptions about how users "should" navigate. Don't add barriers to block desire lines — modify the design to incorporate them.

---

## Persistent Navigation

### Rule: Navigation Must Answer Three Questions

**When:** Designing navigation for any page (except home page and checkout/task flows).
**Do:** Every page's navigation must instantly answer: (1) Where am I? (highlighted current section, page title), (2) What are my options? (visible primary sections), (3) How do I get back? (logo links home, breadcrumbs, back buttons).
**Values:** Current location indicator: always visible, uses color + weight (not color alone). Back path: never more than 1 click to the parent level.
**Don't:** Rely on browser back button as the only way to go back. Don't show navigation that doesn't indicate current position.

### Rule: Persistent Navigation Elements

**When:** Building the global navigation bar/header.
**Do:** Include these elements on every page: (1) Logo linked to home — top left, (2) Primary navigation — top level sections, (3) Search — visible input field or prominent icon, (4) Utilities — account, cart, help. Keep navigation in the same position on every page.
**Values:** Logo: top-left corner, links to home page. Primary nav: 5-7 items maximum. Search: visible on every page. Utilities: top-right corner.
**Don't:** Hide primary navigation behind hamburger menus on desktop. Don't move navigation elements between pages. Don't remove navigation during multi-step flows without providing a way to exit.

### Rule: Navigation Landmark Must Use List Markup

**When:** Building site navigation.
**Do:** Wrap navigation links in a `<nav>` element containing a `<ul>` with `<li>` items. This provides semantic grouping, falls back gracefully without CSS (recognizable bulleted list), and communicates count and position to screen readers ("list, one of five, link, home").
**Values:** `<nav><ul><li><a href="/">Home</a></li>...</ul></nav>`. Screen reader announcement: "Navigation landmark, list, [N] of [total], link, [text]".
**Don't:** Use bare `<a>` tags or `<div>`-based navigation without list structure. Don't use ordered lists (`<ol>`) unless order is meaningful.

### Rule: Menu Button Must Have Text + Icon + Border

**When:** Implementing a hamburger/menu toggle button on mobile or responsive layouts.
**Do:** Combine the three-line icon with the text label "Menu" and a visible button border/outline. Research shows this combination is significantly better understood than icon alone. Use `<button>` (not `<div>` or `<a>`). Communicate open/closed state with `aria-expanded`.
**Values:** Button must include: (1) standard three-line icon (do not modify the icon shape), (2) text "Menu", (3) visible button border. State: `aria-expanded="false"` when closed, `aria-expanded="true"` when open. If menu has < 5 items, don't hide it behind a button at all.
**Don't:** Use icon-only menu buttons without text labels. Don't invent creative icon variations of the hamburger. Don't use `<div>` or `<a>` — use `<button>`.

### Rule: Page Name Must Match What You Clicked

**When:** Naming pages and creating link text.
**Do:** The destination page title must match the link text or button label that led to it.
**Values:** Exact match ideal. Tolerable: obviously synonymous wording. Intolerable: different topic or no page name.
**Don't:** Use one name in navigation and a different name on the page.

### Rule: You Are Here Indicators Must Be Bold

**When:** Designing current-location indicators in navigation.
**Do:** Apply at least 2 simultaneous visual distinctions: color change + bold weight, or background color + text color change. Designers chronically under-emphasize current location.
**Values:** Minimum 2 visual dimensions. Must be noticeable at arm's length.
**Don't:** Use a single subtle cue (just bold, or just a slight color shift).

### Rule: Current Page Link as Skip Link

**When:** Indicating the current page in site navigation.
**Do:** Make the current page's nav link point to `#main` instead of its own URL. This turns a redundant self-referential link into a useful skip link. Screen readers announce "same page link," implicitly communicating "you are here." Style the current link with more than just color — use underline, border, scale, or pointer.
**Values:** Current page link: `<a href="#main">About</a>`. Style: `[href="#main"] { text-decoration: underline; background: $highlight-color; }`. For SPAs where same-page links would be misleading, use `aria-describedby="current"` pointing to a `<div hidden id="current">Current page</div>`.
**Don't:** Remove the current page link from navigation — users need the "you are here" marker. Don't replace the link with a non-focusable `<span>`. Don't differentiate by color alone.

### Rule: Label Multiple Navigation Landmarks

**When:** A page has more than one `<nav>` element.
**Do:** Give each `<nav>` a unique accessible label using `aria-labelledby` (pointing to a visible heading) or `aria-label` (for a direct label). Without labels, screen readers list all nav regions identically as "Navigation."
**Values:** `<nav aria-labelledby="toc-heading"><h2 id="toc-heading">Contents</h2>...</nav>` or `<nav aria-label="Main site navigation">...</nav>`. This produces screen reader output like "Contents navigation landmark" vs "Main site navigation landmark."
**Don't:** Have multiple unlabeled `<nav>` elements — they are indistinguishable to screen reader users browsing by landmark.

### Rule: Breadcrumbs

**When:** Site has more than 2 levels of hierarchy.
**Do:** Place breadcrumbs at the top of the page, below the primary navigation. Use `>` as separator. Bold the current page name (last item). Make all items except the current page clickable links. Start with "Home" or site name.
**Values:** Separator: `>` with 8px spacing on each side. Font size: 12-14px (smaller than body). Position: top of content area, above page title.
**Don't:** Use breadcrumbs as primary navigation. Don't use separators other than `>`. Don't make the current page (last item) a link.

---

## Home Page & Search

### Rule: Home Page Must Communicate Purpose

**When:** Designing or auditing a home page.
**Do:** Answer four questions instantly: (1) What is this site? (2) What can I do here? (3) Why should I be here instead of competitors? (4) What should I do first? Use a clear tagline (6-8 words), a visible starting action, and enough content to establish credibility.
**Values:** Tagline: 6-8 words max, no jargon. Primary CTA: above the fold, 1 action only. Purpose clarity: testable in 5-second test (show page for 5 seconds, ask what the site does).
**Don't:** Use the home page as a splash page or purely decorative landing. Don't have multiple competing CTAs above the fold. Don't use mission-statement language ("Our mission is to leverage synergies...").

### Rule: Search Box on Every Page

**When:** Site has more than 50 pages of content or any form of catalog/database.
**Do:** Provide a visible search input on every page. Use a simple text field with a submit button or magnifying glass icon. Include placeholder text: "Search" or "Search [site name]". Place in the top-right area or centered in the header.
**Values:** Input width: minimum 27 characters visible. Position: consistent on every page. Label: "Search" — not "Find", "Quick Search", or "Keyword".
**Don't:** Hide search behind an icon on content-heavy sites. Don't add filters or options to the main search box — offer advanced search on a separate page. Don't return 0 results without suggestions.

### Rule: Jakob's Law

**When:** Making design decisions about layout, interaction patterns, or navigation structures.
**Do:** Match established conventions from sites your users already use. Users spend 95% of their time on other sites. Shopping cart icon for e-commerce, hamburger for mobile menu, logo-top-left for home — use what users already know.
**Values:** Follow conventions for: navigation placement, icon meanings, form patterns, gesture behaviors. Only deviate when you have usability testing data showing your approach is 2x+ better.
**Don't:** Innovate on navigation patterns without testing. Don't use custom icons when standard ones exist. Don't rename standard concepts ("Shopping Satchel" instead of "Cart").

### Rule: Information Scent

**When:** Writing link text, menu labels, or any clickable element.
**Do:** Link text must clearly predict the destination. Users follow "information scent" like animals follow a trail — each click must confirm they're getting closer to their goal. Use specific, descriptive labels.
**Values:** Link text: 2-5 words that describe the destination, not the action. Menu items: match the heading of the destination page exactly.
**Don't:** Use "Click here", "Learn more", "Read more" as link text. Don't use clever or branded names for standard sections ("The Knowledge Hub" instead of "Help Center").

### Rule: Deep Linking (Don't Leave at the Front Door)

**When:** Implementing mobile sites or handling inbound links.
**Do:** All shared URLs, email links, and social media links must resolve to specific content, even on mobile. Never redirect to home page.
**Values:** 100% of inbound links land on intended destination. Zero tolerance for home page redirects.
**Don't:** Redirect mobile users to mobile home page when they click a deep link.

---

## Usability Mindset

### Rule: Subtract Before Adding

**When:** Fixing a usability problem discovered in testing.
**Do:** Before adding anything (instructions, labels, tooltips), ask: can we remove something causing the confusion? Remove noise, unnecessary choices, and competing elements first.
**Values:** Subtraction before addition. Kayak rule: if users self-correct quickly, deprioritize the problem.
**Don't:** Add instructions as the first fix. Don't treat every stumble as critical.

### Rule: Reservoir of Goodwill

**When:** Making tradeoff decisions that might frustrate users.
**Do:** Every user arrives with a limited reservoir of goodwill. Each usability problem drains it. When it's empty, they leave. Refillable through: making top tasks dead easy, transparency about costs, graceful error recovery, real apologies. When things go wrong, respond with facts first, then regular updates. Emotional goodwill accumulated through good design acts as insurance against user abandonment during failures.
**Values:** Every hidden price, unnecessary field, or broken promise is a withdrawal. Every saved step, honest disclosure, or graceful recovery is a deposit. A single bad experience can drain to zero. Error response timing: acknowledge within 5 minutes, update every 15-30 minutes during outages. The "rosy effect" means users forget bad experiences over time if positive ones dominate. Maintain at least a 5:1 positive-to-negative experience ratio.
**Don't:** Hide support numbers. Require unnecessary info. Use faux sincerity. Put marketing in the way of tasks. Force account creation during checkout. Wait to communicate during outages — silence breeds anxiety. Don't lead with jokes when users are stressed — facts first, then levity.

---

## Platform Notes

| Platform | Navigation Convention |
|----------|----------------------|
| Web (Desktop) | Horizontal top nav, logo top-left, search top-right |
| Web (Mobile) | Hamburger menu top-left or top-right, bottom tab bar for primary actions |
| iOS | Tab bar at bottom (max 5 items), back button top-left |
| Android | Top app bar with navigation drawer, bottom navigation bar |
| CLI | `--help` flag, man pages, consistent subcommand structure |

---

## Checklist

- [ ] Every page answers: Where am I? What can I do? How do I get back?
- [ ] Primary navigation has 7 or fewer items
- [ ] Current section/page is visually indicated with 2+ visual distinctions
- [ ] Logo links to home from every page
- [ ] Search is visible on every page (sites with 50+ pages)
- [ ] Breadcrumbs use `>` separator and bold current page
- [ ] Home page communicates site purpose in under 5 seconds
- [ ] All link text describes the destination, not the action
- [ ] Navigation is in the same position on every page
- [ ] Page hierarchy uses no more than 4 visual levels
- [ ] All UI text has been cut to minimum necessary words
- [ ] Each click in a flow requires zero deliberation
- [ ] Trunk test passes on deep pages (all 6 items identifiable at a glance)
- [ ] Page names match the link/button text that led to them
- [ ] Recommended option is first in scan path and visually dominant
- [ ] Suboptimal user paths still lead to success (muddling through works)
- [ ] Usability fixes subtract noise before adding instructions
- [ ] Goodwill deposits (easy tasks, transparency) outweigh withdrawals
- [ ] All inbound/shared links resolve to specific content (no home page redirects)
- [ ] Content organized using one of the five LATCH strategies per hierarchy level
- [ ] Page optimized for the right mode: browsing, searching, or discovery
- [ ] Forward navigation options exist on every page (users don't rely on back button)
- [ ] Navigation uses `<nav>` with `<ul>` list markup
- [ ] Menu buttons include text label + icon + visible border
- [ ] Current page link styled as skip link pointing to `#main`
- [ ] Multiple `<nav>` elements each have unique accessible labels

---

---

# Chapter 9: Cognitive Load & Attention

Every interface competes for finite mental resources. Working memory holds 4 items. Attention fades after 10 minutes. Decision speed degrades logarithmically with each option added. Design for the brain's actual constraints, not its theoretical capacity.

**When to Use:**
- Simplifying complex interfaces or multi-step flows
- Deciding how many options to present simultaneously
- Optimizing system response times
- Designing dashboards, settings pages, or data-heavy screens
- Prioritizing which elements get visual emphasis
- Balancing novelty with familiarity in redesigns

| Quick Reference | Value |
|----------------|-------|
| Working memory capacity | 4 +/- 1 items |
| Decision time per option | +150ms per doubling of choices |
| System response target | < 400ms |
| Attention span per task segment | 7-10 minutes |
| Max visible groups | 4 |
| Recognition vs recall improvement | 2-3x faster task completion |
| Interface hierarchy | Functional > Reliable > Usable > Pleasurable |

---

## Working Memory & Chunking

### Rule: Miller's Law — 4 Plus or Minus 1

**When:** Presenting groups of items, navigation options, or data points that users must hold in working memory.
**Do:** Group content into chunks of 4 items (updated from the original 7 +/- 2). Phone numbers, credit card fields, navigation groups — break them into clusters of 3-4. Use visual separators (whitespace, dividers, color) to define chunks.
**Values:** 4 items per chunk. Use whitespace of 24px+ between chunks. Maximum 4 chunks visible simultaneously.
**Don't:** Present more than 4 ungrouped items that users must compare or remember. Don't rely on the outdated "7 +/- 2" for interface design — 4 is the functional limit for active manipulation.

### Rule: 4-Item Working Memory Limit

**When:** Designing any interface where users must compare, choose, or remember options.
**Do:** Limit simultaneously visible groups to 4. Pricing plans: show 3-4 tiers. Dashboard widgets: 4 per row. Filter categories: 4 visible, rest in "More". Tab groups: 4-5 max before overflow.
**Values:** 4 visible groups maximum. If more exist, use progressive disclosure, tabs, or "Show more" patterns.
**Don't:** Show 8 pricing plans side by side. Don't display 6+ dashboard sections without visual grouping. Don't present 10 filter categories simultaneously.

### Rule: Recognition Over Recall

**When:** Users must select, configure, or navigate.
**Do:** Show options instead of requiring users to remember them. Use dropdowns instead of blank text fields for known-set inputs. Show recent items, suggestions, and history. Display command palettes with searchable option lists.
**Values:** Recognition is 2-3x faster than recall. Always prefer showing the 5 most common options over an empty input field.
**Don't:** Make users type values they could select from a list. Don't hide options behind memorized keyboard shortcuts without a discoverable alternative. Don't clear user history that aids recognition.

### Rule: Schemas for Learning

**When:** Introducing new features or unfamiliar UI patterns.
**Do:** Anchor new information to something familiar. "This works like [familiar thing], except..." Use familiar metaphors and progressive complexity. Users integrate new concepts faster when they can attach them to existing mental schemas.
**Values:** Onboarding: start with most familiar feature. Use skeuomorphic cues for novel interactions. Layer complexity: basic first, advanced behind toggle.
**Don't:** Introduce multiple unfamiliar concepts simultaneously.

### Rule: Design for Re-Discovery, Not Memorization

**When:** Designing information density, notifications, or history views.
**Do:** Accept users will forget most of what they see. Provide search, recent history, and persistent access. Build UI so forgetting doesn't matter.
**Values:** Search for content with 10+ items. "Recently used" at top of long lists. Tooltips on icons. Undo instead of confirmation dialogs.
**Don't:** Require memorizing shortcuts, icon meanings, or navigation paths without discoverable alternatives.

### Rule: Knowledge in the World vs Knowledge in the Head

**When:** Deciding what information to display vs. what to expect users to remember.
**Do:** Put knowledge in the world: show keyboard shortcuts next to menu items, display format hints in input placeholders, show allowed values near inputs. Use recognition over recall: show recent items, provide autocomplete, display options rather than requiring typed commands. For expert users, allow but don't require memorized shortcuts — always provide a discoverable alternative. Combine both: labels visible by default, with the option to hide them once learned (progressive compaction).
**Values:** Reduced memory burden, accessibility for new users, efficiency for experts.
**Don't:** Require memorization of codes, shortcuts, or formats with no visible reference. Don't remove labels/hints to save space if it forces recall. Don't design only for experts who have memorized the interface (unless explicitly a power-user tool).

### Rule: Persist Prior Choices in Multi-Step Flows

**When:** Designing wizards or flows where users must remember earlier inputs.
**Do:** Display prior choices throughout the flow. Show summary sidebar, breadcrumb with values, or step indicator showing completed inputs. Users cannot hold earlier decisions in working memory while making new ones.
**Values:** Wizard sidebar: show completed step values, not just names. Checkout: order summary always visible. "You selected: X" confirmation before each step.
**Don't:** Force users to remember values from previous steps.

---

## Decision Speed

### Rule: Hick's Law

**When:** Presenting choices — menus, settings, product listings, action buttons.
**Do:** Minimize the number of options presented simultaneously. Decision time increases logarithmically: T = a + b * log2(n). Going from 2 to 4 options adds the same delay as going from 4 to 16. Group related options, use progressive disclosure, highlight recommended choices.
**Values:** Ideal: 3-5 options per decision. Maximum: 7 before categorization is needed. Highlight 1 recommended option to reduce decision time by 30-50%.
**Don't:** Present 20 options in a flat list. Don't add "just one more option" without considering cumulative decision cost. Don't assume that showing all options at once is more efficient.

### Rule: Progressive Disclosure

**When:** Interface has features or options that vary in frequency of use.
**Do:** Show only what's needed for the current step. Hide advanced options behind expandable sections, "Advanced" links, or secondary screens. Reveal complexity incrementally as users demonstrate need.
**Values:** Primary view: 3-5 options (80% use case). Secondary (1 click): 5-10 additional options. Tertiary (2 clicks): everything else. Each level should serve a smaller percentage of users.
**Don't:** Hide frequently used features behind progressive disclosure. Don't make users click through 4+ levels to reach features they use daily. Don't use progressive disclosure to hide poor organization.

### Rule: Control Allocation (Beginner vs Expert Paths)

**When:** Designing systems that will be used both by first-time and repeat users.
**Do:** Provide exactly two interaction methods per core task: one structured path for beginners (menus, wizards, guided flows) and one shortcut for experts (keyboard shortcuts, command palettes, quick actions). Conceal expert methods from beginners to avoid complexity.
**Values:** Limit to 2 methods per task. For infrequently-used systems (kiosks, checkout), design as if all users are first-time users — do not add expert shortcuts. For frequently-used systems, add customization options.
**Don't:** Provide 3+ ways to do the same thing — it adds complexity with diminishing returns. Don't design a museum kiosk or onboarding flow with expert shortcuts.

### Rule: Flexibility-Usability Tradeoff

**When:** Deciding how many features, options, or configuration settings to expose.
**Do:** When users know what they need, favor specialized, opinionated designs. When users cannot predict their needs, favor flexible designs. Recognize that flexibility always increases complexity and decreases ease of use.
**Values:** Specialized design: fewer choices, faster task completion, easier learning. Flexible design: more choices, slower task completion, steeper learning curve. As a product matures and user needs become clearer, shift toward specialization.
**Don't:** Make everything configurable by default. Don't add flexibility "just in case" — every option has a usability cost.

### Rule: Unconscious Decision-Making

**When:** Designing conversion flows, CTAs, or decision points.
**Do:** Most decisions are made unconsciously first, then rationalized. The unconscious responds to: visual weight, position, color, defaults. Optimize these before copy.
**Values:** Pre-select recommended option (users rarely change defaults). Make desired action most visually prominent. Primary CTA at natural eye-flow endpoint. Show highest price first (anchoring).
**Don't:** Rely solely on rational persuasion. Don't make all options visually equal when one is recommended.

### Rule: Emotion Is Required for Decisions

**When:** Designing decision points (plan selection, purchase, settings).
**Do:** Include emotional context alongside rational info. People with damaged emotional centers cannot make decisions even with full rational capacity. Feature tables need emotional headlines.
**Values:** Pricing: feature table + emotional headline. Plan names: evocative ("Pro", "Growth") not clinical ("Tier 2"). Include social proof near decision point.
**Don't:** Present decisions as purely rational comparisons. Don't strip emotion from B2B interfaces.

### Rule: Hyperbolic Discounting in UX

**When:** Designing flows for high-stakes or irreversible actions (account deletion, unsubscribe, data export).
**Do:** For valuable actions: minimize steps and time to completion — immediate rewards feel more valuable. For destructive actions: add deliberate friction (more steps, confirmation, cooling-off periods) so the impulsive motivation decreases. Show what the user will lose NOW, not abstract future consequences.
**Values:** Valuable action: aim for < 3 clicks to completion. Destructive action: add 2-3 extra steps with concrete loss framing ("You will lose 847 saved items"). Show social proof of loss ("12 friends will no longer see your profile").
**Don't:** Add friction to valuable actions. Don't make destructive actions emotionally charged — make them boring and lengthy so impulse fades.

---

## System Responsiveness

### Rule: Doherty Threshold

**When:** Building any interactive system — page loads, form submissions, search results, animations.
**Do:** Keep system response under 400ms to maintain user engagement and flow state. Under 100ms feels instantaneous. 100-400ms feels responsive. Above 400ms, users perceive a delay and disengage. Use loading indicators for anything over 400ms.
**Values:** Instantaneous: < 100ms. Responsive: 100-400ms (Doherty threshold). Noticeable delay: 400ms-1s (show spinner). Long operation: > 1s (show progress bar with estimate). Unacceptable: > 10s without feedback.
**Don't:** Let any user action go without visual feedback for more than 100ms. Don't show loading spinners for operations under 400ms (causes perceived slowness). Don't block the entire UI during background operations.

### Rule: Time Perception Management

**When:** Users must wait for loading, processing, or system responses.
**Do:** Manage time perception, not just actual time. Busy time feels shorter than idle time. Use skeleton screens, meaningful animations, or useful content during waits.
**Values:** Skeleton screens > spinner (reduces perceived wait ~30%). Show useful tips during long waits (>3s). Optimistic UI: show result immediately, sync in background. Determinate progress bar when duration is known.
**Don't:** Use indeterminate spinner when progress is knowable. Don't leave screen blank during loads. Don't exceed 1s without loading feedback.

### Rule: Active Waits (Busyness = Happiness)

**When:** Users must wait for processing or background operations.
**Do:** Give users something to do during waits. Busy people are happier than idle people. Active waits feel shorter and generate more positive associations with your product.
**Values:** Upload: show preview, suggest tagging, display steps. Long process (>10s): show log detail. Post-action: show related content.
**Don't:** Show only a spinner for waits over 3s. Don't block entire UI for partial loads.

---

## Attention Management

### Rule: Von Restorff Effect (Isolation Effect)

**When:** Designing CTAs, important notifications, or key content that must stand out.
**Do:** Make the most important element visually distinct from everything around it. Use a different color, size, shape, or animation. Primary CTAs should be the only element with their specific visual treatment.
**Values:** Primary CTA: unique color not used elsewhere on the page. Size: 1.5x the size of secondary actions minimum. Contrast ratio against background: 4.5:1 minimum.
**Don't:** Make multiple elements "stand out" — if everything is special, nothing is. Don't use the primary CTA color for decorative elements. Don't rely solely on size; combine size + color + whitespace.

### Rule: Selective Attention

**When:** Users need to focus on specific content within a busy interface.
**Do:** Reduce visual noise around important elements. Use whitespace to isolate key content. Dim or blur background content during modal interactions. Remove decorative elements near action areas.
**Values:** Whitespace around CTAs: minimum 24px. Modal overlay opacity: 50-70% black. Maximum competing visual elements in a single viewport: 5-7.
**Don't:** Place banner ads or promotional content adjacent to task-critical UI. Don't animate elements outside the user's current focus area. Don't use background patterns that compete with foreground content.

### Rule: Sustained Attention Limit

**When:** Designing long forms, tutorials, onboarding flows, or reading-heavy content.
**Do:** Break content into segments of 7-10 minutes. Provide natural pause points, progress indicators, and "save and continue later" options. Change the visual pattern every 7-10 minutes to re-engage attention.
**Values:** Segment length: 7-10 minutes of focused activity. Content break: visual separator + progress indicator every 5-7 screens. Long forms: save progress automatically every 30 seconds.
**Don't:** Create 30-minute unbroken flows. Don't lose user progress if they navigate away. Don't present identical visual patterns for more than 10 consecutive minutes.

### Rule: Change Blindness

**When:** Updating content dynamically, showing state changes, or refreshing data.
**Do:** Explicitly highlight what changed. Users fail to notice even large visual changes during visual interruptions (page load, animation, scroll). Use animation, color flash, or "changed" indicators.
**Values:** Animate value changes (counters, fade-in). Flash background of changed cells briefly (200-500ms yellow). Badge/dot for updated sections ("2 new"). Toast for off-screen changes.
**Don't:** Silently update content. Don't change layouts during loading without signaling. Don't remove list items without exit animation.

### Rule: Habituation (Banner Blindness)

**When:** Designing alerts, banners, notifications, or recurring visual elements.
**Do:** Vary visual treatment of important recurring elements. Users habituate to repeated stimuli — they literally stop seeing them.
**Values:** Limit persistent banners to 1 at a time. Rotate copy/design weekly. Escalate: subtle badge > colored badge > inline alert > modal. Dismiss = dismiss; don't re-show.
**Don't:** Show the same banner indefinitely. Don't use alert styling for non-urgent info.

### Rule: Frequency Expectations Affect Attention

**When:** Designing notification frequency or update cadences.
**Do:** Match update frequency to user expectations. Unexpected changes cause anxiety or disengagement.
**Values:** State frequency explicitly ("Updates every 5 min"). "Last updated" timestamps. Let users configure frequency. Consistent cadence > random.
**Don't:** Change frequency without informing users. Don't mix real-time and batch without labels.

### Rule: Mind Wandering Recovery

**When:** Designing long workflows, reading experiences, or multi-step processes.
**Do:** Minds wander ~30% of the time. Provide clear "where am I?" cues for re-orientation.
**Values:** Sticky header with current section name. Progress indicator on multi-step flows. Auto-save with visible "saved" indicator.
**Don't:** Assume continuous attention. Don't auto-advance timed flows. Don't hide context to save space.

### Rule: Flow State Design

**When:** Designing creative tools, editors, writing interfaces, or focused work environments.
**Do:** Create conditions for flow: clear goals, immediate feedback, challenge matched to skill, minimal distractions. Protect flow by minimizing interruptions.
**Values:** Distraction-free/zen mode for editors. Auto-save silently (no save dialogs). Inline feedback, no modal interruptions. Batch notifications in focus mode.
**Don't:** Interrupt with modals, tooltips, or promos. Don't require context switches for subtasks. Don't show notification badges in focus modes.

### Rule: False Causality Prevention

**When:** Multiple things happen simultaneously or sequentially in the UI, and one might be mistaken as causing the other.
**Do:** Ensure feedback is clearly tied to the action that caused it (highlight the specific field with an error, not just a banner at the top). Use proximity and timing: show feedback immediately next to the trigger, not delayed or in a distant location. When background processes complete, make it clear they were background (e.g., "Sync completed" rather than popping up right after the user clicks something unrelated). Label the source of notifications and state changes.
**Values:** Correct mental models, reduced confusion, trust in the interface.
**Don't:** Show unrelated notifications immediately after a user action (user will assume their action caused it). Don't display error messages far from the element that caused the error. Don't allow automatic background changes to appear as if the user triggered them.

---

## Memory & Completion Effects

### Rule: Zeigarnik Effect

**When:** Users are in multi-step processes, onboarding, or profile completion.
**Do:** Show progress toward completion. Incomplete tasks create cognitive tension that motivates completion. Display progress bars, step indicators, and "X of Y completed" counts. Show what's done and what remains.
**Values:** Progress bar: always visible during multi-step flows. Minimum granularity: show progress at each step, not just start/end. Completion percentage: display as number + visual bar.
**Don't:** Hide progress in multi-step flows. Don't show only percentage without visual representation. Don't restart progress indicators between sessions.

### Rule: Goal Gradient Effect

**When:** Users are progressing toward a goal — checkout, onboarding, achievements, rewards.
**Do:** People accelerate effort as they approach a goal. Show proximity to completion. Start progress indicators slightly filled (10-20%) to leverage the endowed progress effect. Use smaller increments near the end to maintain acceleration.
**Values:** Initial progress: 10-20% pre-filled (endowed progress). Progress increments: equal or decreasing size as goal approaches. Visual acceleration: progress bar should show clear advancement with each action.
**Don't:** Start progress at exactly 0% — the first step feels insurmountable. Don't add steps at the end of a flow that users didn't expect. Don't reset progress without clear explanation.

### Rule: Peak-End Rule

**When:** Designing any user experience with a beginning, middle, and end — onboarding, checkout, support interactions.
**Do:** Users judge an experience primarily by its most intense moment (peak) and its ending. Invest design effort in making the peak moment delightful and the final moment satisfying. Confirmation screens, success animations, and summary pages matter disproportionately.
**Values:** Peak moment: include a moment of delight or accomplishment in every flow. End moment: success confirmation with clear next step, celebratory animation (< 2 seconds), and summary of what was accomplished.
**Don't:** End flows with generic "Done" text. Don't make the last step the most frustrating (e.g., CAPTCHA at the end of checkout). Don't neglect error recovery experiences — negative peaks are remembered even more strongly.

### Rule: Mood Affects Decision Architecture

**When:** Designing flows where users might be frustrated (error recovery, cancellation, support).
**Do:** Simplify decision-making in negative-mood contexts. Frustrated people make worse decisions. Reduce options and provide a single clear recovery path.
**Values:** Error flows: one clear recovery path. Cancellation: simple single-path. After failure: reduce to 2 choices (retry vs get help).
**Don't:** Present complex decisions after errors. Don't use dark patterns in cancellation flows.

### Rule: Depth of Processing

**When:** Designing onboarding, tutorials, or help content that users need to remember.
**Do:** Make users actively engage with information rather than passively reading it. Use interactive tutorials over text instructions. Ask users to perform the action rather than watching a demo. Combine multiple media (text + image + interaction) for deepest processing.
**Values:** Elaborative rehearsal (active engagement) = 2-3x better recall than maintenance rehearsal (passive reading). Interactive onboarding > video walkthrough > text documentation for retention.
**Don't:** Present important instructions as a wall of text. Don't show a one-time modal with 5 tips and expect users to remember any of them. Don't rely on tooltips for features users need to recall unprompted.

---

## Complexity & Mental Models

### Rule: Tesler's Law (Conservation of Complexity)

**When:** Simplifying an interface or deciding where to handle complexity.
**Do:** Every system has inherent complexity that cannot be removed, only moved. Move complexity from the user to the system. Auto-detect settings, use smart defaults, compute values automatically. The system should do the hard work.
**Values:** If the system can determine a value with 90%+ accuracy, auto-fill it. If a decision has a best answer for 80%+ of users, make it the default. User-facing complexity should be the minimum irreducible set.
**Don't:** Expose system complexity to users (database IDs, internal state, technical jargon). Don't force users to make decisions the system can make. Don't simplify the UI by removing necessary features — move complexity, don't delete it.

### Rule: Mental Models

**When:** Designing interaction patterns, terminology, or system behavior.
**Do:** Match the user's existing mental model, not your system's architecture. Users think in terms of tasks ("send a message"), not system structures ("create a message object and assign it to the outbox queue"). Use language and flows that match how users think about the task.
**Values:** User testing: 5 users describing the task in their own words should use similar language to your UI. Task flow: should match the order users naturally think about the task, not the order the system processes it.
**Don't:** Expose database structure in the UI. Don't use technical terms when plain language exists. Don't organize navigation by internal team structure ("Engineering Tools", "Marketing Tools") instead of user tasks.

### Rule: Conceptual Models and System Image

**When:** Designing any system the user must build a mental model of (file systems, state machines, multi-step workflows, settings hierarchies).
**Do:** Design the "system image" (everything visible to the user) so it communicates the correct conceptual model. Show system state explicitly — never make the user guess what mode they're in or what the system is doing. Use familiar metaphors that map to real-world mental models (folders = containers, trash = reversible delete). Provide immediate, visible feedback that reinforces the correct model of how the system works.
**Values:** Predictability, user confidence, reduced errors from wrong mental models.
**Don't:** Assume the user's conceptual model matches the implementation model. Don't hide system state behind menus or require memorization of modes. Don't mix metaphors (e.g., a "folder" that behaves like a tag).

### Rule: Gulf of Execution and Gulf of Evaluation

**When:** Designing any user workflow, especially complex multi-step tasks.
**Do:** Bridge the Gulf of Execution (gap between intention and available actions): make available actions visible and match user vocabulary — if the user thinks "I want to share this," there should be a button labeled "Share," not "Export to collaborative workspace." Bridge the Gulf of Evaluation (gap between system state and user understanding): show clear, immediate feedback after every action — loading states, success confirmations, progress bars, state changes. Minimize the number of steps between "I want to do X" and actually doing X.
**Values:** Direct manipulation feel, immediate feedback, minimal cognitive translation.
**Don't:** Use system-internal terminology in UI labels (e.g., "PATCH request failed" instead of "Could not save changes"). Don't perform actions silently with no visible feedback. Don't require the user to check a different page/screen to see the result of their action.

### Rule: Eliminate Excise (Non-Goal Work)

**When:** Auditing any workflow for unnecessary steps, especially in forms, navigation, and settings.
**Do:** Identify and eliminate four types of excise: **Navigation excise** — reduce clicks/taps to reach a goal; if a task requires navigating 3+ levels deep, provide a shortcut. **Cognitive excise** — don't make users translate between their vocabulary and the system's. **Mechanical excise** — reduce the physical effort of repetitive tasks (copy-paste support, bulk actions, drag-and-drop, auto-fill). **Visual excise** — don't make users visually search for the thing they need; put it where they're already looking. Ask: "Does this step serve the USER's goal, or only the SYSTEM's need?" — if only the system's, eliminate or automate it.
**Values:** Streamlined workflows, user time respected, goal-focused interaction.
**Don't:** Add confirmation dialogs for low-risk actions just to "be safe." Don't require login/re-authentication in the middle of a task when session is still valid. Don't force users through onboarding/setup wizards on every visit. Don't make users manually enter data the system already has (address lookups, auto-complete from profile).

### Rule: Aesthetic-Usability Effect

**When:** Making decisions about visual polish vs functional improvements.
**Do:** Attractive interfaces are perceived as more usable and users are more forgiving of minor usability issues. Invest in visual design proportional to the interface's complexity — the more complex the task, the more visual design helps users tolerate friction.
**Values:** Visual polish increases perceived usability by 20-30% in studies. Users will retry failed tasks 2-3x more on attractive interfaces. Minimum investment: consistent spacing, harmonious colors, professional typography.
**Don't:** Use visual polish to mask fundamental usability problems. Don't assume an attractive interface is a usable one — test both aesthetics and usability. Don't sacrifice clarity for style.

### Rule: Processing Hierarchy — Visceral, Behavioral, Reflective

**When:** Evaluating overall user experience quality.
**Do:** Design for all three levels of cognitive processing. Visceral (< 50ms): is it visually appealing? Behavioral (during use): is it efficient and satisfying? Reflective (after use): does the user feel good about using it? Each level requires different design attention.
**Values:** Visceral: polished visuals, appropriate color palette, clean typography. Behavioral: task completion < 3 clicks for common actions, clear feedback on every interaction. Reflective: brand alignment, status signaling, story the user tells about the product.
**Don't:** Optimize only for visceral appeal (pretty but unusable). Don't optimize only for behavioral efficiency (functional but ugly). Don't ignore reflective aspects (users won't recommend products they're embarrassed to use).

### Rule: Maslow's Hierarchy for Interfaces

**When:** Planning or auditing any interface, prioritizing design effort across functional correctness, usability, and delight.
**Do:** Interface needs follow a hierarchy: (1) **Functional** — it works, it's reliable, it doesn't crash. This is the non-negotiable foundation. (2) **Reliable** — it works consistently, loads quickly, data is safe. (3) **Usable** — it's easy to learn and efficient to use. (4) **Pleasurable** — it creates positive emotional response, delight, personality. Satisfy each level before investing in the next. A delightful interface that crashes is worse than a boring one that works. But stopping at "usable" means your product is a commodity — the pleasurable layer creates loyalty and word-of-mouth.
**Values:** Time allocation suggestion: 70% functional+reliable, 20% usable, 10% pleasurable. The 10% on pleasurable delivers disproportionate emotional ROI. The pleasurable layer includes: personality in copy, Signature Moments, surprise and delight in feedback, aesthetic polish beyond functional requirements.
**Don't:** Invest in delight before the product is reliable (users will resent playful animations in a buggy product). Don't skip the usability layer to add personality. Don't treat the hierarchy as optional — products that stay at "functional" lose to competitors who reach "pleasurable." Don't confuse "pleasurable" with "decorated" — true delight comes from interactions that feel effortless, not from visual ornament.

### Rule: MAYA (Most Advanced Yet Acceptable)

**When:** Introducing a redesign, new UI pattern, or unfamiliar interaction to users.
**Do:** Balance novelty with familiarity. The most commercially successful design is the most novel form that is still recognizable as something familiar. When introducing a new feature or pattern, anchor it to a recognized convention.
**Values:** For mass audiences: maximize novelty while maintaining recognition. For design-expert audiences (design tools, dev tools): lean more toward novelty. For anxious/stressed users: lean more toward familiar patterns.
**Don't:** Make a redesign so novel that users don't recognize what the product does. Don't be so conservative that the design is indistinguishable from competitors.

### Rule: Design for Perpetual Intermediates

**When:** Designing the default experience and deciding feature prominence.
**Do:** Optimize the UI for intermediate users — they are the largest and most stable user group. Provide easy onboarding for beginners, but don't let beginner-friendly features dominate the interface permanently (use dismissible tips, not permanent helper text). Offer expert shortcuts and power features, but keep them out of the default view (keyboard shortcuts, command palettes, advanced settings behind a toggle). Use a "gentle slope" from beginner to intermediate: progressively reveal complexity as usage patterns mature.
**Values:** Efficiency for the majority, graceful skill progression, no ceiling on expertise.
**Don't:** Design primarily for first-time users at the expense of daily users (permanent tutorials, oversimplified workflows). Don't design primarily for power users at the expense of approachability (CLI-only interfaces, hidden features with no discovery path). Don't force all users through the same experience regardless of skill level.

---

## Checklist

- [ ] No more than 4 ungrouped items presented simultaneously
- [ ] Choices at each decision point: 3-5 options maximum
- [ ] System response time under 400ms for interactive elements
- [ ] Progress indicators visible in all multi-step flows
- [ ] Primary CTA is visually unique — distinct color, size, and whitespace
- [ ] Advanced options hidden behind progressive disclosure
- [ ] Content segmented into 7-10 minute attention blocks for long flows
- [ ] Smart defaults reduce decisions users must make
- [ ] UI language matches user mental models, not system architecture
- [ ] Loading feedback: skeleton screen at 400ms, progress bar at 1s+
- [ ] Each flow has an identifiable peak moment and satisfying end
- [ ] Recognition used instead of recall for all selection interfaces
- [ ] Dynamic content changes are visually highlighted (no silent updates)
- [ ] Prior choices visible throughout multi-step flows
- [ ] New features anchored to familiar concepts
- [ ] Error/frustration flows simplified to minimal choices
- [ ] Focus modes protect flow state from interruptions
- [ ] Exactly 2 interaction methods per core task (beginner + expert)
- [ ] Interface satisfies Functional > Reliable > Usable > Pleasurable hierarchy
- [ ] Redesigns balance novelty with familiarity (MAYA principle)
- [ ] Default experience optimized for intermediate users
- [ ] Knowledge displayed in the world, not required from memory
- [ ] Feedback tied to its source action (no false causality)
- [ ] Navigation, cognitive, mechanical, and visual excise eliminated
- [ ] Onboarding uses active engagement, not passive reading
- [ ] Conceptual model visible through system image
- [ ] Gulf of Execution and Gulf of Evaluation both bridged

---

---

# Chapter 10: Behavioral Triggers & Engagement

Habits form when a behavior occurs with sufficient frequency and perceived utility. The Hook cycle — Trigger, Action, Variable Reward, Investment — is the foundational model for building products users return to without external prompting. Microinteractions — the small, single-purpose interactive moments within features — are where engagement design becomes tangible. Use these patterns to build genuine value, not manipulation.

**When to Use:**
- Designing retention and re-engagement systems
- Building notification and trigger strategies
- Creating reward and feedback loops
- Increasing feature adoption and daily active usage
- Evaluating whether your product is a Facilitator or a Dealer
- Designing single-purpose interactive moments (toggles, likes, status changes)

| Quick Reference | Value |
|----------------|-------|
| Hook cycle stages | 4: Trigger > Action > Variable Reward > Investment |
| Behavior formula | B = M x A x T (Motivation x Ability x Trigger) |
| Habit Zone threshold | Frequency: daily-weekly + Perceived utility: high |
| Min trigger-to-action steps | 1 tap/click from trigger to core action |
| Reward types | 3: Tribe (social), Hunt (resources), Self (mastery) |
| Investment timing | After reward delivery, never before |
| Microinteraction parts | 4: Trigger > Rules > Feedback > Loops & Modes |
| Feedback timing | < 100ms for direct manipulation |

---

## Microinteraction Architecture

### Rule: Microinteraction Architecture (Trigger > Rules > Feedback > Loops & Modes)

**When:** Designing any single-purpose interactive moment — a toggle, a status change, a like button, a mute switch, a password field, a pull-to-refresh, a volume control, or any contained interaction that does one thing.
**Do:** Structure every microinteraction as four distinct parts: (1) **Trigger** — what initiates it (user action or system condition), (2) **Rules** — what happens once triggered (the invisible logic), (3) **Feedback** — how the user knows what's happening (visual, audio, haptic), (4) **Loops & Modes** — how it behaves over time and in alternate states. Design each part explicitly. Most failed microinteractions skip the Rules or Loops phase entirely.
**Values:** Every interactive element should have all four parts documented. Triggers must be discoverable. Rules should feel natural and match user mental models. Feedback must be immediate (<100ms). Loops define what happens on repeat use, expiration, or long-term engagement. A microinteraction is NOT a feature — it is a single-use-case moment within a feature.
**Don't:** Design microinteractions as afterthoughts bolted onto features. Don't conflate a feature (multi-step, multi-goal) with a microinteraction (single task, single goal). Don't skip the Loops phase — every interaction changes over time. Don't design feedback without first defining rules.

### Rule: Trigger Discoverability Hierarchy

**When:** Deciding how to surface interactive controls — buttons, gestures, hover zones, long-press actions, keyboard shortcuts.
**Do:** Rank triggers by discoverability: (1) **Visible + labeled** (button with text) — most discoverable, (2) **Visible + icon-only** (icon button) — moderate, (3) **Hidden but conventional** (right-click, swipe) — low, (4) **Hidden and unconventional** (shake device, 3D touch) — lowest. Match discoverability level to frequency of use. Primary actions need Level 1 triggers. Power-user shortcuts can be Level 3-4 but must always have a Level 1-2 fallback.
**Values:** First-time use: Level 1 triggers only. Frequent actions: provide Level 3 shortcuts alongside Level 1 visible triggers. Never make a critical action available only through a hidden trigger. "Bring the data forward" — if a trigger depends on information (e.g., unread count), display that information on or near the trigger itself.
**Don't:** Hide primary actions behind gestures or long-press without a visible alternative. Don't require users to discover triggers through exploration alone. Don't use Level 4 triggers (shake, force-touch) as the only path to functionality. Don't separate the trigger from the data it acts upon.

### Rule: Manual vs System Triggers

**When:** Deciding whether an interaction should be initiated by the user or by the system automatically.
**Do:** Use **manual triggers** when the user has intent and context (clicking "Send", toggling dark mode). Use **system triggers** when a condition is met that the user would want to know about but shouldn't have to monitor (low battery, new message, sync complete). System triggers must meet a condition rule: the trigger fires only when specific criteria are met. Always allow users to configure or disable system triggers.
**Values:** System triggers should match one or more of: location, time, data threshold, device state, internal state (preferences), or other people's actions. Never fire a system trigger without the user having opted in (explicitly or through reasonable defaults). System triggers that interrupt (modal, sound) require higher threshold than passive ones (badge, dot).
**Don't:** Use system triggers for marketing messages disguised as notifications. Don't fire system triggers at high frequency without throttling. Don't make system triggers non-configurable. Don't use manual triggers for conditions the system can detect automatically (e.g., making users manually check for updates when auto-check is feasible).

### Rule: Rules Should Be Invisible But Feel Natural

**When:** Defining the logic behind any interactive element — what happens when a toggle is flipped, what constraints exist on a form input, what sequence of states an object moves through.
**Do:** Rules are the invisible algorithm of a microinteraction. Users should never need to read documentation to understand them. Rules should: (1) Feel like common sense — match the user's mental model, (2) Limit options wisely — use smart constraints to prevent errors (a date picker that grays out past dates rather than validating after selection), (3) Use defaults aggressively — pre-fill with the best guess from known context (location, time, history, device state). The best rules are ones users never notice.
**Values:** Define the simplest rule that achieves the goal. Every rule should answer: what is the goal of this interaction? What constraints apply? What data is available to make it smarter?
**Don't:** Expose rule complexity to users through error messages that reveal internal logic. Don't create rules that contradict the user's mental model (a volume "knob" that works like a slider breaks the metaphor). Don't allow states that the rules make invalid — if a combination is impossible, prevent it from being selected. Don't make the user remember state — the system should track and reflect it.

---

## Feedback Design

### Rule: Feedback Personality and Restraint

**When:** Designing the visual, auditory, or haptic response to any user action — success states, loading indicators, error messages, confirmations, transitions.
**Do:** Feedback should follow three principles: (1) **Minimal** — the least amount of feedback necessary to communicate the state change. Don't animate what can be shown statically. Don't use sound when visual is sufficient. (2) **Non-arbitrary** — every feedback element must have a reason tied to the interaction's meaning. A red flash for an error is meaningful; a random bounce animation is not. (3) **Personality-bearing** — feedback is where product personality lives. The way a toggle snaps, the micro-copy in a loading state, the sound of a sent message — these are "Signature Moments" that differentiate your product.
**Values:** Feedback must be: immediate (<100ms for direct manipulation), informative (communicates what happened), and proportional (big actions get big feedback, small actions get small feedback). Use the "overlooked, ignored, endured" test: if your feedback is merely endured, reduce it. If it's overlooked, it's the right amount. Create 1-3 "Signature Moments" — feedback interactions so well-crafted they become associated with your brand.
**Don't:** Add animation for its own sake. Don't use the same feedback for different state changes (if success and error both show a generic toast, the feedback is meaningless). Don't make feedback louder/bigger to compensate for poor placement — fix the placement instead. Don't let feedback persist longer than needed. Don't use sound feedback as the only channel — always pair with visual.

### Rule: Feedback Hierarchy by Channel

**When:** Choosing which feedback channel (visual, auditory, haptic) to use for a given interaction.
**Do:** Match feedback channel to context and urgency: (1) **Visual** — default channel, works everywhere, least intrusive. Use for: state changes, progress, confirmations. (2) **Auditory** — attention-getting, works when user isn't looking at screen. Use for: completed background tasks, errors requiring action, incoming messages. (3) **Haptic** — subtle confirmation, works on mobile. Use for: toggle feedback, button press confirmation, boundary reached (end of scroll). Layer channels for critical feedback: error = red visual + error sound + haptic buzz. Use single channel for routine feedback: toggle = visual state change only.
**Values:** Visual feedback: always present as base layer. Sound: only when visual might be missed (background tasks, off-screen events) or for Signature Moments. Haptic: confirmation of physical-feeling actions (toggles, sliders, pulls). Never use auditory as the sole feedback channel. Critical actions: 2+ channels. Routine actions: 1 channel (visual).
**Don't:** Use sound for every interaction (notification fatigue applies to audio too). Don't use haptic feedback on desktop (not available on most devices). Don't layer all three channels for routine actions (overwhelming). Don't forget that feedback channels have accessibility implications — always ensure at least one non-auditory and one non-visual channel for critical feedback.

### Rule: Surprise Amplifies Emotional Response

**When:** Designing micro-interactions, confirmations, or discovery moments.
**Do:** Introduce unexpected positive moments at strategic points in the user journey. Surprise compresses emotion into a split second, creating stronger memory imprints. Use surprise to break behavioral patterns and redirect attention. Follow surprise with a proportional positive emotional response. Establish a pattern, then break it positively.
**Values:** Place surprises at these strategic points: (1) post-purchase/post-action confirmation, (2) milestone achievements, (3) idle discovery moments. Limit to 1-2 surprises per session to prevent habituation. Frequency: 1 surprise per 20-50 routine interactions. Surprises must be positive, contextual, and proportional.
**Don't:** Use surprise to trick or deceive users. Don't place surprises in critical task flows where they might disrupt focus. Don't overuse — if everything is surprising, nothing is. Don't surprise during checkout, data entry, or security flows. Don't repeat the exact same surprise — vary it or it becomes routine.

### Rule: Anticipation as Open System

**When:** Planning feature launches, redesigns, or phased rollouts.
**Do:** Create anticipation by foreshadowing desired events and giving the audience time to imagine the experience. Use partial reveals (teasers, previews) rather than full disclosure. Combine with limited access (velvet rope effect) to elevate perceived status of early users.
**Values:** Anticipation timeline: tease 2-4 weeks before launch. Partial reveal: show 30-40% of the experience. Limited access: roll out to 5-10% of users first, then expand.
**Don't:** Force users onto new interfaces without choice. Always offer "You may" (opt-in) rather than "You must" (forced migration). Don't reveal everything at once — leave room for imagination.

---

## Long Loops & Modes

### Rule: Long Loops — Progressive Adaptation Over Time

**When:** Designing any interaction that users will encounter repeatedly over days, weeks, or months — onboarding flows, tooltips, power-user features, notification frequency, interface complexity.
**Do:** Microinteractions should evolve over time through "long loops": (1) **Progressive Reduction** — reduce UI chrome as users demonstrate mastery. Replace labeled buttons with icons after N uses. Collapse expanded tutorials into compact hints. Hide beginner scaffolding for power users. (2) **Progressive Disclosure in reverse** — start simple, but unlock complexity as the user is ready. (3) **Graceful degradation of frequency** — reduce notification/reminder frequency as the user builds the habit. Day 1: remind every session. Week 2: remind daily. Month 2: remind weekly. Month 6: stop reminding.
**Values:** Track interaction count per user to drive progressive reduction. After 10+ uses: consider reducing labels to icons. After 50+ uses: consider offering keyboard shortcuts prominently. After 100+ uses: consider a "compact mode". Notification frequency should decay. Never remove functionality through progressive reduction — only reduce visual prominence. Always provide a way to "reset" or access the full UI.
**Don't:** Show the same onboarding tooltip to a user who has completed the action 50 times. Don't increase notification frequency over time. Don't permanently hide features through progressive reduction without an escape hatch. Don't treat all users identically — track individual mastery, not calendar time.

### Rule: Spring-Loaded and Temporary Modes

**When:** An interaction requires a temporary alternate state — caps lock, shift key, temporary zoom, drag mode, preview mode, or any "hold to activate" behavior.
**Do:** Prefer **spring-loaded modes** (active only while held/engaged, revert automatically on release) over **toggle modes** (stay in alternate state until explicitly toggled off). Spring-loaded modes prevent "mode errors" — the user forgetting they're in an alternate mode. Examples: hold Shift for uppercase (spring-loaded) vs. Caps Lock (toggle mode that causes errors). Hold to preview (spring-loaded) vs. enter preview mode (toggle that users forget to exit).
**Values:** Spring-loaded: use for temporary, brief-duration alternate states (< 5 seconds). Toggle: use only when the user needs to perform extended work in the alternate mode (> 30 seconds). If using toggle modes: provide a persistent, visible indicator that the mode is active. For one-off modes (single action in alternate state), auto-revert after the action completes.
**Don't:** Create toggle modes without visible mode indicators. Don't use toggle modes for actions that are typically brief. Don't let users perform destructive actions while in a mode they may have forgotten they entered. Don't stack multiple modes — if the user is in Mode A and triggers Mode B, either exit A automatically or prevent B.

---

## The Hook Model

### Rule: The Hook Cycle

**When:** Designing any product feature intended for repeated use.
**Do:** Map the complete cycle: (1) Trigger — what prompts the user, (2) Action — simplest behavior in anticipation of reward, (3) Variable Reward — satisfies the need but leaves wanting more, (4) Investment — user puts something in that improves next cycle. Each hook loads the next trigger.
**Values:** Complete all 4 stages. Incomplete cycles don't form habits. Map each stage explicitly before building.
**Don't:** Skip the Investment phase. Don't make rewards predictable (kills engagement). Don't trigger actions without a clear reward path.

### Rule: Internal vs External Triggers

**When:** Designing the trigger strategy for a feature or product.
**Do:** Start with external triggers (notifications, emails) to train behavior. The goal is to graduate users to internal triggers — emotional states that automatically prompt product use. Map which emotions your product addresses: boredom (social media), uncertainty (search), loneliness (messaging), FOMO (feeds).
**Values:** External triggers: drive initial behavior. Internal triggers: sustain long-term habits. Successful products connect to internal triggers within 3-4 weeks of regular use.
**Don't:** Rely on external triggers permanently — they lose effectiveness over time. Don't guess at internal triggers; interview users and identify the emotion that precedes product use.

### Rule: Four External Trigger Types

**When:** Planning acquisition, growth, and retention trigger strategies.
**Do:** Use all four types strategically: (1) Paid triggers — ads, SEM (acquisition, not sustainable), (2) Earned triggers — press, viral content (spikes, not reliable), (3) Relationship triggers — referrals, word-of-mouth (growth engine), (4) Owned triggers — app icons, email subscriptions, notifications (retention, most valuable). Invest most in owned triggers.
**Values:** Paid: acquisition only, measure CAC strictly. Earned: amplification, not primary strategy. Relationship: highest conversion rate (3-5x paid). Owned: highest LTV, requires permission (email, push notification opt-in).
**Don't:** Depend on paid triggers for retention. Don't treat earned media as predictable. Don't abuse owned triggers — notification fatigue destroys the channel permanently.

### Rule: Trigger-to-Action Distance

**When:** Designing notifications, emails, or any trigger-initiated flow.
**Do:** One tap or click from trigger to core action. Push notification opens directly to relevant content. Email CTA links to exact screen. Every intermediate step loses 20-50% of users.
**Values:** Maximum steps from trigger to action: 1 (ideal), 2 (acceptable), 3+ (redesign required). Each additional step loses 20-50% of users.
**Don't:** Send notifications that open to the home screen. Don't require login between trigger and action (use deep links with auth). Don't add interstitials between trigger and action.

### Rule: Viral Loop Structure

**When:** Designing social features, sharing mechanics, or user-generated content systems.
**Do:** Structure actions so: User A's action = feedback for User B = content for User C. Make the viral action (share, retweet, invite) the visually primary action, not the secondary one. Design sharing to benefit the sharer first (self-expression, status), with virality as a side effect.
**Values:** Viral actions should be the first or most prominent button in social interactions. Non-viral actions (like, bookmark) should be visually secondary. The formula: Action > Feedback > Content > Loop.
**Don't:** Make the share button small and last in a list. Don't make sharing purely altruistic — users share for themselves first. Don't rely on "Share this page" buttons on non-social content.

---

## Fogg Behavior Model

### Rule: B = MAT (Behavior = Motivation x Ability x Trigger)

**When:** Analyzing why users don't complete a desired action.
**Do:** All three factors must be present simultaneously. If behavior isn't happening, diagnose which factor is missing: (1) Is the user motivated? (2) Is the action easy enough? (3) Is there a trigger at the right moment? Address the weakest factor first.
**Values:** Motivation: does the user want the outcome? Ability: can they do it in < 3 steps? Trigger: is there a prompt at the moment of motivation + ability? All three must be present — zero on any factor means zero behavior.
**Don't:** Add motivational copy when the action is too complex. Don't trigger users who lack ability. Don't increase ability without ensuring triggers are present.

### Rule: Always Increase Ability Before Motivation

**When:** Deciding between making an action easier vs. making users want it more.
**Do:** Reduce friction first. Increasing motivation is expensive (marketing, copywriting, incentives) and temporary. Increasing ability is cheap (fewer fields, bigger buttons, smarter defaults) and permanent. A motivated user blocked by friction churns. An unmotivated user with an easy path might still convert.
**Values:** Priority order: (1) Reduce steps, (2) Reduce cognitive load, (3) Add motivation. Every field removed from a form increases completion by 5-10%.
**Don't:** Write motivational copy instead of simplifying the flow. Don't add incentives (discounts, bonuses) to compensate for a bad UX. Don't assume users lack motivation when they actually lack ability.

### Rule: Six Elements of Simplicity

**When:** Evaluating whether an action is "easy enough" for users.
**Do:** Assess and minimize all six: (1) Time — how long does it take? (2) Money — what's the financial cost? (3) Physical effort — how many taps, scrolls, keystrokes? (4) Brain cycles — how much thinking? (5) Social deviance — does this violate social norms? (6) Non-routine — how unfamiliar is this behavior?
**Values:** Optimize the scarcest resource for your user segment. Time-poor professionals: minimize time above all. Price-sensitive users: minimize cost signals. New users: minimize non-routine elements.
**Don't:** Optimize only one simplicity factor while ignoring others. Don't assume all users have the same scarcest resource. Don't add brain cycles to save physical effort (e.g., complex filtering to reduce scrolling).

### Rule: Three Core Motivators

**When:** Designing motivational elements — CTAs, value propositions, urgency signals.
**Do:** All human motivation maps to three spectrums: (1) Pleasure / Pain — immediate sensation, (2) Hope / Fear — anticipated outcomes, (3) Social Acceptance / Rejection — belonging and status. Identify which motivator your product serves and align all messaging.
**Values:** Most effective: match the motivator to the user's current emotional state. Pleasure/pain: immediate rewards and consequences. Hope/fear: future-oriented features (savings goals, health tracking). Acceptance/rejection: social features, reviews, profiles.
**Don't:** Mix motivators in a single CTA (confusing). Don't use fear-based motivation for pleasure-oriented products. Don't underestimate social acceptance as a motivator — it's often the strongest.

---

## Cognitive Heuristics in UI

### Rule: Scarcity Effect

**When:** Displaying availability, time limits, or exclusive access.
**Do:** Show real scarcity signals: "3 left in stock", "Offer ends in 2 hours", "Limited to first 100 users". Scarcity increases perceived value and urgency.
**Values:** Display exact numbers ("3 left") not vague language ("limited"). Show countdown timers for time-limited offers. Update scarcity signals in real-time.
**Don't:** Fabricate scarcity. Don't show "Only 2 left!" permanently. Don't use scarcity for everyday items where it's implausible.

### Rule: Anchoring Effect

**When:** Presenting prices, plan comparisons, or numerical values.
**Do:** Present the highest-value option first to anchor perception. Show the original price before the discount. Display enterprise pricing before starter pricing on comparison pages.
**Values:** First number seen becomes the anchor. Show "was $99, now $49" not just "$49". Place premium plan first (left position in LTR layouts).
**Don't:** Anchor with unrealistically high numbers (damages trust). Don't hide reference prices. Don't present the cheapest option first in upgrade flows.

### Rule: Endowed Progress Effect

**When:** Designing loyalty programs, onboarding progress, or achievement systems.
**Do:** Give users a head start on progress. A loyalty card with 2 of 10 stamps pre-filled converts better than a blank 8-stamp card, despite requiring the same 8 purchases. Pre-fill onboarding progress with steps already completed (account created, email verified).
**Values:** Pre-fill 10-20% of progress. Show "Step 2 of 6" instead of "Step 1 of 5" when account creation counts as step 1. Completion rate increase: 15-30% with endowed progress.
**Don't:** Pre-fill more than 30% (feels manipulative). Don't endow progress on tasks with no real head start. Don't reset endowed progress.

### Rule: Framing Effect

**When:** Presenting options, outcomes, or statistics to users.
**Do:** Frame positively: "95% uptime" not "5% downtime". Frame losses when motivating action: "You'll lose your saved data" not "Save your data to keep it". People weigh losses 2x more than equivalent gains.
**Values:** Positive framing for features and benefits. Loss framing for urgency and risk prevention. Loss aversion ratio: ~2:1 (a $10 loss feels like a $20 gain).
**Don't:** Use negative framing for product features ("We don't crash often"). Don't mix positive and negative framing in the same context. Don't use loss framing manipulatively.

---

## Variable Rewards

### Rule: Three Types of Variable Rewards

**When:** Designing the reward phase of any engagement loop.
**Do:** Match reward type to user motivation: (1) Tribe — social rewards: likes, comments, mentions, leaderboard positions. (2) Hunt — resource rewards: money, information, deals, content. (3) Self — mastery rewards: skill improvement, completion, leveling up, personal achievement.
**Values:** Use at least 2 of 3 reward types per product. Social products: Tribe primary. Marketplaces/feeds: Hunt primary. Learning/productivity: Self primary.
**Don't:** Use only one reward type. Don't make rewards entirely predictable (kills the dopamine response). Don't misalign reward type with user motivation.

### Rule: Match Rewards to Motivations

**When:** Choosing which rewards to implement.
**Do:** Users seeking social connection need Tribe rewards (not points). Users seeking information need Hunt rewards (not badges). Users seeking mastery need Self rewards (not social proof). Mismatched rewards fail regardless of variability or quality.
**Values:** Interview 10 users about why they use the product. Map answers to Tribe/Hunt/Self. Primary reward type should match 70%+ of user motivations.
**Don't:** Add gamification (badges, points) to products where users seek social connection. Don't add social features to products where users seek solitary mastery. Don't assume all users want the same reward type — segment if needed.

### Rule: Maintain User Autonomy

**When:** Implementing any persuasive or engagement pattern.
**Do:** Users must feel in control. Add phrases like "you are free to..." or "it's entirely up to you" — this doubles compliance in studies. Provide easy opt-out from notifications, emails, and features. Reactance (pushback against perceived manipulation) destroys engagement.
**Values:** Every notification has a visible "Turn off" option. Every engagement feature has an opt-out. Language: "You might like..." not "You must...". "You are free to..." increases compliance by 100%.
**Don't:** Remove user control to increase engagement metrics. Don't make opt-out paths harder than opt-in. Don't trigger reactance with aggressive language, forced actions, or hidden options.

### Rule: Infinite vs Finite Variability

**When:** Designing content feeds, reward systems, or discovery features.
**Do:** Prefer user-generated variability over designed variability. User-generated content feeds are infinitely variable. Designed puzzles and challenges eventually become predictable. Enable users to create the variability that keeps them engaged.
**Values:** Infinite variability: social feeds, user content, multiplayer interactions. Finite variability: game levels, curated playlists, editorial content. Finite variability has a shelf life — plan for content refresh cycles.
**Don't:** Build finite variability systems without a content pipeline. Don't assume infinite variability is always better — some products need curation. Don't let infinite variability become noise (curate the feed).

---

## Investment Phase

### Rule: Ask for Investment AFTER Reward

**When:** Timing when to ask users to contribute data, content, effort, or money.
**Do:** Deliver value first, then ask for investment. After a user receives a reward (found useful content, received social validation, completed a satisfying task), they're primed to invest. Post-reward investment rates are 2-3x higher than pre-reward.
**Values:** Investment request: within 5 seconds of reward delivery. Conversion rate: 2-3x higher post-reward. Never ask for investment as the first interaction.
**Don't:** Ask for ratings before showing results. Don't request profile completion before demonstrating value. Don't paywall content before the user has experienced the product.

### Rule: Five Forms of Stored Value

**When:** Designing investment mechanics that increase switching costs.
**Do:** Enable users to store value in your product across five categories: (1) Content — posts, documents, playlists they create. (2) Data — preferences, history, personalization. (3) Followers — social connections, audience. (4) Reputation — ratings, reviews, karma, credentials. (5) Skill — learned behaviors, keyboard shortcuts, expertise with the tool.
**Values:** Implement at least 2 forms of stored value. Each form increases switching costs. Content + Data are easiest to implement. Reputation + Followers have highest lock-in.
**Don't:** Make stored value non-portable (creates resentment). Don't undervalue skill investment — users who learn your shortcuts are deeply retained. Don't build stored value that doesn't benefit the user.

### Rule: Stage Investments Progressively

**When:** Asking users for increasing levels of commitment.
**Do:** Start with tiny investments (set a username), graduate to medium (upload a photo, connect an account), then larger (invite friends, create content, pay). Each completed investment increases commitment to the next.
**Values:** First session: 1 micro-investment (< 10 seconds). First week: 2-3 small investments (< 1 minute each). First month: 1-2 medium investments (1-5 minutes). Ongoing: content creation and social investment.
**Don't:** Ask for large investments from new users. Don't request multiple investments simultaneously. Don't skip stages — the progression builds psychological commitment.

### Rule: Load the Next Trigger

**When:** Designing the end of any usage session or completed action.
**Do:** Every investment should set up the next trigger to return. Creating content triggers notifications when others engage with it. Setting preferences triggers personalized recommendations. Following users triggers updates on their activity. The investment phase plants the seed for the next Hook cycle.
**Values:** 100% of investment actions should load at least 1 future trigger. Time to next trigger: within 24 hours for daily products, within 7 days for weekly products.
**Don't:** End sessions without planting a return trigger. Don't invest without a follow-up mechanism. Don't create dead-end flows where nothing triggers a return.

---

## Habit Design

### Rule: Habit Formation by Design

**When:** Designing onboarding, daily-use features, or engagement loops.
**Do:** Habits form through consistent context + behavior + reward. Make first uses easy, rewarding, and contextually triggered.
**Values:** Streak indicators. Default to habitual action (most recent project). Don't change location of frequently used controls (breaks muscle memory).
**Don't:** Change layouts for experienced users. Don't require extra steps for routine actions.

### Rule: Habit vs Value-Based Decisions

**When:** Designing for both new and returning users.
**Do:** New users make value-based decisions (weighing pros/cons); returning users make habit-based decisions (automatic). Design different flows for each.
**Values:** New users: explanations, tooltips, comparisons. Returning: recent items, shortcuts, remembered preferences. Don't show onboarding to returning users.
**Don't:** Design exclusively for new or power users.

### Rule: Competition Works With Fewer Competitors

**When:** Designing leaderboards or competitive features.
**Do:** Limit competitive set to small groups. Show user's immediate neighborhood (3 above, 3 below).
**Values:** Leaderboard: show rank +/-3. Team challenges: 5-10 people. Personal bests when group is too large.
**Don't:** Show large leaderboards that make users feel anonymous.

---

## Ethical Framework

### Rule: The Habit Zone

**When:** Evaluating whether your product should use habit-forming patterns.
**Do:** Products enter the Habit Zone when they have both sufficient frequency (daily or weekly use) and high perceived utility. Map your product on both axes. Only products in the Habit Zone should invest heavily in habit-forming patterns.
**Values:** Habit Zone: frequency >= weekly AND perceived utility >= "would miss it if gone". Below frequency threshold: focus on increasing usage occasions. Below utility threshold: fix the core value proposition first.
**Don't:** Apply habit-forming patterns to products used monthly or less. Don't confuse forced usage (mandatory work tool) with genuine habit (would use voluntarily). Don't optimize for engagement without genuine utility.

### Rule: Manipulation Matrix

**When:** Evaluating the ethics of your engagement design.
**Do:** Place your product in one of four quadrants: (1) Facilitator — you'd use it yourself AND it materially helps users. (2) Peddler — you'd use it yourself but it doesn't help users. (3) Entertainer — you wouldn't use it but it helps users. (4) Dealer — you wouldn't use it AND it doesn't help users. Only build Facilitators.
**Values:** Facilitator: build with confidence. Peddler: proceed with caution, add genuine value. Entertainer: acknowledge the entertainment value, don't pretend it's more. Dealer: do not build.
**Don't:** Build Dealer products. Don't rationalize manipulative patterns as "engagement". Don't use the Hook Model without considering which quadrant you're in.

---

## Checklist

- [ ] All four Hook cycle stages are explicitly designed (Trigger > Action > Variable Reward > Investment)
- [ ] Internal triggers identified and mapped to user emotions
- [ ] Trigger-to-action distance: 1 click/tap maximum
- [ ] Ability barriers assessed across all 6 simplicity factors
- [ ] Reward type matches user motivation (Tribe/Hunt/Self)
- [ ] Rewards have variability — not predictable
- [ ] Investment is requested after reward delivery, not before
- [ ] At least 2 forms of stored value are implemented
- [ ] Each investment loads a future trigger
- [ ] User autonomy is maintained — easy opt-out for everything
- [ ] Product is in the Facilitator quadrant of the Manipulation Matrix
- [ ] Investments are staged progressively (small to large over time)
- [ ] Habit-forming features use consistent context + behavior + reward
- [ ] New vs returning users get different flow designs
- [ ] Frequently used controls maintain stable positions (muscle memory)
- [ ] Leaderboards show local neighborhood, not full rankings
- [ ] Every microinteraction has all 4 parts: Trigger > Rules > Feedback > Loops
- [ ] Primary actions use Level 1 triggers (visible + labeled)
- [ ] System triggers are configurable and opt-in
- [ ] Feedback is immediate (<100ms), proportional, and non-arbitrary
- [ ] Feedback channel matches context (visual default, audio for background, haptic for mobile)
- [ ] 1-3 Signature Moments identified and polished
- [ ] Long loops reduce UI chrome as users gain mastery
- [ ] Spring-loaded modes preferred over toggle modes for brief states
- [ ] Surprises placed at strategic points (1-2 per session max)
- [ ] Viral actions positioned as primary, not secondary

---

---

# Chapter 11: Persuasion & Trust Patterns

Persuasion follows predictable psychological principles. Used ethically, these patterns help users make decisions aligned with their own interests. Used manipulatively, they erode trust and create backlash. Every technique here has a corresponding dark pattern — know both to use one and avoid the other.

**When to Use:**
- Designing onboarding and conversion flows
- Building pricing and upgrade experiences
- Creating social proof and trust signals
- Writing persuasive copy and CTAs
- Auditing for dark patterns and manipulative design

| Quick Reference | Value |
|----------------|-------|
| Cialdini's principles | 6: Reciprocity, Commitment, Social Proof, Liking, Authority, Scarcity |
| Foot-in-the-door conversion lift | 2-3x over cold asks |
| Social proof minimum | 10+ testimonials or 1,000+ users for credibility |
| Authority signals needed | Minimum 3 visible credibility markers |
| Scarcity effectiveness | Newly scarce > Always scarce by 30-50% |
| Dark pattern categories | 13 types to avoid |
| Priming placement | 1-3 steps before target action |

---

## Reciprocity

### Rule: Give Before You Ask

**When:** Designing free trials, freemium features, content marketing, or lead generation.
**Do:** Provide genuine, unrestricted value before asking for anything in return. Free tools, useful content, generous trial periods. The value must be real and useful on its own — not a teaser. When users receive value, they feel psychologically obligated to reciprocate.
**Values:** Free value delivered: before any signup required. Trial period: minimum 14 days for SaaS. Free tier: must solve a real use case completely, not just demonstrate.
**Don't:** Gate content behind email walls immediately. Don't provide "free" tools that are useless without upgrading. Don't give token gestures (a 3-day trial is an insult, not reciprocity).

### Rule: Reciprocal Concessions (Door-in-the-Face)

**When:** Presenting pricing tiers or feature packages.
**Do:** Show the premium option first, then present the standard option as a concession. "Enterprise: $299/mo. Not ready for that? Standard at $49/mo gives you everything you need to start." The standard option feels like a reasonable concession from the larger ask.
**Values:** Present options in descending price order: Premium > Standard > Basic. The middle option typically gets 60-70% of selections (compromise effect). Lead with the highest-value option.
**Don't:** Start with the cheapest option and upsell (less effective). Don't make the price gap between tiers so large it feels absurd. Don't hide the premium option — it's the anchor.

### Rule: Personalize the Gift

**When:** Implementing reciprocity-based features.
**Do:** Tailored gifts trigger stronger reciprocity than generic ones. Personalized recommendations, content curated to user history, features unlocked based on usage patterns. "Based on your projects, here's a custom template" beats "Here's our template library."
**Values:** Personalized reciprocity: 2-4x more effective than generic. Include the user's name, usage data, or stated preferences. Minimum personalization: reference one specific user attribute.
**Don't:** Send mass "gifts" with no personalization. Don't over-personalize to the point of creepiness (referencing data the user didn't knowingly share). Don't automate personalization without quality checks.

---

## Commitment & Consistency

### Rule: Foot-in-the-Door

**When:** Seeking user commitment — account creation, subscriptions, feature adoption.
**Do:** Start with a small, easy commitment. Users who agree to a small request are 2-3x more likely to agree to a larger related request later. Start with "Create a free account" before "Upgrade to Pro." Get users to set a preference before asking them to complete a profile.
**Values:** First ask: < 30 seconds to complete. Second ask: within 1-3 sessions of first commitment. Conversion lift: 2-3x over cold large asks. Each commitment should be slightly larger than the last.
**Don't:** Jump to large asks from new users. Don't make the small commitment so trivial it doesn't register as a commitment. Don't wait too long between small and large asks (the consistency effect fades).

### Rule: Make Commitments Active, Public, Effortful, and Freely Chosen

**When:** Designing onboarding steps, settings, or preference selections.
**Do:** Active commitments (typing, selecting, creating) bind more strongly than passive ones (checking a box). Public commitments (shared profiles, reviews) bind more than private ones. Some effort invested increases commitment. All commitments must feel freely chosen — forced commitments create reactance.
**Values:** Active > Passive by 2x. Public > Private by 2x. Effortful > Easy by 1.5x. Freely chosen > Forced by 3x+. Combine: an active, public, effortful, freely chosen commitment is maximally binding.
**Don't:** Pre-check boxes and call it commitment. Don't force public commitments without consent. Don't make effort artificially high to increase commitment (users will abandon instead).

### Rule: Inner Choice Over External Pressure

**When:** Designing incentive structures for user commitment.
**Do:** Remove external justifications so users internalize their commitment. "You're using our product because it makes you more productive" is more durable than "You're using our product because of the $5 discount." External rewards can undermine intrinsic motivation.
**Values:** Intrinsic motivation lasts indefinitely. Extrinsic motivation lasts only while the incentive exists. Once behavior is established, phase out external incentives and reinforce internal reasons.
**Don't:** Create permanent dependency on discounts or incentives. Don't reward behavior so heavily that users attribute their actions to the reward, not their own choice. Don't use large incentives for behaviors you want sustained long-term.

### Rule: Label Users by Their Best Behavior

**When:** Encouraging continued engagement or desired behavior.
**Do:** Telling users "You're a power user" or "You're among our most engaged" creates a self-image they'll work to maintain. The label creates the consistency pressure — once someone accepts an identity, they act to confirm it.
**Values:** Identity labels increase follow-through on consistent behavior. "You've been a great contributor" leads to more contributions. Labels work even when users know they're being labeled.
**Don't:** Use labels that create obligation ("You owe us"). Don't label falsely — the label must have some basis in real behavior.

---

## Social Proof

### Rule: Show What Similar Others Do

**When:** Displaying user counts, testimonials, reviews, or usage statistics.
**Do:** Show evidence of others' behavior: "10,000+ teams use this", "4.8/5 from 2,000 reviews", "Most Popular" badges. Social proof is most powerful when users are uncertain. Place social proof near decision points (pricing pages, signup forms, checkout).
**Values:** Minimum for credibility: "1,000+ users" or "100+ reviews". Display exact numbers when large ("12,847 customers"), round numbers when smaller ("100+"). Star ratings: show only if 4.0+ average. Include source attribution.
**Don't:** Show low numbers ("3 people are viewing this" looks desperate). Don't display social proof without context ("Loved by users" — how many?). Don't show social proof that's outdated (reviews from 3 years ago).

### Rule: Similarity in Social Proof

**When:** Selecting which testimonials, case studies, or user examples to display.
**Do:** People follow the behavior of similar others. Segment social proof by user type: "Trusted by startups like yours", show testimonials from the user's industry, display usage stats from comparable companies. Similarity increases social proof effectiveness by 2-3x.
**Values:** Segment social proof by: industry, company size, role, geography, use case. Match at least 2 attributes to the current user. Display the most similar testimonials first.
**Don't:** Show Fortune 500 logos to indie developers. Don't display consumer testimonials to enterprise buyers. Don't mix segments without labels.

### Rule: Avoid Negative Social Proof

**When:** Writing copy about user behavior, compliance, or adoption.
**Do:** Frame social proof positively. "70% of users complete their profile" not "30% of users never complete their profile." Negative social proof normalizes the undesired behavior — if 30% don't do it, it feels acceptable not to.
**Values:** Always frame the majority behavior: "Most users...", "70%+ of teams...", "The majority choose...". If the desired behavior is not yet the majority, use aspiration framing: "Top-performing teams do X."
**Don't:** Publish stats about undesired behavior ("60% of users churn in the first month"). Don't use negative framing in campaigns ("Stop being one of the 40% who..."). Don't normalize non-compliance with your own messaging.

---

## Liking

### Rule: Visual Appeal Creates a Halo Effect

**When:** Designing any user-facing surface — marketing pages, product UI, onboarding.
**Do:** Attractive designs are perceived as more trustworthy, more competent, and easier to use. The halo effect means positive impressions in one area (visual appeal) transfer to other areas (perceived reliability). Invest in visual polish at trust-critical touchpoints: landing pages, pricing pages, checkout.
**Values:** Professional photography: 2x trust over stock photos. Consistent visual design: 1.5x perceived reliability. Visual polish at checkout: 20-30% reduction in abandonment.
**Don't:** Use low-quality images, inconsistent styling, or broken layouts at decision points. Don't assume substance alone is sufficient — presentation matters for trust. Don't over-design at the expense of performance (slow pages kill trust faster than ugly ones).

### Rule: Similarity Breeds Liking

**When:** Writing copy, choosing imagery, or designing brand voice.
**Do:** Mirror the language, values, and aesthetic preferences of your target users. Developers trust developer-style interfaces (monospace fonts, dark mode, terminal aesthetics). Enterprise buyers trust polished, formal presentations. Match your audience's self-image.
**Values:** Language: use vocabulary from user interviews, not marketing jargon. Imagery: feature people who look like your users. Tone: match the formality level of your user's workplace.
**Don't:** Use corporate language for indie developers. Don't use casual language for healthcare or finance. Don't create a disconnect between brand personality and user personality.

### Rule: Compliments Work Even When Transparent

**When:** Designing success states, achievement notifications, or onboarding progress.
**Do:** Genuine praise works even when users know it's designed: "Great choice!", "You're all set — that was fast!", "Your project is looking professional." Positive reinforcement at key moments increases satisfaction and completion rates.
**Values:** Praise: at every major milestone (account created, first action completed, goal reached). Specificity: "Your dashboard is set up with 3 data sources" beats "Good job!". Timing: immediately after the user's action.
**Don't:** Praise trivial actions ("Amazing! You clicked a button!"). Don't be condescending. Don't praise in contexts where users are frustrated (error recovery).

### Rule: Look-and-Feel Is the First Trust Signal

**When:** Designing landing pages, sign-up flows, or first-impression surfaces.
**Do:** Users decide whether to trust a website within 50ms, based almost entirely on visual design. Professional typography, consistent spacing, quality imagery signal credibility before any content is read.
**Values:** No broken images, misaligned elements, or inconsistent styles on landing pages. Quality imagery: real photos or professional illustrations.
**Don't:** Launch with placeholder content or unpolished design. Don't ignore visual bugs on first-impression surfaces.

### Rule: Stories Persuade More Than Feature Lists

**When:** Writing onboarding copy, feature descriptions, case studies, or empty states.
**Do:** Frame information as narrative. Stories activate causal thinking, increase retention, and drive emotional engagement. A story with a character and transformation outperforms bullet points.
**Values:** Empty state: "Sarah had 50 tabs of research. Now she searches one library." > "Store and search documents." Testimonials: story format > rating format.
**Don't:** Rely solely on bullet-point feature lists. Don't call out that you're using persuasion techniques (breaks the effect).

### Rule: Association and Conditioning

**When:** Building brand perception.
**Do:** Users transfer feelings from context to product. Pleasant experiences build favorable associations. The environment in which users encounter your brand colors their perception of it.
**Values:** Never deliver bad news alongside brand identity without buffer. Pair product with positive outcomes.
**Don't:** Fabricate associations. Don't use misleading celebrity endorsements.

---

## Authority

### Rule: Display Credibility Signals

**When:** Building trust on landing pages, pricing pages, or any decision-critical screen.
**Do:** Show credentials, certifications, press mentions, client logos, expert endorsements, and security badges. Authority signals reduce perceived risk. Place them near CTAs and in the decision flow.
**Values:** Minimum 3 credibility markers on landing pages. Client logos: 4-6, recognizable to target audience. Security badges: SSL, SOC 2, GDPR near checkout. Press mentions: publication logos with dates.
**Don't:** Fabricate credentials or endorsements. Don't show credentials irrelevant to the user's concern. Don't clutter decision areas with too many logos (8+ feels desperate).

### Rule: Three Authority Symbols

**When:** Establishing authority through UI design or content.
**Do:** Authority is communicated through three channels: (1) Titles — credentials, certifications, years of experience. (2) Appearance — professional design, quality photography, polished presentations. (3) Trappings — the tools and associations that signal competence (enterprise clients, industry awards, technology partnerships).
**Values:** Use at least 2 of 3 authority symbol types. Titles: specific credentials ("SOC 2 certified") over vague claims ("industry-leading"). Trappings: real partnerships and integrations, not aspirational claims.
**Don't:** Claim authority without evidence. Don't use vague authority signals ("trusted by thousands" without specifics). Don't rely on a single authority channel.

### Rule: Argue Against Own Interest

**When:** Building trust through content, product descriptions, or sales copy.
**Do:** Admit a small weakness to establish credibility for larger claims. "We're not the cheapest option, but we're the most reliable." "Our UI has a learning curve, but power users save 3 hours per week." Acknowledging drawbacks makes positive claims 2x more believable.
**Values:** Acknowledge 1 real limitation before stating 2-3 genuine strengths. The limitation should be minor relative to the strengths. Frame the limitation as a trade-off, not a deficiency.
**Don't:** Acknowledge a critical weakness (price is a minor weakness; frequent data loss is not). Don't use fake weaknesses ("Our only flaw is that we're too innovative"). Don't list weaknesses without stronger compensating strengths.

---

## Scarcity

### Rule: Limited Availability Increases Perceived Value

**When:** Displaying inventory, offer duration, or access restrictions.
**Do:** Show genuine scarcity: limited seats, time-bound offers, waitlists, exclusive access. Scarcity activates loss aversion — the fear of missing out is stronger than the desire to gain.
**Values:** Specificity: "7 seats left" not "limited availability". Time: countdown timer with exact end date. Access: "invite-only" or "limited beta" with clear criteria.
**Don't:** Fake scarcity (perpetual countdown timers, fake "only 2 left"). Don't apply scarcity to digital goods with no actual limit (undermines trust). Don't use scarcity for essential services (creates anxiety, not desire).

### Rule: Newly Scarce Is More Powerful Than Always Scarce

**When:** Introducing limitations or changing availability.
**Do:** Items that become scarce after being abundant trigger stronger desire than items that were always scarce. "Price increasing from $49 to $99 on March 1" is more motivating than always pricing at $49. Communicate the change in availability.
**Values:** Newly scarce: 30-50% stronger response than always scarce. Communicate the transition: "Previously unlimited, now limited to 100/month." Give notice before scarcity takes effect (24-72 hours).
**Don't:** Make things permanently scarce from day one without explanation. Don't create artificial scarcity transitions. Don't remove features users already have without strong justification.

### Rule: Competition Amplifies Scarcity

**When:** Multiple users or buyers compete for the same resource.
**Do:** Show competitive demand: "5 others are looking at this", "3 teams on the waitlist ahead of you". Competition intensifies the scarcity response because it adds social proof and urgency simultaneously.
**Values:** Display real-time demand signals when genuine. Show waitlist position with estimated wait time. Competition signals: effective only if truthful and verifiable.
**Don't:** Fabricate competition signals. Don't show competitive demand for unlimited resources. Don't create anxiety in contexts where competition isn't real.

### Rule: Exclusive Information Scarcity

**When:** Presenting data, insights, or information that has limited distribution.
**Do:** Information itself can be scarce. Customers told that information was exclusive bought 6x more than those given a standard pitch. Frame proprietary data and unique insights as exclusive access. "This data available only to Pro users."
**Values:** Exclusive information: 6x conversion over standard framing. Frame insights as limited-access: "Only available to [tier] members." Combine with authority: exclusive data from a credible source is maximally persuasive.
**Don't:** Fabricate exclusivity for publicly available information. Don't gate trivially available data behind exclusivity framing.

### Rule: Wanting Is Not Enjoying

**When:** Setting expectations about scarcity-driven features.
**Do:** Scarcity increases wanting but does not increase satisfaction after acquisition. Users who fought for access expect extraordinary quality. Set appropriate expectations. Deliver an experience that justifies the scarcity.
**Values:** Post-acquisition satisfaction must meet pre-acquisition expectations. Scarce items face 2x scrutiny. Follow scarcity signals with exceptional onboarding and first-use experience.
**Don't:** Use scarcity to drive signups for mediocre products (churn will spike). Don't create exclusive access without exclusive quality. Don't rely on scarcity to compensate for a weak value proposition.

---

## Priming & Perception

### Rule: Priming User Perceptions

**When:** Designing onboarding flows, pre-task screens, or task sequences.
**Do:** Expose users to positive stimuli before asking them to complete important tasks. Priming shapes response to subsequent stimuli by activating memory associations. Layer positive micro-interactions along the pathway to conversion or task completion. Three types of priming work in interfaces: (1) **Visual priming** — attractive design primes trust; polished aesthetics before a signup form increase completion. (2) **Tonal priming** — friendly, approachable copy primes willingness to engage; warm language before a support form reduces hostility. (3) **Sequential priming** — small positive experiences prime willingness for larger commitments; a quick win before a complex setup increases follow-through.
**Values:** Place priming elements 1-3 steps before the target action. Visual: ensure pages before conversion points are aesthetically strong. Tonal: use warm, encouraging language in the steps leading to commitment. Sequential: deliver a small success (saved first item, saw first result) before asking for investment.
**Don't:** Prime users with negative stimuli before asking for commitment (error messages, warnings, or frustrating steps immediately before signup). Don't use priming to manipulate users against their interests. Don't place the most frustrating step immediately before the conversion action.

---

## Persuasion & Trust Design

### Rule: Defense Strategies (Recognizing Persuasion)

**When:** Building products that help users evaluate offers, make purchases, or compare products.
**Do:** Help users recognize when persuasion techniques are being used on them. For each principle, teach the defense:
- Reciprocity: "Is this gift genuine or a compliance trick?"
- Consistency: "Knowing what I now know, would I make the same choice?"
- Social proof: "Is this evidence real or manufactured?"
- Liking: "Have I come to like this seller more than expected?"
- Authority: "Is this person truly an expert? How truthful can they be?"
- Scarcity: "Do I want this to own it or to use it?"
**Values:** Add cooling-off periods before scarcity-triggered purchases. Show "Review your original reasons" before subscription renewals. Flag unattributed testimonials.
**Don't:** Exploit these vulnerabilities in your own product. Transparency is the test: ethical persuasion survives exposure.

### Rule: The Contrast Principle

**When:** Presenting items in sequence — pricing, features, plans.
**Do:** Present items in strategic order. The second item is perceived relative to the first, not in absolute terms. Show higher-priced options first so standard feels like better value.
**Values:** Show premium first, then mid-tier feels smart. Show original price before discount. Real estate: show a worse option first to make the next shine.
**Don't:** Anchor with unrealistically high numbers. Don't hide reference prices.

### Rule: Use Familiar Patterns When Users Are Anxious

**When:** Users are in stressful contexts (payment, deletion, error recovery, security).
**Do:** Use maximally familiar UI patterns. Stressed users strongly prefer the familiar. Novel interactions in high-stakes moments increase anxiety and abandonment.
**Values:** Checkout: standard flow, familiar field labels. Delete confirmation: conventional modal. Security: patterns from major platforms as reference.
**Don't:** Experiment with novel patterns in stressful flows. Don't use playful copy in high-stakes errors.

### Rule: Frame Value as Time Saved, Not Money Saved

**When:** Writing pricing copy, value propositions, or upgrade prompts.
**Do:** Time framing creates stronger personal connection than money framing. People value their time more emotionally than their money.
**Values:** "Save 5 hours/week" > "Save $50/month." "Set up in 2 minutes" > "Only $9.99."
**Don't:** Lead with price when time savings are available.

---

## Dark Pattern Indicators

### Rule: 13 Dark Pattern Red Flags

**When:** Auditing any persuasive design for ethical compliance.
**Do:** Check your product against these 13 dark patterns and eliminate any matches:

1. **Roach Motel** — easy to get in, hard to get out (cancellation harder than signup)
2. **Trick Questions** — confusing opt-in/opt-out language (double negatives)
3. **Sneak into Basket** — adding items during checkout without consent
4. **Forced Continuity** — charging after free trial without clear warning
5. **Hidden Costs** — fees revealed only at final checkout step
6. **Bait and Switch** — advertising one thing, delivering another
7. **Confirmshaming** — guilt-trip decline buttons ("No, I don't want to save money")
8. **Disguised Ads** — ads designed to look like content or navigation
9. **Misdirection** — visual design that draws attention away from important information
10. **Privacy Zuckering** — sharing more data than intended through confusing settings
11. **Friend Spam** — importing contacts without clear consent for messaging
12. **Forced Disclosure** — requiring personal information unrelated to the service
13. **Infinite Scroll Traps** — removing natural stopping points to maximize time spent

**Values:** Zero tolerance for patterns 1-6 (legally risky). Patterns 7-13: redesign immediately if detected. Audit quarterly.
**Don't:** Rationalize dark patterns as "industry standard." Don't use confirmshaming even as humor. Don't hide unsubscribe links.

### Rule: Context Appropriateness

**When:** Deciding which persuasion techniques to use for your product type.
**Do:** Match persuasion intensity to product type and user vulnerability.

| Technique | SaaS/Tools | E-commerce | Health/Finance | Children's Products |
|-----------|-----------|------------|----------------|-------------------|
| Social Proof | Yes | Yes | Careful | No |
| Scarcity | Mild | Yes | No | No |
| Reciprocity | Yes | Yes | Yes | Mild |
| Authority | Yes | Yes | Required | Required |
| Commitment | Yes | Mild | Careful | No |
| Urgency | Mild | Yes | No | No |

**Values:** Higher user vulnerability = lower persuasion intensity. Regulated industries (health, finance): authority and transparency only. Products for children: minimize all persuasive techniques.
**Don't:** Apply e-commerce urgency tactics to healthcare decisions. Don't use social proof for children's products. Don't use scarcity in financial services.

### Rule: The Golden Rule

**When:** Making any decision about persuasive design.
**Do:** Build products you would want your family to use. If a technique would feel manipulative if used on your parent, partner, or child, don't use it on your users.
**Values:** Single ethical test: "Would I be comfortable if my family knew exactly how this works?" If yes, proceed. If no, redesign.
**Don't:** Separate "business decisions" from ethical considerations. Don't assume sophisticated users are immune to manipulation. Don't optimize metrics at the expense of user wellbeing.

---

## Checklist

- [ ] Free value delivered before any ask (reciprocity)
- [ ] Pricing shown in descending order (anchor high, concede down)
- [ ] First commitment is < 30 seconds to complete
- [ ] Social proof: 3+ credibility signals near CTAs
- [ ] Social proof segments match the current user type
- [ ] All social proof framed positively (majority behavior)
- [ ] Authority: 3+ credibility markers on decision pages
- [ ] 1 acknowledged weakness paired with 2-3 compensating strengths
- [ ] Scarcity signals are genuine and specific (exact numbers)
- [ ] All 13 dark patterns checked and eliminated
- [ ] Persuasion intensity appropriate for product type and audience
- [ ] Golden rule test passed: would you want your family to experience this?
- [ ] Users labeled by positive behavior, not obligation
- [ ] Familiar UI patterns used in stressful contexts
- [ ] Value framed as time saved where applicable
- [ ] Stories used alongside feature lists for persuasion
- [ ] Visual design polished on all first-impression surfaces (50ms trust test)
- [ ] Priming elements placed 1-3 steps before target actions (visual, tonal, sequential)

---

---

# Chapter 12: Form Design & User Input

Forms are where users exchange effort for value. Every unnecessary field, unclear label, or confusing error message costs conversions. Form design is the highest-ROI design investment — removing one field can increase completion by 5-10%. Good form design prevents errors at the control level rather than catching them after submission.

**When to Use:**
- Designing registration, checkout, or data entry forms
- Building search interfaces and filter panels
- Creating settings and configuration pages
- Implementing error handling and validation
- Designing for both touch and pointer input

| Quick Reference | Value |
|----------------|-------|
| Touch target minimum | 44x44px (mobile), 32x32px (desktop) |
| Recommended touch target | 48x48px |
| Label position | Top-aligned (fastest completion) |
| Validation timing | On blur (after leaving field) |
| Fields to completion rate | Each field removed = +5-10% completion |
| Error message formula | What happened + Why + How to fix |
| Error prevention priority | Prevention > Detection > Recovery |
| Constraint types | 4: Physical, Semantic, Cultural, Logical |

---

## Target Sizing

### Rule: Fitts's Law Applied

**When:** Sizing and placing interactive elements — buttons, links, form fields, toggles.
**Do:** Target size should be proportional to: (1) frequency of use and (2) importance of the action. More important actions get larger targets. Targets closer together require more precision and slow users down. Place primary CTAs in easy-to-reach locations with generous sizing.
**Values:** Primary CTA: minimum 48px height, full-width on mobile. Secondary actions: minimum 44px touch / 32px pointer. Icon buttons: minimum 44x44px touch area (icon can be smaller, tap target must not be). Spacing between adjacent targets: minimum 8px.
**Don't:** Make destructive actions the same size as constructive actions. Don't place small targets adjacent to each other without spacing. Don't make form submit buttons smaller than form fields.

### Rule: Place Destructive Actions Far from Constructive Ones

**When:** Positioning actions like Delete, Cancel, Remove near Save, Submit, Confirm.
**Do:** Physically separate destructive actions from constructive ones. Place them on opposite sides of the screen or in different visual groups. Use color differentiation: constructive (primary color), destructive (red or muted). Add confirmation dialogs for irreversible destructive actions.
**Values:** Minimum distance: 24px between destructive and constructive buttons on desktop, 32px on mobile. Destructive actions: secondary styling (outlined or text-only), never primary button styling. Confirmation: required for any data loss.
**Don't:** Place "Delete" next to "Save." Don't style destructive actions as primary buttons. Don't allow single-click irreversible deletion without confirmation.

### Rule: Touch Target Sizes

**When:** Designing for mobile or touch-enabled interfaces.
**Do:** Follow minimum target sizes strictly. The finger pad covers approximately 44px — anything smaller causes mis-taps. Add padding to increase tap area even when the visual element is smaller.
**Values:** Recommended: 48x48px. Minimum: 44x44px (WCAG 2.5.5). Dense UIs: 32x32px absolute minimum with 8px gap. The tap target can be larger than the visual element using padding.
**Don't:** Use 24px tap targets on mobile. Don't measure tap target by the visual size of the icon (a 16px icon needs a 44px tap area). Don't place multiple small targets in a row without adequate spacing.

### Rule: Natural Mapping (Spatial Analogy)

**When:** Arranging controls that affect spatial or sequential outcomes (volume sliders, layout editors, navigation, list reordering).
**Do:** Map control layout to the spatial layout of what they control (left control = left output, top slider = top element). Use spatial analogy: arrange controls in the same pattern as the things they affect. For sequential controls, use natural orderings (left-to-right = earlier-to-later, top-to-bottom = first-to-last). Group related controls near the things they modify.
**Values:** Intuitive operation, zero learning curve, error reduction.
**Don't:** Arrange controls in a grid when the things they control have a different spatial layout. Don't separate a control from the element it affects by large distances or on different screens. Don't use arbitrary ordering when a natural spatial mapping exists.

---

## Form Layout

### Rule: One Column Forms

**When:** Designing form layout for any multi-field form.
**Do:** Use a single-column layout. Users complete single-column forms 15-25% faster than multi-column forms because the eye path is a simple vertical scan. The only exception: closely related short fields like First Name / Last Name or City / State / Zip.
**Values:** One column for all forms. Exception fields: name pairs, city/state/zip, date components (MM/DD/YYYY). Maximum width: 500-600px for form container.
**Don't:** Place unrelated fields side by side to "save space." Don't use grid layouts for forms. Don't let forms stretch to full viewport width on desktop.

### Rule: Top-Aligned Labels

**When:** Choosing label placement for form fields.
**Do:** Place labels above their input fields (top-aligned). This produces the fastest completion times and works across all viewport sizes. Labels should be 12-14px, medium weight, and 4-8px above the input.
**Values:** Label position: above input, left-aligned. Label size: 12-14px. Label weight: medium (500-600). Gap between label and input: 4-8px. Gap between field groups: 16-24px.
**Don't:** Use left-aligned labels (slow eye movement). Don't use placeholder text as labels (disappears on input, accessibility failure). Don't use floating labels as the only label (unreliable on autofill).

### Rule: Group Related Fields

**When:** Organizing forms with more than 5 fields.
**Do:** Group semantically related fields with visual proximity: a shared heading, border, or background. "Personal Information" (name, email), "Address" (street, city, state, zip), "Payment" (card, expiry, CVC). Visual proximity signals semantic relationship.
**Values:** Group heading: 16-18px, semibold. Group spacing: 32-48px between groups, 16-24px between fields within a group. Visual grouping: subtle background color or top border.
**Don't:** Present 15 ungrouped fields in a flat list. Don't use heavy borders or boxes around groups (adds visual noise). Don't create groups of 1 field (not a meaningful group).

### Rule: Reduce Fields to Minimum

**When:** Designing any form.
**Do:** Every field you remove increases completion rate by 5-10%. Challenge every field: Can it be auto-filled? Derived from other data? Asked later? Made optional? Remove "How did you hear about us?" from signup forms. Remove "Company" if not immediately needed. Ask only what's required for the current step.
**Values:** Registration form: email + password (2 fields ideal). Checkout: minimum viable fields per step. Each field removed: +5-10% completion. If a field doesn't block the current action, defer it.
**Don't:** Collect data "just in case." Don't add fields for analytics purposes in user-critical flows. Don't ask the same information twice (shipping = billing unless unchecked).

---

## Error Prevention & Constraints

### Rule: Four Types of Constraints

**When:** Preventing user errors in forms, configuration screens, or any input that can go wrong.
**Do:** Apply four constraint types to eliminate errors at the source:
  - **Physical constraints**: disable impossible options, grey out unavailable actions, use input masks (date pickers instead of free text)
  - **Semantic constraints**: only show options that make sense in context (don't offer "delete" on something that can't be deleted)
  - **Cultural constraints**: follow platform conventions (red = danger/stop, green = success/go, X = close)
  - **Logical constraints**: if only one valid option remains, auto-select it; if a choice eliminates others, hide or disable them immediately
**Values:** Error prevention at the source, reduced need for error messages, guided completion.
**Don't:** Show all options including invalid ones and rely on validation to catch errors after the fact. Don't override cultural conventions without strong justification (e.g., green for errors). Don't leave the user to figure out constraints through trial and error.

### Rule: Error Taxonomy — Slips vs Mistakes

**When:** Designing error prevention, error messages, and recovery flows.
**Do:** Distinguish **slips** (right goal, wrong action) from **mistakes** (wrong goal entirely) — they need different solutions:
  - For **capture slips** (doing a frequent action instead of the intended one): make destructive actions visually and spatially distinct from common actions
  - For **description-similarity slips** (acting on the wrong similar-looking item): make similar items visually distinguishable (different icons, colors, or prominent labels)
  - For **mode-error slips** (acting as if in a different mode): make the current mode highly visible, or eliminate modes entirely
  - For **memory-lapse slips** (forgetting a step): use checklists, progress indicators, and forced-function sequences
  - For **mistakes** (wrong mental model): provide better feedback, tutorials, and undo rather than just error messages
**Values:** Targeted error prevention, proportional intervention, reduced user blame.
**Don't:** Treat all errors the same way with generic "something went wrong" messages. Don't place destructive actions (delete, send, submit) adjacent to frequent actions (save, edit, back). Don't use invisible modes where the same button does different things depending on hidden state.

### Rule: Forcing Functions

**When:** A user error would cause irreversible or severe consequences (data loss, financial transactions, destructive operations).
**Do:** Use **interlocks**: require a specific sequence of actions before a dangerous operation (e.g., type "DELETE" to confirm deletion). Use **lock-ins**: prevent the user from leaving a dangerous state without completing safety steps (e.g., "Save changes?" dialog before closing). Use **lock-outs**: prevent entry into a dangerous state without meeting prerequisites (e.g., disable "Deploy" until tests pass). Scale the forcing function to the severity.
**Values:** Proportional safety, prevented catastrophes, user awareness of consequences. Mild confirmation for moderate risk, typed confirmation for severe risk.
**Don't:** Use heavy forcing functions for low-risk, easily reversible actions (don't require typed confirmation to delete a draft). Don't overuse confirmation dialogs until users click through them reflexively ("confirmation fatigue"). Don't block the user without explaining what they need to do to proceed.

### Rule: Undo over Confirmation

**When:** Designing safety nets for user actions, especially destructive or significant ones.
**Do:** Prefer undo over "Are you sure?" dialogs — undo lets users act confidently and recover gracefully. Make undo visible and easily accessible immediately after the action (toast with "Undo" button, Ctrl+Z support). For truly irreversible actions (send email, charge credit card), use a brief delay window ("Sending in 5 seconds... [Cancel]") rather than a pre-action confirmation. Support multi-level undo with a visible history when feasible.
**Values:** User confidence, speed of interaction, graceful recovery, reduced confirmation fatigue.
**Don't:** Use confirmation dialogs as the primary safety mechanism (users learn to click "OK" reflexively). Don't make undo hidden or hard to discover (buried in menus, no keyboard shortcut). Don't silently discard undo history when the user navigates away.

### Rule: Poka-Yoke (Mistake-Proofing at the Control Level)

**When:** Designing any input control where users could enter invalid data — forms, configuration panels, filters, date ranges, numeric inputs, selection interfaces.
**Do:** Prevent errors at the interaction level rather than catching them after submission. Use **constrained controls** — sliders for ranges, date pickers for dates, dropdowns for known option sets. Use **smart disabling** — gray out options that are invalid given current state (return date before departure date, past dates for future events). Use **inline transformation** — auto-format phone numbers as typed, auto-capitalize proper nouns, auto-complete from known lists.
**Values:** Prevention > Detection > Recovery. A slider that constrains to valid range is better than a text field that validates after submission. A date picker that disables past dates is better than an error message saying "Date must be in the future." Every error message in your product represents a failure to prevent the error in the first place.
**Don't:** Use free-text inputs when the valid set is known and finite (<20 options = dropdown; range = slider; date = picker). Don't validate after the fact when you could constrain in advance. Don't show error messages for errors that the UI should have prevented. Don't over-constrain to the point of frustration (if 90% of users need custom input, a constrained control is wrong).

---

## Validation & Errors

### Rule: Inline Validation

**When:** Validating form input in real time.
**Do:** Validate on blur (when the user leaves the field), not on keystroke. Show success indicators (green checkmark) for valid fields and error messages for invalid ones. Place error messages directly below the offending field in red (or your error color) with an icon.
**Values:** Trigger: on blur (field loses focus). Success indicator: green checkmark or border. Error indicator: red border + icon + message below field. Message position: immediately below the field, 4px gap.
**Don't:** Validate on every keystroke (validates incomplete input, frustrating). Don't validate on page load (nothing is wrong yet). Don't show error messages far from the field. Don't clear the user's input on error.

### Rule: Error Messages Must Identify, Explain, and Fix

**When:** Writing error messages for any validation failure.
**Do:** Every error message must answer three questions: (1) What went wrong? (2) Why? (3) How to fix it. "Please enter a valid email address (example: name@domain.com)" not "Invalid input." Be specific, human, and prescriptive.
**Values:** Format: [What's wrong] + [How to fix]. Length: 1-2 sentences maximum. Tone: helpful, not blaming ("Please enter..." not "You failed to..."). Include an example of valid input when applicable.
**Don't:** Use generic messages ("Error", "Invalid input", "Something went wrong"). Don't blame the user ("You entered an invalid..."). Don't use error codes without human-readable text. Don't show multiple errors at once for a single field.

### Rule: Blame the System, Not the User

**When:** Writing error messages or failure states.
**Do:** Attribute problems to the situation, not the user (fundamental attribution error). "We couldn't process that" not "You entered invalid data." Users who feel blamed become frustrated and disengage.
**Values:** "Something went wrong on our end" > "You made an error." Passive voice for errors; active voice for successes ("You're all set!").
**Don't:** Use "invalid", "wrong", "incorrect." Write "didn't match", "not recognized", "try again" instead.

### Rule: Errors Are Inevitable — Design for Recovery

**When:** Building any form or input flow.
**Do:** Assume users will make errors. Preserve all valid input when errors occur. Highlight only the field(s) with errors. Scroll to and focus the first error field. Never clear the form on submission failure. Provide clear path to correct the error and resubmit.
**Values:** On error: preserve all input, highlight error fields, scroll to first error, focus first error field. Error rate assumption: 10-30% of form submissions contain at least one error. Recovery path: user should fix the error and submit in < 10 seconds.
**Don't:** Clear the form on error. Don't redirect to a separate error page. Don't require the user to re-enter valid fields. Don't show only a page-level error without identifying which field caused it.

### Rule: Stress Increases Errors

**When:** Designing high-stakes forms — checkout, financial transactions, medical input, time-sensitive actions.
**Do:** Simplify aggressively in high-stress contexts. Reduce fields, enlarge targets, use clear labels, provide reassurance text. Users under stress have reduced working memory and motor precision. Checkout under time pressure (flash sale) needs simpler forms than casual browsing.
**Values:** High-stress forms: 30% fewer fields than standard. Button sizes: 20% larger than standard in checkout. Reassurance text near submit: "Your data is encrypted" or "You can modify this later." Auto-save: every 15 seconds in long forms.
**Don't:** Add CAPTCHA at the end of checkout. Don't require account creation during checkout (offer guest checkout). Don't add promotional upsells in high-stress flows.

---

## Input Optimization

### Rule: Postel's Law for Inputs

**When:** Accepting user input — phone numbers, dates, addresses, codes.
**Do:** Be liberal in what you accept. Accept "(555) 123-4567", "555-123-4567", "5551234567", and "555.123.4567" — normalize behind the scenes. Accept "March 5, 2024", "3/5/24", "2024-03-05". Transform and format on the system side.
**Values:** Phone: accept any format, display formatted. Dates: accept multiple formats, store ISO 8601. Currency: accept with or without $ symbol, commas. Names: accept Unicode, don't restrict characters.
**Don't:** Reject valid input because of formatting. Don't show "Phone number must be in format (XXX) XXX-XXXX." Don't restrict input to a single format when the value is unambiguous. Don't strip accented characters from names.

### Rule: Use Smart Defaults

**When:** Pre-filling form fields or setting initial states.
**Do:** Pre-fill fields with the most likely value. Use geolocation for country/city. Default currency to user's locale. Pre-select the most common option. Repeat previous selections for returning users. Every default that's correct saves the user a decision.
**Values:** Default accuracy target: correct for 80%+ of users. Sources: geolocation, browser locale, user history, account data. Pre-fill: shipping address from profile, payment method from last order.
**Don't:** Default to a value that's wrong for most users. Don't pre-select terms and conditions or marketing opt-ins. Don't default to the most expensive option in pricing selections.

### Rule: Context-Aware Defaults (Don't Start from Zero)

**When:** Setting initial values for any control, form field, configuration, or interactive element.
**Do:** Use every available signal to provide an intelligent starting point: (1) **Device data** — location, time zone, language, screen size, (2) **User history** — last value used, frequency of selections, (3) **Social data** — what most users in this context choose, (4) **Environmental data** — time of day, day of week, season. An alarm clock app should default to a common wake-up time, not 12:00 AM. A shipping form should default to the user's country based on IP/locale.
**Values:** Default accuracy target: correct for 80%+ of users. Sources ranked by reliability: explicit user history > device signals > social/aggregate data > static best-guess. Every "empty" starting state is a design failure — always provide a meaningful default. Remember the user's last setting for repeat interactions.
**Don't:** Default to the first item alphabetically (arbitrary). Don't default to the developer's preference instead of the user's likely choice. Don't force users to set values that the system could infer. Don't forget defaults for returning users — if they set it once, remember it.

### Rule: Simple vs Easy vs Fast vs Minimal

**When:** Optimizing a multi-step process (checkout, registration, onboarding) for better completion rates.
**Do:** Choose the right optimization strategy based on context:
  - **Simpler** (fewer steps): Remove unnecessary fields. Auto-detect information (card type, country from IP).
  - **Easier** (more obvious steps): Add clear instructions. Break complex questions into multiple simple ones.
  - **Faster** (less time): Save previous answers. Use autocomplete and smart defaults. Add shortcuts for repeat users (1-click buy).
  - **Minimal** (fewer functions): Remove entire features that aren't core. Reduce scope, not just steps.
**Values:** First-time flow: prioritize Easy + Simple. Repeat-use flow: prioritize Fast. New product: prioritize Minimal. Mature product: mix Simple + Fast.
**Don't:** Confuse minimal visual design with minimal functionality. Don't simplify a form by hiding essential fields behind a "show more" toggle — that's harder, not simpler.

### Rule: Mark Optional Fields, Not Required

**When:** Indicating which fields are required vs optional.
**Do:** Most fields should be required (you've already eliminated unnecessary ones). Mark the few optional fields with "(optional)" text after the label. Don't use asterisks for required fields — they're learned but not intuitive.
**Values:** Mark optional fields with "(optional)" in lighter/smaller text after label. If most fields are optional, your form has too many fields — remove them. Asterisk (*) for required is acceptable but "(required)" is clearer.
**Don't:** Use asterisks without a legend. Don't mark both required and optional (one is sufficient). Don't make everything optional (if nothing is required, the form shouldn't exist).

### Rule: Use Correct HTML Input Types

**When:** Building forms for mobile and cross-device usage.
**Do:** Use the correct `type` attribute to trigger the right mobile keyboard. `type="email"` shows @ key. `type="tel"` shows number pad. `type="number"` shows numeric keyboard. `inputmode="numeric"` for non-number numeric inputs (credit cards).
**Values:** Email: `type="email"`. Phone: `type="tel"`. Numbers: `type="number"` or `inputmode="numeric"`. URLs: `type="url"`. Search: `type="search"`. Passwords: `type="password"` with show/hide toggle.
**Don't:** Use `type="text"` for everything. Don't use `type="number"` for credit cards (it adds increment arrows). Don't forget `autocomplete` attributes for browsers to auto-fill.

### Rule: Allow Zooming on Mobile

**When:** Building any web page for mobile.
**Do:** Never disable pinch-to-zoom. Both usability and WCAG requirement. Users with low vision depend on zoom; all users benefit when reading small text.
**Values:** Never set `user-scalable=no` or `maximum-scale=1.0`. Allow zoom to 200%.
**Don't:** Disable zooming.

---

## Checklist

- [ ] All touch targets are minimum 44x44px (48px recommended)
- [ ] Destructive and constructive actions are visually separated (24px+ distance)
- [ ] Form uses single-column layout
- [ ] Labels are top-aligned, 12-14px, 4-8px above input
- [ ] Related fields are visually grouped with headings
- [ ] Every field is justified — no "nice to have" fields
- [ ] Validation triggers on blur, not on keystroke
- [ ] Error messages: what happened + how to fix + example
- [ ] Error messages blame the system, not the user
- [ ] User input is preserved on error (form never clears)
- [ ] Inputs accept flexible formats (Postel's Law)
- [ ] Smart defaults pre-fill 80%+ correctly
- [ ] Optional fields marked "(optional)", not required marked with *
- [ ] Correct HTML input types used for mobile keyboards
- [ ] Pinch-to-zoom is never disabled on mobile
- [ ] All four constraint types applied (physical, semantic, cultural, logical)
- [ ] Slips and mistakes addressed with different prevention strategies
- [ ] Forcing functions scaled to severity (interlock > lock-in > lock-out)
- [ ] Undo preferred over confirmation dialogs for reversible actions
- [ ] Controls spatially mapped to what they affect (natural mapping)
- [ ] Constrained controls used instead of free-text when valid set is known (Poka-Yoke)
- [ ] Context-aware defaults use device, history, social, and environmental signals
- [ ] Optimization strategy chosen explicitly: simpler, easier, faster, or minimal

---

# Chapter 13: Responsive & Adaptive Design

Responsive design is not "make it fit smaller screens." It is a fundamental rethinking of layout, hierarchy, interaction targets, and content priority at each viewport size. Elements do not scale uniformly — large elements shrink faster, touch targets grow, and content reorders by importance.

The interaction style of your application should also match its **posture** — how long and how intensively users engage with it. A full-screen productivity app (sovereign posture) demands different density and controls than a quick-interaction dialog (transient posture) or a background notification system (daemonic posture). Responsive design adapts not just to screen size, but to usage context.

**When to Use:**
- Building any web interface that serves multiple device types
- Adapting desktop designs for mobile or tablet
- Choosing breakpoints and sizing strategies
- Designing touch-first interfaces
- Handling typography, images, and navigation across viewports
- Matching UI density and controls to application posture

| Quick Reference | Value |
|----------------|-------|
| Breakpoints | 640 / 768 / 1024 / 1280 / 1536px |
| Touch target | 44-48px |
| Pointer target | 32px |
| Content max-width | 65-75ch for text, 1280px for layout |
| Desktop headline ratio | 2.5x body size |
| Mobile headline ratio | 1.5-1.7x body size |
| Thumb zone | Bottom 1/3 of mobile screen |
| Text container safety factor | 1.5x expected content length |
| Button label i18n growth | 30-50% |

---

## Mobile-First Approach

### Rule: Mobile-First Design

**When:** Starting any responsive design project.
**Do:** Design for the smallest viewport first, then add complexity for larger screens. Mobile constraints force you to prioritize content and actions. Start with a 375px viewport, establish hierarchy, then enhance for 768px, 1024px, and wider.
**Values:** Base design: 375px wide. Enhancement steps: 640px > 768px > 1024px > 1280px > 1536px. Mobile design must be complete and usable on its own — not a stripped-down desktop.
**Don't:** Design desktop first and then "make it responsive." Don't hide critical features on mobile. Don't treat mobile as an afterthought.

### Rule: Breakpoint Scale

**When:** Defining responsive breakpoints in CSS.
**Do:** Use a consistent breakpoint scale. Apply breakpoints based on content needs, not device names. Test at each breakpoint and at sizes between them.
**Values:** 640px: large phone / small tablet. 768px: tablet portrait. 1024px: tablet landscape / small laptop. 1280px: desktop. 1536px: wide desktop. These are starting points — adjust if content breaks between them.
**Don't:** Target specific devices ("iPhone 14 breakpoint"). Don't use more than 5-6 breakpoints (maintenance burden). Don't ignore the spaces between breakpoints.

### Rule: Content Priority Shift

**When:** Adapting content layout across viewport sizes.
**Do:** Reorder content for mobile based on importance: hero/key message first, primary CTA second, supporting content third. On desktop, you can show more simultaneously because the viewport allows scanning. On mobile, content is consumed linearly — order is everything.
**Values:** Mobile order: (1) Key message/hero, (2) Primary CTA, (3) Key benefits (top 3), (4) Social proof, (5) Secondary content. Desktop can display these in parallel columns; mobile must stack them vertically.
**Don't:** Keep desktop column order on mobile (left column first, then right). Don't push the primary CTA below the fold on mobile. Don't show the same amount of content on mobile as desktop.

---

## Sizing & Typography

### Rule: Relative Sizing Doesn't Scale

**When:** Sizing elements across breakpoints.
**Do:** Size elements independently at each breakpoint. A desktop sidebar at 25% width becomes too narrow on tablet and too wide on mobile. A hero image at 50vh works on desktop but overwhelms mobile. Set explicit sizes or use clamped ranges for each breakpoint.
**Values:** Don't assume a percentage that works at 1280px works at 768px. Reassess every sized element at every breakpoint. Use fixed or clamped values instead of pure percentages for critical elements.
**Don't:** Use a single percentage across all viewports. Don't assume proportional relationships hold across screen sizes. Don't use viewport units (vw, vh) without clamping.

### Rule: Large Elements Shrink Faster

**When:** Scaling headings, hero images, margins, and padding across viewports.
**Do:** Apply a non-linear scaling ratio. Desktop headline at 48px (2.5x body at 16px) should become 28-30px on mobile (1.7x body at 16-17px), not 48px * (375/1280). Large padding (80px desktop) might become 32px mobile. Small text (14px) stays the same or even grows on mobile.
**Values:** Desktop heading ratio: 2.0-2.5x body. Mobile heading ratio: 1.5-1.7x body. Desktop padding: 48-80px sections. Mobile padding: 24-32px sections. Body text: 16px everywhere (never smaller).
**Don't:** Scale everything by the same ratio. Don't use 48px headings on mobile. Don't shrink body text below 16px on any device.

### Rule: Fluid Typography

**When:** Implementing responsive font sizes.
**Do:** Use CSS `clamp()` for smooth font scaling between breakpoints. Define a minimum size, preferred size (viewport-relative), and maximum size. This prevents text from being too small on mobile or too large on wide screens.
**Values:** Body: `clamp(1rem, 0.95rem + 0.25vw, 1.125rem)` (16-18px). H1: `clamp(1.75rem, 1.5rem + 1.5vw, 3rem)` (28-48px). H2: `clamp(1.375rem, 1.2rem + 1vw, 2.25rem)` (22-36px). Line height: 1.5 for body, 1.2 for headings.
**Don't:** Use fixed font sizes without any responsiveness. Don't use pure `vw` units for font size (too small on mobile, too large on ultrawide). Don't set body text below 16px on any viewport.

### Rule: Don't Fill the Screen

**When:** Setting content width on large viewports.
**Do:** Constrain content width. Text lines longer than 75 characters are hard to read. Set `max-width` on content containers. Allow whitespace on the sides. Center the content block.
**Values:** Text content: max-width 65-75ch (approximately 600-700px). Layout container: max-width 1280px. Full-bleed sections: background extends, content is constrained. Padding on mobile: 16-24px sides.
**Don't:** Let text span 1920px wide monitors. Don't fill the entire viewport just because you can. Don't add content to fill whitespace.

### Rule: Factor of Safety / Design Headroom

**When:** Defining layout constraints, text containers, or interactive element sizes that must accommodate variable content.
**Do:** Design with a safety factor — build in buffer for content that exceeds expected length. Size text containers for 1.5x the expected content length. Allow button labels to grow by 30-50% for internationalization. Design grids that accommodate 1 extra item beyond the expected count. Test API response displays with 2x expected data volume.
**Values:** Text container safety factor: 1.5x expected length. Button width: allow 50% growth for translation (German and Finnish labels are significantly longer than English). Card grids: test with +1 and -1 items from expected count. API response display: handle 2x expected data volume gracefully.
**Don't:** Design containers that fit content exactly at its current length — content will change. Don't hardcode widths that break with longer translations. Don't assume card counts or list lengths are fixed.

---

## Touch & Interaction

### Rule: Touch vs Pointer Targets

**When:** Designing interactive elements for multi-device use.
**Do:** Detect or design for the primary input method. Touch requires larger targets (44-48px) with more spacing (8px+ gaps). Pointer allows smaller targets (32px) with tighter spacing. Many devices support both — design for the larger input.
**Values:** Touch: 44-48px targets, 8px minimum gap. Pointer: 32px targets, 4px minimum gap. Hybrid (touch laptop): use touch targets. Hover states: provide alternatives for touch (long-press, explicit button).
**Don't:** Assume desktop = pointer and mobile = touch (Surface, iPad with keyboard). Don't rely on hover for essential information on touch devices. Don't use tiny close buttons (X) on mobile modals.

### Rule: Thumb Zone

**When:** Placing primary actions on mobile interfaces.
**Do:** Primary actions should be in the bottom third of the screen — the natural thumb zone for one-handed mobile use. Place navigation, CTAs, and frequently used actions within easy thumb reach. Content for reading can be anywhere; actions for tapping must be reachable.
**Values:** Easy reach: bottom 1/3 of screen. Stretch: middle 1/3. Hard to reach: top 1/3. Place primary actions (FAB, bottom nav, submit buttons) in the bottom 1/3. Place secondary/infrequent actions (settings, close) in the top 1/3.
**Don't:** Place primary CTAs at the top of mobile screens. Don't put the most-used actions in the hardest-to-reach areas. Don't ignore one-handed usage (80%+ of mobile usage is one-handed).

### Rule: Touch Gestures

**When:** Implementing mobile interactions beyond tapping.
**Do:** Support standard touch gestures where appropriate: (1) Swipe horizontally for carousels and navigation. (2) Pull-to-refresh for content updates. (3) Pinch-to-zoom for images and maps. (4) Long-press for context menus. Always provide a visible alternative to gesture-based actions.
**Values:** Swipe threshold: 30px minimum distance to register. Provide visual affordances: dots for carousel position, visible scroll indicators. Always include a non-gesture alternative (arrow buttons, refresh button).
**Don't:** Make gestures the only way to perform an action. Don't use custom gestures that conflict with OS gestures (edge swipe for back on iOS). Don't implement swipe-to-delete without undo.

### Rule: Never Disable Pinch-to-Zoom

**When:** Setting the viewport meta tag on any web page.
**Do:** Use the correct viewport meta tag that preserves the user's ability to zoom. Zooming is essential for users with low vision and is protected by WCAG. The only acceptable viewport content values are `width=device-width` and `initial-scale=1.0`.
**Values:** Correct: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`. Never include `maximum-scale=1.0`, `minimum-scale=1.0`, or `user-scalable=no` in the viewport meta tag.
**Don't:** Disable zoom to "fix" layout issues — fix the layout instead. Don't use `position: fixed` elements that create blind spots when content is zoomed. Don't add zoom-disabling attributes to prevent users from zooming into form fields.

---

## Navigation Patterns

### Rule: Mobile Navigation Patterns

**When:** Adapting navigation for mobile viewports.
**Do:** Use a hamburger menu or bottom tab bar for primary navigation on mobile. Hamburger: place in top-left or top-right, use standard 3-line icon. Bottom tabs: maximum 5 items, use icon + short label. Switch from horizontal desktop nav to these patterns at the tablet breakpoint (768px).
**Values:** Hamburger: at 768px breakpoint, collapse horizontal nav. Bottom tabs: 4-5 items max, icon (24px) + label (10-12px). Active state: filled icon + color change. Hamburger menu: full-screen overlay or slide-in drawer (minimum 280px wide).
**Don't:** Show a horizontal nav that wraps to multiple lines on mobile. Don't use more than 5 bottom tab items. Don't use only icons without labels in bottom tabs (recognition requires both).

---

## Posture-Based Design

Applications have different postures based on how users interact with them. Responsive design must account for this — the same content may need different density, controls, and behavior depending on whether the app is sovereign, transient, or daemonic.

**Sovereign posture** (full-screen, long-session apps like IDEs, email clients, dashboards): maximize information density, use small and efficient controls, support keyboard shortcuts extensively, minimize chrome, keep toolbars and palettes persistent. These apps should reward investment in learning with increased efficiency.

**Transient posture** (brief-interaction tools like dialogs, popovers, search bars, quick actions): make purpose immediately obvious, use large and clear controls, require zero learning, support single-action completion, auto-dismiss when done. Every additional step loses users.

**Daemonic posture** (background services, notification systems, sync engines): minimize interruptions, batch notifications, never steal focus, provide a quiet status indicator rather than active UI. These should be nearly invisible during normal operation.

Match UI density and interaction style to how long and how often users interact with each part of your application. A settings dialog within a sovereign app should still use transient posture — large controls, obvious purpose, minimal learning required.

---

## Images & Media

### Rule: Responsive Images

**When:** Displaying images across viewport sizes.
**Do:** Use `srcset` and `sizes` attributes to serve appropriately sized images. Provide 1x, 2x, and 3x versions for retina displays. Use `loading="lazy"` for below-the-fold images. Set explicit `width` and `height` to prevent layout shift.
**Values:** Image formats: WebP primary, JPEG fallback. Sizes: 640px, 1024px, 1536px, 2048px source images. Lazy loading: all images below the fold. Aspect ratio: set explicitly to prevent CLS (Cumulative Layout Shift).
**Don't:** Serve 2048px images to mobile devices. Don't omit width/height (causes layout shift). Don't lazy-load above-the-fold hero images. Don't use uncompressed images.

---

## Platform Differences

| Convention | iOS | Android | Web |
|-----------|-----|---------|-----|
| Back navigation | Swipe from left edge, top-left button | System back button/gesture | Browser back |
| Primary action | Top-right bar button | FAB (bottom-right) | Top-right or inline |
| Navigation | Bottom tab bar | Bottom nav bar or nav drawer | Top nav bar |
| Modals | Slide up from bottom | Centered dialog | Centered dialog |
| Search | Pull down to reveal | Top app bar with search icon | Search field in header |
| Delete | Swipe left to reveal | Long-press context menu | Icon button or menu |
| Scrolling | Rubber-band bounce | Edge glow | Scrollbar |
| Typography | SF Pro | Roboto | System font stack |

---

## Checklist

- [ ] Design starts at 375px and enhances upward
- [ ] Breakpoints defined: 640 / 768 / 1024 / 1280 / 1536px
- [ ] Primary CTA is in the bottom 1/3 on mobile (thumb zone)
- [ ] Touch targets are 44-48px minimum on touch devices
- [ ] Headings use non-linear scaling (2.5x desktop, 1.5-1.7x mobile)
- [ ] Body text is never smaller than 16px
- [ ] Text content has max-width of 65-75ch
- [ ] Fluid typography uses `clamp()` for smooth scaling
- [ ] Images use `srcset`, explicit dimensions, and lazy loading
- [ ] Mobile navigation uses hamburger or bottom tabs (max 5 items)
- [ ] All gesture-based actions have visible alternatives
- [ ] Content reorders by priority on mobile (CTA above fold)
- [ ] Platform conventions are respected (iOS vs Android vs Web)
- [ ] Viewport meta tag does not disable pinch-to-zoom
- [ ] Text containers sized with 1.5x safety factor for content growth
- [ ] Button labels allow 30-50% width growth for internationalization
- [ ] UI density matches application posture (sovereign / transient / daemonic)

---

# Chapter 14: Accessibility Checklist

Accessibility is not optional and not a feature. It is a baseline requirement that affects 15-20% of users directly and improves usability for everyone. Every rule in this chapter has a specific, testable criterion. Treat this as a verification checklist — if any item fails, it must be fixed before shipping.

When auditing accessibility, group issues by component pattern (e.g., "upvote button," "product card," "navigation menu") rather than by abstract WCAG principle. This allows developers to fix an entire component at once and improve the pattern library, producing more robust solutions than patchwork per-principle fixes.

**When to Use:**
- Auditing any interface before release
- Designing new components or pages
- Reviewing pull requests for accessibility regressions
- Building a design system or component library
- Responding to accessibility complaints or legal requirements

| Quick Reference | Value |
|----------------|-------|
| Normal text contrast | 4.5:1 minimum |
| Large text contrast (18px+) | 3:1 minimum |
| UI component contrast | 3:1 minimum |
| Touch target minimum | 44x44px (WCAG 2.5.5) |
| Text resize support | Usable at 200% zoom |
| Color blindness prevalence | 8% of men, 0.5% of women |
| WCAG target level | AA minimum |

---

## Document Setup

### Rule: Document Language Declaration

**When:** Creating any HTML document or embedding content in a different language.
**Do:** Always declare the language on the `<html>` element using the `lang` attribute. Use `lang` on child elements when switching languages inline. This enables correct screen reader pronunciation, proper spell-checking, accurate translation services, and correct font rendering for international character sets.
**Values:** `<html lang="en">` for English. Use BCP 47 language tags. For inline language switches: `<span lang="fr">Bonjour</span>`. For CJK content: `lang="zh-Hans"` triggers simplified Chinese font rendering. For quotations in other languages: `<blockquote lang="fr">`.
**Don't:** Omit the `lang` attribute — screen readers will use the wrong voice profile and mispronounce content. Don't set the wrong language code — a French text read by an English voice profile is unintelligible.

### Rule: Visually Hidden Class for Screen-Reader-Only Content

**When:** Providing information that is visually apparent from context but needs a screen reader equivalent — icon-only buttons, visual status indicators, layout-implied relationships.
**Do:** Include a `.visually-hidden` utility class in every project. Use it to provide screen-reader-only text for context that is visually communicated through layout, icons, or styling. This class keeps elements in the accessibility tree while hiding them visually.
**Values:** `.visually-hidden { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(1px, 1px, 1px, 1px); }`. Never use `display: none` or `visibility: hidden` for screen-reader content — these hide from assistive technology too.
**Don't:** Use `display: none` or `height: 0` or `width: 0` when you want content to remain accessible to screen readers. Don't overuse — only add when visual context is unclear non-visually.

---

## Color & Contrast

### Rule: Text Contrast Ratios

**When:** Choosing text colors against any background.
**Do:** Meet minimum contrast ratios per WCAG 2.1 AA. Measure with a contrast checker tool. Test against the actual background color, not an approximation. Include states (hover, focus, disabled) in testing.
**Values:** Normal text (< 18px / < 14px bold): 4.5:1 contrast ratio. Large text (>= 18px / >= 14px bold): 3:1 contrast ratio. Disabled text: exempt from contrast requirements but must be distinguishable from enabled text.
**Don't:** Use light gray text on white backgrounds (#999 on #fff = 2.85:1, fails). Don't measure contrast against transparent backgrounds without checking the actual rendered color. Don't exempt placeholder text from contrast requirements.

### Rule: UI Component Contrast

**When:** Designing borders, icons, focus indicators, form controls, and other non-text UI elements.
**Do:** All meaningful UI components and graphical objects must have 3:1 contrast against adjacent colors. This includes: input borders, icon buttons, chart elements, toggle states, focus rings, and custom checkboxes/radios.
**Values:** UI component contrast: 3:1 minimum against adjacent background. Focus indicator contrast: 3:1 against both the focused element and the surrounding background. State changes (on/off, selected/unselected): 3:1 between states.
**Don't:** Use thin, low-contrast borders for form inputs. Don't rely on subtle color changes for state indication. Don't use icons without sufficient contrast against their background.

### Rule: Don't Rely on Color Alone

**When:** Communicating status, errors, required fields, categories, or any information through color.
**Do:** Always pair color with a secondary indicator: icon, text label, pattern, or shape. Error states: red color + error icon + text message. Required fields: asterisk or "(required)" text, not just red label. Status: colored dot + text label ("Active", "Pending").
**Values:** Color + text label for all status indicators. Color + icon for all feedback (success checkmark, error X, warning triangle). Color + pattern for charts and data visualization.
**Don't:** Use only red/green to indicate error/success. Don't use color as the sole differentiator in charts or graphs. Don't mark required fields only with a red asterisk.

### Rule: Color Blindness Testing

**When:** Finalizing any color palette or visual design.
**Do:** Test designs with color blindness simulators. 8% of men and 0.5% of women have some form of color vision deficiency. Test against the three most common types: deuteranopia (red-green, most common), protanopia (red-green), and tritanopia (blue-yellow).
**Values:** Test with: deuteranopia, protanopia, tritanopia simulators. Tool: browser DevTools > Rendering > Emulate vision deficiencies. All information must be distinguishable under all three simulations.
**Don't:** Use red/green as opposing indicators without additional differentiation. Don't use pastel colors that become indistinguishable under simulation. Don't assume "most users can see color" — 1 in 12 men cannot.

---

## Keyboard Navigation

### Rule: All Interactive Elements Must Be Focusable

**When:** Building any interactive component — buttons, links, inputs, menus, modals, custom widgets.
**Do:** Every element that responds to click or tap must also be reachable and operable via keyboard. Use semantic HTML (`<button>`, `<a>`, `<input>`) which provides keyboard support automatically. For custom elements, add `tabindex="0"`, `role`, and keyboard event handlers.
**Values:** Focusable: all buttons, links, form controls, menu items, tabs, custom interactive widgets. Not focusable: decorative elements, disabled controls (use `tabindex="-1"`). Keyboard operations: Enter/Space to activate, Arrow keys for menu/tab navigation, Escape to close.
**Don't:** Use `<div>` or `<span>` as interactive elements without proper role and keyboard handling. Don't trap keyboard focus (user must be able to tab away). Don't use `tabindex` values greater than 0 (disrupts natural tab order).

### Rule: Visible Focus States

**When:** Styling focus indicators for any interactive element.
**Do:** Provide a highly visible focus indicator that is distinct from hover state. Use a 2-3px solid outline with 3:1 contrast against the background. Never remove the focus outline without providing an alternative.
**Values:** Focus ring: 2-3px solid, offset 2px from element. Contrast: 3:1 against surrounding background. Color: blue (#0066CC) or high-contrast color appropriate to your palette. Apply to: all interactive elements.
**Don't:** Set `outline: none` without a replacement focus style. Don't use only color change as a focus indicator. Don't make focus indicators too subtle (1px dotted light gray fails). Don't remove focus styles "because they look ugly" — make them look good instead.

### Rule: Focus Styles Must Use Background Color

**When:** Choosing how to implement focus indicators, especially for links and inline interactive elements.
**Do:** Replace browser default focus outlines (thin dotted lines) with a solid `background-color` highlight that creates a clearly visible filled box. This is significantly more visible than thin outlines, especially for users with low vision. The GOV.UK design system uses this pattern to great effect.
**Values:** `a:focus { outline: none; background-color: #cef; }` (or your brand's highlight color). Minimum focus indicator area: 2px solid outline or full background-color fill. The focused element must have at least 3:1 contrast ratio against adjacent non-focused elements.
**Don't:** Use thin dotted outlines as the sole focus indicator — they are too subtle for many users. Don't just remove focus outlines with `outline: none` without providing a replacement. Don't use a focus style that only changes the text color.

### Rule: Logical Focus Order

**When:** Laying out page content and interactive elements.
**Do:** Tab order must match the visual layout. Users pressing Tab should move through the page in a logical sequence: top-to-bottom, left-to-right (in LTR languages). Do not use `tabindex` values > 0 to override natural order — instead, fix the DOM order.
**Values:** Focus order: matches visual reading order. Test: Tab through entire page, verify sequence makes sense. Modals: focus trapped within modal, returns to trigger on close. Skip links: "Skip to main content" as first focusable element.
**Don't:** Use CSS to visually reorder elements while leaving DOM order mismatched. Don't let focus jump unpredictably across the page. Don't leave focus on a hidden or removed element.

### Rule: Focus Management After Dynamic Content Load

**When:** Loading new content dynamically via AJAX, "Load more" buttons, filters, or any action that adds content to the page without a full page reload.
**Do:** After new content loads, move keyboard focus to the first element of the newly loaded content. Use `tabindex="-1"` on the target element (such as the first heading) to make it programmatically focusable without adding it to the permanent tab order. Call `element.focus()` after the content renders. Replace infinite scroll with an explicit "Load more" button so keyboard and screen reader users maintain control.
**Values:** Focus target: first heading (`<h2>` or `<h3>`) of new content with `tabindex="-1"`. Call `element.focus()` after content renders. Always use explicit "Load more" buttons instead of infinite scroll.
**Don't:** Leave focus on the "Load more" button after new content pushes it off-screen. Don't let focus reset to `<body>` — this causes keyboard users to lose their place entirely. Don't use positive `tabindex` values. Don't use infinite scroll as the default pagination pattern.

---

## Screen Reader Support

### Rule: Semantic HTML First

**When:** Building any page structure or component.
**Do:** Use semantic HTML elements as the foundation: `<nav>`, `<main>`, `<article>`, `<aside>`, `<header>`, `<footer>`, `<section>`, `<h1>`-`<h6>`, `<button>`, `<a>`, `<table>`, `<form>`, `<label>`, `<fieldset>`, `<legend>`. Semantic HTML provides built-in accessibility that ARIA cannot replicate.
**Values:** Use semantic elements for: navigation (`<nav>`), main content (`<main>`), headings (`<h1>`-`<h6>`), buttons (`<button>`), links (`<a href>`), tables (`<table>` with `<th>`), forms (`<form>` with `<label>`).
**Don't:** Build everything with `<div>` and `<span>`. Don't use ARIA roles as a substitute for semantic HTML. Don't use `<a>` for buttons or `<button>` for navigation links.

### Rule: Alt Text for Images

**When:** Including any image in the interface.
**Do:** Provide `alt` text that describes the image's purpose, not its appearance. Functional images (icons, buttons): describe the action ("Search", "Close menu"). Informative images: describe the content ("Bar chart showing 40% growth in Q3"). Decorative images: use `alt=""` (empty string, not omitted).
**Values:** Alt text length: 1-2 sentences maximum (125 characters for most screen readers). Functional images: describe action, not image. Informative images: describe meaning. Decorative: `alt=""`.
**Don't:** Use "Image of..." or "Photo of..." prefixes (screen readers already announce "image"). Don't leave `alt` attribute missing entirely. Don't use filenames as alt text. Don't describe decorative images.

### Rule: ARIA Labels for Custom Components

**When:** Building custom interactive components that lack semantic HTML equivalents.
**Do:** Add `aria-label` or `aria-labelledby` to elements that have no visible text label. Icon buttons need `aria-label="Close"`. Custom dropdowns need `role="listbox"` with `aria-expanded`. Loading states need `aria-live="polite"` regions.
**Values:** Icon buttons: `aria-label` with action name. Custom menus: `role="menu"` + `aria-expanded` + `aria-haspopup`. Live regions: `aria-live="polite"` for non-urgent updates, `aria-live="assertive"` for errors. Modals: `role="dialog"` + `aria-modal="true"` + `aria-labelledby`.
**Don't:** Add ARIA to elements that already have proper semantics (a `<button>` doesn't need `role="button"`). Don't use `aria-label` on elements that have visible text (use `aria-labelledby`). Don't forget to update `aria-expanded` when menus toggle.

### Rule: Toggle Buttons with aria-pressed

**When:** Building a button that toggles between on/off states — like/unlike, mute/unmute, dark mode toggle, bookmark, follow/unfollow.
**Do:** Use a `<button>` element with `aria-pressed="true"` or `aria-pressed="false"` to communicate toggle state to assistive technology. Toggle the attribute value on click. Style the pressed state using the `[aria-pressed="true"]` CSS attribute selector so visual state and accessible state stay in sync.
**Values:** Initial state: `aria-pressed="false"`. Screen reader announcement: "Button name, toggle button, not pressed" / "pressed". Click handler: toggle between `"true"` and `"false"` string values. Using `<button>` provides Enter and Space keyboard activation for free.
**Don't:** Use checkboxes for toggle actions that are not form fields. Don't use two separate on/off buttons when a single toggle button suffices. Don't change the button label between states (keep the label constant, let `aria-pressed` communicate the state).

---

## Heading Hierarchy

### Rule: Heading Levels Must Not Skip

**When:** Structuring any page content.
**Do:** Use heading levels sequentially: `<h1>` followed by `<h2>`, then `<h3>`. Never skip from `<h1>` to `<h3>`. Each page should have exactly one `<h1>`. Headings create the document outline that screen reader users navigate by.
**Values:** One `<h1>` per page (the page title). `<h2>` for major sections. `<h3>` for subsections within `<h2>`. Never skip levels. Heading count: screen reader users scan headings first — ensure all major content has a heading.
**Don't:** Skip from `<h1>` to `<h3>`. Don't use headings for visual styling (use CSS instead). Don't have multiple `<h1>` elements. Don't use bold text instead of proper heading elements.

### Rule: Descriptive Link Text

**When:** Writing any hyperlink or interactive text.
**Do:** Link text must describe the destination or action out of context. Screen reader users navigate by links list — each link must make sense independently. Use "View pricing details" not "Click here." Use "Download 2024 annual report" not "Download."
**Values:** Link text: 2-6 words describing the destination. Unique: no two links on the same page should have identical text unless they go to the same destination. Action links: start with a verb ("View", "Download", "Open").
**Don't:** Use "Click here", "Read more", "Learn more" as link text. Don't use the URL as link text. Don't use identical "Read more" links for different articles.

### Rule: External Link Indicators via CSS

**When:** Displaying inline links that navigate to external domains.
**Do:** Automatically identify and mark external links using CSS attribute selectors. Add a visual icon and screen-reader-accessible text via `::after` pseudo-content. This requires no editorial effort — the CSS handles detection automatically.
**Values:** Selector: `[href^="http"]:not([href*="yourdomain.com"])::after`. Icon: `display: inline-block; width: 1em; height: 1em;` with SVG background-image of an external link icon. Screen reader text: use `.visually-hidden` text within the `::after` content reading "(external link)". Size the icon in `em` units so it scales with surrounding text.
**Don't:** Require editors to manually add classes or icons to external links — automate it. Don't use `target="_blank"` without warning users that the link opens in a new window. Don't omit the screen-reader-accessible label for the external icon.

---

## Motion & Animation

### Rule: Respect prefers-reduced-motion

**When:** Implementing any animation, transition, or motion effect.
**Do:** Check the `prefers-reduced-motion` media query and provide reduced or eliminated motion for users who request it. Essential motion (progress bars, loading spinners) can be simplified but not removed. Decorative motion (parallax, entrance animations) should be removed entirely.
**Values:** Query: `@media (prefers-reduced-motion: reduce)`. Essential motion: simplify to opacity changes or static states. Decorative motion: remove completely. Transition duration with reduced motion: 0ms or instant.
**Don't:** Ignore `prefers-reduced-motion`. Don't auto-play video backgrounds without a pause control. Don't use flashing or strobing effects (seizure risk — never more than 3 flashes per second). Don't lock content behind animation completion.

### Rule: Provide Pause Controls

**When:** Any content auto-plays, auto-scrolls, or auto-advances (carousels, videos, tickers, animations).
**Do:** Provide visible pause/stop controls. Auto-playing content that lasts more than 5 seconds must have a mechanism to pause, stop, or hide it. Users with attention or cognitive disabilities need control over moving content.
**Values:** Pause button: visible and accessible on all auto-playing content. Auto-play duration before requiring user interaction: 5 seconds maximum per WCAG. Video: paused by default or with visible controls. Carousels: pause on hover/focus, visible play/pause.
**Don't:** Auto-play videos with sound. Don't auto-advance carousels without pause capability. Don't make pause controls disappear on hover. Don't auto-play content indefinitely.

### Rule: No Autoplay Audio

**When:** Designing audio feedback, video, or sound-enabled interfaces.
**Do:** Never autoplay audio. Sudden sounds trigger startle reflex and negative association. All audio must be user-initiated.
**Values:** Default all audio muted. Video: autoplay muted with captions. System sounds: soft, brief (<500ms). Always provide mute/volume control.
**Don't:** Autoplay audio on page load. Don't use sounds without visual equivalent.

---

## Text & Zoom

### Rule: Content Must Be Usable at 200% Zoom

**When:** Building any web interface.
**Do:** Test the entire interface at 200% browser zoom. No content should be cut off, overlapped, or require horizontal scrolling. Use relative units (`rem`, `em`, `%`) for font sizes, padding, and margins. Text must reflow within the viewport.
**Values:** Test at: 100%, 150%, 200% zoom. No horizontal scroll at 200% on a 1280px viewport. No text truncation without a mechanism to access full text. No overlapping elements.
**Don't:** Use fixed pixel values for container widths that prevent reflow. Don't hide overflow without providing an alternative. Don't use viewport-relative text sizes that don't respond to browser zoom.

### Rule: Skip Navigation Link

**When:** Building any multi-page website.
**Do:** Provide a "Skip to main content" link as the first focusable element on every page. It should be visually hidden by default but visible on focus. This allows keyboard users to bypass repeated navigation.
**Values:** Position: first focusable element. Visibility: hidden until focused (`position: absolute` + visible on `:focus`). Target: links to `<main>` or `id="main-content"`. Text: "Skip to main content."
**Don't:** Omit skip links on content-heavy pages. Don't make skip links permanently hidden (they must appear on focus). Don't link to an incorrect target.

---

## Video & Media Accessibility

### Rule: Accessible Video with Captions and Transcript

**When:** Embedding video content in any interface.
**Do:** Provide three accessibility layers for every video: (1) A keyboard-accessible player with visible focus styles on all controls. (2) Closed captions that identify speakers and describe sound effects. (3) A full text transcript placed below the video. Captions must identify speaker changes and relevant non-speech audio.
**Values:** Caption format: `SPEAKER: "Dialog text"`. Sound effects: `[GLASS BREAKING]`. Off-screen speakers: `SPEAKER (off screen):`. Recommended accessible players: YouTube embed, Able Player, PayPal's accessible HTML5 player. Transcript should be a full-text version of the video content, not just a caption dump.
**Don't:** Use video players that are not keyboard-navigable — test by pressing Tab into the player and using Space/Enter to play/pause. Don't provide captions without also providing a transcript — captions only work when the video loads and plays. Don't auto-generate captions without human review.

---

## Form Accessibility

### Rule: Labels Linked to Inputs

**When:** Building any form field.
**Do:** Every input must have a programmatically associated label using the `for` attribute matching the input's `id`. This ensures screen readers announce the label when the input is focused and increases the click target (clicking the label focuses the input).
**Values:** Every `<input>`, `<select>`, and `<textarea>` has a `<label>` with matching `for`/`id`. Grouped inputs (radio buttons, checkboxes) use `<fieldset>` + `<legend>`. Error messages linked via `aria-describedby`.
**Don't:** Use placeholder text as the only label. Don't position labels far from their inputs. Don't use implicit label association (`<label><input></label>`) without also using `for`/`id` (less reliable across assistive tech).

### Rule: Error Announcements

**When:** Displaying form validation errors.
**Do:** Announce errors to screen readers using `aria-live="assertive"` or by moving focus to the error summary. Link error messages to their fields using `aria-describedby`. Provide an error summary at the top of the form listing all errors with links to the offending fields.
**Values:** Error summary: at top of form, announced via `aria-live` or focused. Individual errors: linked to field via `aria-describedby`. Error icon: include `aria-hidden="true"` if decorative (text conveys meaning). Focus: move to first error field or error summary on submission.
**Don't:** Show errors only visually without screen reader announcement. Don't use color alone to indicate errors. Don't show errors that disappear before users can read them.

---

## Accessibility Auditing

### Rule: Evaluate Accessibility by Pattern, Not by Principle

**When:** Auditing or fixing accessibility issues in an interface.
**Do:** Group accessibility issues by component or pattern (e.g., "upvote button," "product card," "navigation menu") rather than by WCAG principle (perceivable, operable, understandable, robust). This allows developers to fix an entire component at once and improve the pattern library, resulting in fewer tickets, more robust solutions, and reusable exemplars for the design system.
**Values:** Instead of 3 separate tickets ("button missing label," "button not keyboard-accessible," "button has wrong role"), create 1 ticket: "Replace `<div>` upvote button with semantic `<button>` using SVG icon and `aria-label`." Pattern-based fixes produce cleaner components than principle-based patchwork (e.g., a proper `<button>` instead of a `<div>` with `role="button"`, `tabindex="0"`, and `aria-label` bolted on).
**Don't:** Create per-principle accessibility tickets that different developers fix independently — this leads to bloated, over-patched components. Don't audit only against WCAG success criteria in isolation — always check how the full component works together.

---

## Verification Checklist

Test each criterion. Mark Pass, Fail, or N/A.

### Perceivable
- [ ] Text contrast >= 4.5:1 (normal) / 3:1 (large 18px+) — **Tool:** browser DevTools or axe
- [ ] UI component contrast >= 3:1 — **Tool:** contrast checker against adjacent colors
- [ ] No information conveyed by color alone — **Test:** grayscale screenshot still understandable
- [ ] All images have appropriate `alt` text — **Tool:** axe, WAVE, or manual check
- [ ] Color blindness simulation passes — **Tool:** DevTools > Rendering > Emulate vision deficiencies
- [ ] Video/audio has captions, transcript, and keyboard-accessible player
- [ ] Document language declared with `lang` attribute on `<html>`
- [ ] External links marked with visual indicator and screen-reader text

### Operable
- [ ] All interactive elements keyboard accessible — **Test:** unplug mouse, navigate with Tab/Enter/Space/Arrows
- [ ] Visible focus indicator on all interactive elements — **Test:** Tab through page, verify visible highlight (background-color preferred over thin outline)
- [ ] Focus order matches visual layout — **Test:** Tab through, verify logical sequence
- [ ] Focus managed correctly after dynamic content loads — **Test:** trigger "Load more", verify focus moves to new content
- [ ] Skip navigation link present and functional — **Test:** Tab on first load, verify "Skip to main content" appears
- [ ] Touch targets >= 44x44px — **Tool:** measure in DevTools
- [ ] No keyboard traps — **Test:** Tab into and out of every component (modals, menus, widgets)
- [ ] `prefers-reduced-motion` respected — **Test:** enable in OS settings, verify motion removed
- [ ] Auto-playing content has pause control
- [ ] No autoplay audio — all audio user-initiated
- [ ] Pinch-to-zoom not disabled — **Test:** check viewport meta tag for `user-scalable=no` or `maximum-scale`

### Understandable
- [ ] Heading hierarchy is sequential (h1 > h2 > h3, no skips) — **Tool:** HeadingsMap extension
- [ ] Link text is descriptive out of context — **Test:** read all links without surrounding text
- [ ] Form labels linked to inputs via `for`/`id` — **Tool:** axe or click label to verify focus
- [ ] Error messages: identify problem, explain, suggest fix — **Test:** trigger errors, read messages
- [ ] Error announcements reach screen readers — **Tool:** VoiceOver / NVDA / JAWS
- [ ] Language attribute set on `<html>` element
- [ ] Toggle buttons use `aria-pressed` for state — **Test:** inspect toggle components

### Robust
- [ ] Valid HTML (no duplicate IDs, proper nesting) — **Tool:** W3C validator
- [ ] ARIA used correctly (roles, states, properties) — **Tool:** axe accessibility checker
- [ ] Content usable at 200% browser zoom — **Test:** Cmd/Ctrl + zoom to 200%, check for overflow
- [ ] No horizontal scroll at 200% zoom on 1280px viewport
- [ ] Works with screen reader — **Tool:** VoiceOver (Mac), NVDA (Windows), TalkBack (Android)
- [ ] `.visually-hidden` class available and used for screen-reader-only content

### Testing Tools Quick Reference
| Tool | What It Tests | How to Access |
|------|--------------|---------------|
| axe DevTools | Automated WCAG violations | Browser extension |
| WAVE | Visual accessibility overlay | Browser extension |
| Lighthouse | Accessibility score + issues | Chrome DevTools > Lighthouse |
| HeadingsMap | Heading hierarchy | Browser extension |
| Color Contrast Analyzer | Contrast ratios | Desktop app (TPGi) |
| VoiceOver | Screen reader testing | Built into macOS (Cmd+F5) |
| NVDA | Screen reader testing | Free download (Windows) |

---

---

---

# Chapter 15: Anti-Pattern Catalog

Common UI/UX mistakes organized by domain. Each anti-pattern includes what's wrong, why it fails, and the correct approach. Use this chapter as a review checklist before shipping any interface.

**When to Use:**
- Reviewing designs before launch
- Auditing existing interfaces for problems
- Training designers and agents on what to avoid
- Post-mortem analysis of usability issues

---

## Visual Design Anti-Patterns

### Anti-Pattern: Equal Visual Weight

**Wrong:** Every element has the same size, color, and weight. Headlines, body text, labels, and metadata all compete for attention equally.
**Why it fails:** Without hierarchy, users can't scan. Nothing stands out, so everything is noise. Users feel overwhelmed and bounce.
**Correct:** Assign 3 levels of importance. Primary (dark, large, bold), secondary (grey, medium), tertiary (light, small). Use font weight (400 vs 600), color contrast, and size differences that are clearly distinct at each level.

### Anti-Pattern: Grey Text on Colored Backgrounds

**Wrong:** Using literal grey (`#666`) on a colored (e.g., blue) background to de-emphasize text.
**Why it fails:** Grey on color creates muddy, unreadable text. The goal is reduced contrast, not literally grey text.
**Correct:** Hand-pick a color based on the background: same hue, adjusted saturation and lightness. On a blue background, use a lighter or darker blue — not grey.

### Anti-Pattern: Scaling Up Small Icons

**Wrong:** Taking a 16-24px icon and scaling it to 64px or larger for hero sections.
**Why it fails:** Small icons are designed with minimal detail. At 3-4x size, they look chunky, pixelated, and unprofessional.
**Correct:** Enclose the small icon in a larger shaped container (circle or rounded square) with a background color. Or use an icon set designed for the target size.

### Anti-Pattern: True Black (#000000) and Pure White (#FFFFFF)

**Wrong:** Using pure black for text or pure white for backgrounds.
**Why it fails:** True black looks unnatural and creates harsh contrast. Pure white backgrounds cause glare. Users with scotopic sensitivity (Irlen syndrome) experience text blur or movement with maximum contrast.
**Correct:** Use near-black (`#222` to `#333`) on near-white (`#f5f5f5` to `#eee`). This still passes WCAG AAA (7:1+) while reducing visual strain.

### Anti-Pattern: False Affordances

**Wrong:** Elements that look interactive but aren't (underlined non-link text, raised card that doesn't click, colored text that isn't a link).
**Why it fails:** Users click and nothing happens, eroding trust. Every false affordance teaches users to distrust real interactive elements.
**Correct:** Every element with a signifier of interactivity (underline, hover effect, raised appearance, pointer cursor) must be interactive. If it looks clickable, it must be clickable.

### Anti-Pattern: Misaligned Asymmetric Elements

**Wrong:** Using software center-alignment for asymmetric elements like icons, pull quotes, or numbered lists.
**Why it fails:** Geometric centering ignores visual weight. The element looks off-center because the human eye perceives visual mass, not bounding boxes.
**Correct:** Align by visual weight/area. Hang pull quote marks outside the text margin. Align numbered lists on the text start, not the numbers. Center asymmetric icons on their visual mass, not bounding box.

---

## Typography Anti-Patterns

### Anti-Pattern: Size-Only Hierarchy

**Wrong:** Differentiating headings from body text solely by making them bigger (e.g., 36px heading, 16px body, nothing else changes).
**Why it fails:** Leads to oversized headings and undersized body text. The primary text ends up too large, and the secondary too small for comfort.
**Correct:** Combine size with weight (600-700 for headings, 400 for body) and color (darker for headings, grey for secondary text). A 24px bold dark heading with 16px regular grey body is clearer than a 36px vs 12px size-only split.

### Anti-Pattern: Using em Units for Font Size

**Wrong:** Setting font sizes in `em` units throughout nested components.
**Why it fails:** `em` compounds relative to parent. A `0.9em` inside another `0.9em` computes to `0.81em`, drifting from your type scale without warning.
**Correct:** Use `px` or `rem` for font sizes. Both reference a fixed base and don't compound.

### Anti-Pattern: Walls of Text Without Visual Entry Points

**Wrong:** Long paragraphs with uniform styling — no headings, no bold, no bullets, no whitespace variation.
**Why it fails:** Users scan, reading only 20-28% of words. Without visual entry points, they skip the entire block.
**Correct:** Break text into short paragraphs (3-4 lines). Bold key phrases. Use headings every 2-3 paragraphs. Use bullet lists for 3+ related items. Place the most important information in the first two words of each line.

### Anti-Pattern: Pixel Root Font Size

**Wrong:** Setting `html { font-size: 16px }` or any pixel value as the root font size.
**Why it fails:** Overrides user-configured font sizes set in browser preferences. Users with low vision who set larger defaults get ignored.
**Correct:** Set `html { font-size: 100% }` to respect user preferences. Use `rem` for all sizes so everything scales proportionately.

### Anti-Pattern: Render-Blocking Web Fonts

**Wrong:** Loading web fonts synchronously so text is invisible (FOIT) until fonts download.
**Why it fails:** Users on slow connections see no text at all for seconds. Content is completely inaccessible during the flash of invisible text.
**Correct:** Load fonts asynchronously. Choose system font fallbacks with similar metrics. Subset to needed characters. Maximum web font budget: 100-150KB.

### Anti-Pattern: Removing Underlines from Inline Links

**Wrong:** Using `text-decoration: none` on inline links within paragraph text, relying on color alone.
**Why it fails:** Color-blind users (8% of men) cannot distinguish links from surrounding text. The universal affordance for clickable text within a paragraph is the underline.
**Correct:** Keep underlines on inline links. CTA buttons styled as buttons are exempt. For improved aesthetics, use CSS gradient-based underlines that avoid crossing descenders.

---

## Color Anti-Patterns

### Anti-Pattern: 5-Color Palette Generator

**Wrong:** Starting with a palette generator that produces 5 colors and attempting to build a complete UI from them.
**Why it fails:** Real interfaces need 8-10 grey shades, 5-10 shades per primary color, and accent colors for semantic states (error, warning, success). Five colors are wildly insufficient.
**Correct:** Build three palette categories: greys (8-10 shades), primary (5-10 shades per color), supporting/accent (5-10 shades each for red, yellow, green at minimum). Pre-define a 9-shade scale (100-900) per color.

### Anti-Pattern: Color-Only Meaning

**Wrong:** Using red vs. green as the only indicator of status (error vs. success, down vs. up).
**Why it fails:** 8% of men and 0.5% of women have color vision deficiency. Red-green is the most common type. Relying on color alone makes the interface unusable for ~1 in 12 male users.
**Correct:** Always pair color with a secondary indicator: icon (checkmark/X), text label, pattern, or shape difference. Use contrast (light vs. dark) in addition to hue for colorblind accessibility.

### Anti-Pattern: Picking Colors on Neutral Canvas

**Wrong:** Choosing colors from a swatch palette without placing them on the actual design background.
**Why it fails:** Perceptual constancy causes colors to appear different on different backgrounds. The same grey looks darker on white, lighter on black. Colors shift warm/cool depending on surrounding hues.
**Correct:** Always test colors against their actual backgrounds. Verify contrast ratios in context. Adjust hue and saturation separately for light mode and dark mode.

---

## Layout & Spacing Anti-Patterns

### Anti-Pattern: Filling the Entire Screen

**Wrong:** Stretching content to fill a wide desktop viewport — making sidebars, text blocks, and images as wide as the browser.
**Why it fails:** Content has an optimal width. Text becomes unreadable past 75 characters per line. Stretched UI elements look sparse and disconnected.
**Correct:** Give elements their natural width. Use `max-width` on content containers. Start with 400px (mobile-width) and scale up. Split narrow content into columns rather than stretching it.

### Anti-Pattern: Ambiguous Spacing

**Wrong:** Equal spacing above and below labels, headings, or group separators.
**Why it fails:** When a label has the same distance to the element above and below it, it's unclear which element it belongs to. Users lose the spatial relationship between label and content.
**Correct:** Place labels closer to their associated content than to adjacent elements. Use the rule: space within a group < space between groups. If a label sits between two fields, it should be 2-3x closer to the field it describes.

### Anti-Pattern: Border Overload

**Wrong:** Using borders to separate every section, card, list item, and nav element.
**Why it fails:** Excessive borders create visual clutter and make the design feel busy, heavy, and dated.
**Correct:** Replace borders with: (1) Different background colors for adjacent sections, (2) Box shadows for card outlines, (3) Extra whitespace between groups. Reserve borders for tables and form inputs where they serve a functional purpose.

---

## Navigation & IA Anti-Patterns

### Anti-Pattern: "Click Here" Links

**Wrong:** Link text that says "Click here", "Learn more", "Read more" without context.
**Why it fails:** Users scan links. "Click here" provides zero information about the destination. Screen readers read links out of context, making "click here" useless for accessibility.
**Correct:** Use descriptive link text that predicts the destination: "View pricing plans", "Read the API documentation", "Download the report". Link text should make sense without surrounding context.

### Anti-Pattern: Hiding Search on Content-Heavy Sites

**Wrong:** Putting search behind a magnifying glass icon on sites with 100+ pages of content.
**Why it fails:** Many users are "search-dominant" — they go straight to search rather than browsing navigation. Hiding it adds a step for your most goal-oriented users.
**Correct:** Show a visible search input field on every page. Minimum 27 characters wide. Place consistently in the header.

### Anti-Pattern: Icon-Only Hamburger Menu

**Wrong:** Using a three-line icon alone as the menu toggle button, without text label or button border.
**Why it fails:** Research shows icon-only hamburger buttons are significantly less understood than labeled ones. Users don't recognize the icon reliably, especially older or non-technical audiences.
**Correct:** Combine three-line icon + text "Menu" + visible button border. Use `<button>` element with `aria-expanded`. If the menu has fewer than 5 items, don't hide it at all.

### Anti-Pattern: Navigation Without List Markup

**Wrong:** Building navigation with bare `<a>` tags or `<div>`-based layouts without semantic list structure.
**Why it fails:** Screen readers can't communicate count ("3 of 5 items") or grouping. Without CSS, nav becomes an unparseable string of links.
**Correct:** Always use `<nav><ul><li><a>` structure. Label multiple `<nav>` elements with `aria-labelledby` or `aria-label` to distinguish them.

### Anti-Pattern: Back-Button-Dependent Navigation

**Wrong:** Designing page flows that require users to hit the browser back button to navigate between siblings or continue a task.
**Why it fails:** Users don't go backward. Every back-button press increases abandonment probability. Each page should provide clear forward navigation options.
**Correct:** Design forward-only loops. Every page answers "What do I do next?" with visible forward options. If >15% of users hit back in testing, the page is failing.

---

## Behavioral Design Anti-Patterns

### Anti-Pattern: Fake Scarcity

**Wrong:** Countdown timers that reset on page reload. "Only 2 left!" indicators that never change. "Limited time offer" that runs permanently.
**Why it fails:** Users notice. A single discovery of fake scarcity destroys all trust signals on the site. Word spreads through reviews and social media.
**Correct:** Only display scarcity signals backed by real data. If stock is limited, show real inventory counts that actually decrease. If a deadline is real, let it expire. If the offer is always available, don't pretend otherwise.

### Anti-Pattern: Confirm-Shaming

**Wrong:** Opt-out copy that shames users: "No thanks, I don't want to save money" or "I prefer to stay uninformed."
**Why it fails:** Users feel manipulated, not persuaded. It creates negative brand association and social media backlash. It technically works in the short term but destroys long-term trust and brand sentiment.
**Correct:** Use neutral opt-out language: "No thanks" or "Maybe later". Respect the user's decision. Focus on making the offer genuinely valuable rather than guilting users into accepting.

### Anti-Pattern: Dark Pattern Roach Motel

**Wrong:** Making sign-up a 1-click process but cancellation requires calling a phone number, waiting on hold, or navigating a 7-step maze.
**Why it fails:** Users feel trapped. Regulatory bodies (FTC, EU) are increasingly penalizing this pattern. Retained users who wanted to leave generate negative reviews and support costs.
**Correct:** Make cancellation as easy as sign-up. One-click cancel with optional "tell us why" survey. Offer a pause option instead of cancellation. Win retention through value, not friction.

### Anti-Pattern: Notification Fatigue

**Wrong:** Sending push notifications, emails, and in-app alerts for every possible event, especially within the first 24 hours.
**Why it fails:** Users disable all notifications or uninstall. The notification channel — your most valuable owned trigger — is permanently destroyed. Once a user turns off notifications, they rarely turn them back on.
**Correct:** Start with minimal notifications (only high-value, user-initiated triggers). Let users choose notification types. Respect frequency: max 1 push per day for most apps. Save notifications for moments when the user would genuinely want to know.

### Anti-Pattern: Lowball Bait

**Wrong:** Getting users committed to a price/feature set, then changing terms after commitment (showing features in trial that disappear in paid tier, advertising a price excluding mandatory fees).
**Why it fails:** Distinct from bait-and-switch — user has already committed before the switch. Destroys trust permanently. Users who feel deceived after commitment become vocal detractors.
**Correct:** Honor all stated terms. If pricing changes, grandfather existing commitments.

### Anti-Pattern: Invisible State Changes

**Wrong:** Silently updating content without visual indication (dashboards, live data, notifications).
**Why it fails:** Change blindness — users fail to notice even large changes during visual interruptions. They make decisions based on stale data they believe is current.
**Correct:** Animate changes, flash updated cells, show "2 new" badges, toast for off-screen updates.

### Anti-Pattern: Confirmation Dialog as Safety Net

**Wrong:** Using "Are you sure?" confirmation dialogs as the primary protection against user errors.
**Why it fails:** Users learn to click "OK" reflexively (confirmation fatigue). The dialog becomes invisible within a few encounters. It interrupts flow without actually preventing errors.
**Correct:** Prefer undo over confirmation. Show a brief delay window ("Sending in 5 seconds... [Cancel]") for irreversible actions. Support multi-level undo with visible history. Reserve confirmation for truly irreversible, high-severity actions only.

---

## Form Design Anti-Patterns

### Anti-Pattern: Multi-Column Forms

**Wrong:** Placing form fields side by side (first name / last name in two columns, or worse, mixing column layouts throughout a form).
**Why it fails:** Users' eyes have to zigzag. Completion rate drops. The visual flow breaks. On mobile, side-by-side fields are too narrow.
**Correct:** One column for all form fields. The only exception: closely related short fields (first name + last name, city + state + zip). Even then, they must share a single visual row.

### Anti-Pattern: Validate on Keystroke

**Wrong:** Showing validation errors while the user is still typing (e.g., "Invalid email" appears after typing "j").
**Why it fails:** The user hasn't finished the input yet. Premature validation is distracting, anxiety-inducing, and makes the interface feel combative.
**Correct:** Validate on blur (when the user leaves the field). Exception: show positive confirmation as-you-type for password strength meters and username availability.

### Anti-Pattern: Placeholder Labels in Forms

**Wrong:** Using placeholder text as the only form field label.
**Why it fails:** Disappears on input, fails on autofill, inaccessible to screen readers. Users forget what field they're filling once they start typing.
**Correct:** Persistent labels above fields. Placeholder for format hints only (e.g., "MM/DD/YYYY").

### Anti-Pattern: Blaming the User in Error Messages

**Wrong:** "You entered an invalid email" / "Wrong password" / "Error: incorrect input"
**Why it fails:** Users feel blamed and frustrated. Drains goodwill reservoir. Fundamental attribution error — attributing the problem to the person rather than the situation.
**Correct:** "That email wasn't recognized" / "That password didn't match" / System-voice, not user-blame. Active voice for successes, passive for errors.

### Anti-Pattern: Free-Text for Constrained Inputs

**Wrong:** Using a text input for data with a known valid set — dates, quantities, countries, status values.
**Why it fails:** Every error message represents a failure to prevent the error. Users type invalid formats, misspell options, or enter out-of-range values that could have been prevented.
**Correct:** Use constrained controls: date pickers for dates, sliders for ranges, dropdowns for known sets (<20 items), steppers for quantities. Disable invalid options based on current state.

### Anti-Pattern: Starting from Zero

**Wrong:** Presenting empty fields with no defaults, requiring users to fill in everything from scratch.
**Why it fails:** Increases cognitive load and time to completion. Misses signals the system already has (location, time zone, history, common choices).
**Correct:** Pre-fill with intelligent defaults using device data, user history, social data, or environmental signals. Default should be correct for 80%+ of users.

---

## Interaction Design Anti-Patterns

### Anti-Pattern: Multi-Function Components

**Wrong:** A single button or control that does different things depending on context, state, or hidden modes.
**Why it fails:** Users can't predict what will happen. Mode errors cause unintended actions. The component can't be named with a single verb.
**Correct:** One component = one verb (save, send, delete, toggle, search). If a component needs multiple behaviors, split it. A search molecule (input + button + suggestions) has one responsibility despite multiple atoms.

### Anti-Pattern: Hidden-Only Triggers for Primary Actions

**Wrong:** Making a critical action available only through a gesture (swipe), long-press, or keyboard shortcut with no visible alternative.
**Why it fails:** Users can't discover what they can't see. Hidden triggers work for power users but leave everyone else stuck.
**Correct:** Rank by discoverability: (1) visible + labeled, (2) visible + icon, (3) hidden but conventional, (4) hidden unconventional. Primary actions must be Level 1. Expert shortcuts can supplement but never replace visible triggers.

### Anti-Pattern: Toggle Modes Without Indicators

**Wrong:** Using toggle modes (like Caps Lock) without visible indication that the mode is active.
**Why it fails:** Users forget they're in an alternate mode and perform actions with unintended results (mode errors). They blame the software for "not working."
**Correct:** Prefer spring-loaded modes (active only while held, revert on release) for brief states. For toggle modes, show a persistent visible indicator. Auto-revert after single-action modes complete.

### Anti-Pattern: Delight Before Reliability

**Wrong:** Investing in playful animations, witty microcopy, or visual polish while the product still has reliability or usability issues.
**Why it fails:** Users resent personality in a buggy product. A charming but unreliable interface destroys trust faster than a boring but stable one.
**Correct:** Follow Maslow's hierarchy for interfaces: Functional > Reliable > Usable > Pleasurable. Each level must be satisfied before investing in the next. The pleasurable layer creates loyalty, but only on a solid foundation.

---

## Accessibility Anti-Patterns

### Anti-Pattern: Focus State Removal

**Wrong:** Adding `outline: none` or `:focus { outline: 0 }` to remove the default browser focus indicator.
**Why it fails:** Keyboard users (including people with motor disabilities) cannot see where they are on the page. Navigation becomes impossible without a visible focus state.
**Correct:** Never remove focus indicators. Replace the default with a solid background-color highlight (GOV.UK pattern) rather than thin outlines. Ensure 3:1 contrast ratio for the focus indicator against its background.

### Anti-Pattern: "Click Here" for Screen Readers

**Wrong:** Using generic link text ("click here", "learn more") or images without alt text.
**Why it fails:** Screen readers present links and images out of context. "Click here, click here, click here" in a links list is useless. Missing alt text means images are invisible.
**Correct:** Descriptive link text ("View pricing plans"). Alt text that conveys meaning, not file names ("Bar chart showing revenue growth", not "chart.png" or "image"). Decorative images get empty alt (`alt=""`).

### Anti-Pattern: Autoplay Audio/Video with Sound

**Wrong:** Playing audio automatically when a page loads.
**Why it fails:** Triggers startle reflex, creates negative emotional association. Users immediately close the tab. Inaccessible to users in shared environments and those with sensory sensitivities.
**Correct:** All audio muted by default. Video autoplay muted with captions. Sound only on user action.

### Anti-Pattern: Missing Language Declaration

**Wrong:** Omitting the `lang` attribute on the `<html>` element.
**Why it fails:** Screen readers use the wrong voice profile (English text read in a French voice is unintelligible). Spell-checking, translation, and font rendering break silently.
**Correct:** Always include `<html lang="en">` (or appropriate BCP 47 tag). Use inline `lang` attributes when switching languages within content.

### Anti-Pattern: Disabled Pinch-to-Zoom

**Wrong:** Using `user-scalable=no` or `maximum-scale=1.0` in the viewport meta tag.
**Why it fails:** Prevents users with low vision from zooming in to read content. Violates WCAG 1.4.4.
**Correct:** Use only `<meta name="viewport" content="width=device-width, initial-scale=1.0">`. Fix layout issues in CSS, not by disabling zoom.

### Anti-Pattern: Using display:none for Screen Reader Content

**Wrong:** Using `display: none` or `visibility: hidden` to hide content intended for screen readers.
**Why it fails:** These CSS properties hide content from assistive technology too. The screen reader never sees it.
**Correct:** Use the `.visually-hidden` pattern: `position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(1px,1px,1px,1px)`. This hides visually while keeping content accessible.

### Anti-Pattern: Per-Principle Accessibility Tickets

**Wrong:** Creating separate accessibility tickets grouped by WCAG principle ("fix all perceivable issues", "fix all operable issues").
**Why it fails:** Different developers fix fragments of the same component independently, resulting in bloated, over-patched markup (e.g., `<div role="button" tabindex="0" aria-label="...">` instead of simply `<button>`).
**Correct:** Group accessibility issues by component/pattern. One ticket: "Replace `<div>` upvote button with semantic `<button>`." Pattern-based fixes produce fewer tickets and more robust solutions.

---

## Responsive Design Anti-Patterns

### Anti-Pattern: Desktop-First with Breakpoint Overrides

**Wrong:** Designing for desktop viewport first, then adding `@media (max-width: ...)` overrides to cram everything into mobile.
**Why it fails:** Produces mobile experiences that feel like compressed desktop sites. Essential features get hidden or broken at small sizes. The CSS becomes override spaghetti.
**Correct:** Design mobile-first. Start with the smallest viewport, then add `@media (min-width: ...)` rules to enhance for larger screens. This ensures the core experience works everywhere and larger screens get additions, not subtractions.

### Anti-Pattern: Hamburger Menu on Desktop

**Wrong:** Using a hamburger menu icon to hide primary navigation on desktop viewports.
**Why it fails:** Desktop screens have ample room for visible navigation. Hiding it behind a hamburger on desktop reduces discoverability by 50%+ in studies. Users don't explore what they can't see.
**Correct:** Show full horizontal navigation on desktop (5-7 items). Only use hamburger on mobile viewports where space is genuinely limited. Consider a hybrid: visible primary nav + hamburger for secondary items.

### Anti-Pattern: Exact-Fit Containers

**Wrong:** Designing text containers, button widths, or card grids that fit content exactly at its current length.
**Why it fails:** Content changes. Translations can be 30-50% longer. User-generated content varies wildly. Edge cases (long names, extra items) break the layout.
**Correct:** Design with a safety factor of 1.5x for text containers. Allow 30-50% button label growth for internationalization. Test grids with +1 and -1 items from expected count.

---

## Summary Checklist

Before shipping any interface, verify you haven't introduced these anti-patterns:

**Visual:**
- [ ] No equal-weight competing elements — clear 3-level hierarchy exists
- [ ] No true black (#000) or pure white (#fff) — using near-black on near-white
- [ ] No scaled-up small icons
- [ ] No false affordances — if it looks clickable, it is clickable
- [ ] Asymmetric elements aligned by visual weight, not edges

**Typography:**
- [ ] Not relying on size alone for hierarchy — using weight + color + size
- [ ] No `em` units for font sizes — using `px` or `rem`
- [ ] No walls of text without visual entry points
- [ ] Root font size set as `100%`, not pixels
- [ ] Web fonts loaded asynchronously, never render-blocking
- [ ] Inline links have underlines (not color-only)

**Color:**
- [ ] Palette has 8+ grey shades and 9 shades per primary color
- [ ] No color-only meaning — secondary indicators present
- [ ] Contrast meets WCAG minimums (4.5:1 text, 3:1 large text/UI)
- [ ] Colors tested on actual backgrounds, not neutral canvas

**Layout:**
- [ ] Content not stretched to fill viewport — using max-width
- [ ] Labels are closer to their content than to adjacent elements
- [ ] Borders used sparingly — shadows and spacing preferred

**Navigation:**
- [ ] No "click here" links — all link text describes destination
- [ ] Search visible on content-heavy sites (50+ pages)
- [ ] Navigation shows current location
- [ ] Hamburger button has text "Menu" + icon + border
- [ ] Navigation uses `<nav><ul><li>` semantic markup
- [ ] Multiple `<nav>` elements are labeled distinctly

**Behavioral:**
- [ ] No fake scarcity, countdown timers, or manufactured urgency
- [ ] No confirm-shaming opt-out copy
- [ ] Cancellation is as easy as sign-up
- [ ] Notifications are minimal and user-controllable
- [ ] No lowball bait — terms honored after commitment
- [ ] No invisible state changes — all updates visually signaled
- [ ] Undo preferred over confirmation dialogs

**Interaction:**
- [ ] Components have single responsibility (one verb each)
- [ ] Primary actions have visible triggers, not hidden-only
- [ ] Toggle modes have visible indicators
- [ ] Delight layer built on top of reliable, usable foundation

**Forms:**
- [ ] Single-column layout
- [ ] Validation on blur, not keystroke
- [ ] Error messages identify problem + suggest fix
- [ ] Persistent labels above fields — no placeholder-only labels
- [ ] Error messages blame the system, not the user
- [ ] Constrained inputs used instead of free-text where possible
- [ ] Smart defaults pre-filled from available context

**Accessibility:**
- [ ] Focus states visible (background-color highlight, not just thin outline)
- [ ] All links have descriptive text
- [ ] All images have meaningful alt text (or empty alt for decorative)
- [ ] Touch targets meet minimum size (44px mobile, 32px desktop)
- [ ] No autoplay audio — all sound user-initiated
- [ ] `<html lang>` attribute set correctly
- [ ] Pinch-to-zoom not disabled
- [ ] `.visually-hidden` used (not `display: none`) for screen-reader content
- [ ] Accessibility issues grouped by component pattern in audits

**Responsive:**
- [ ] Mobile-first CSS approach
- [ ] Full navigation visible on desktop (no hamburger)
- [ ] Containers sized with safety factor for content growth and i18n