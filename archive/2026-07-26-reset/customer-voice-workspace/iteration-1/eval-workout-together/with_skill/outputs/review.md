## Customer Review: Workout Together

### Impact Assessment
**Personas served**: Guided Explorer (Marilyn), Busy Optimizer (Teresa), Power Tracker (Arthur), Tech-Savvy Engager (Chris)
**Weighted coverage**: 90% (42% + 20% + 17% + 11%)
**Primary beneficiary**: Guided Explorer (Marilyn) at 17% base weight, elevated to **34%** via the Peloton Parity Rule (Peloton has community challenges, friend activity, and group workout features)

### First Reaction
A turn-based workout with my partner on the same device? That actually sounds fun. My wife has been wanting to try the Amp but I always feel like I have to give up my session for her to use it. Being able to do it together — taking turns on the cable — means we both get a workout in and keep each other accountable. The 60% household stat rings true. But I have questions: how long does this take? If I normally do a 30-minute workout, does this become 60 minutes because we're alternating? And what does my partner see on screen while I'm doing my set — are they just standing there?

### Would I Use This?
Yes, if I have a partner or guest who wants to try Amp. The value is clear for households. But this is situational — I'm not using it every session, only when someone else is around. The 0.25% adoption rate the PRD flags is concerning and suggests most users either don't know it exists or don't find it compelling enough to try. The turn-based model is smart because it doesn't require two devices, but the session length question is real. If a Workout Together session takes twice as long, the Busy Optimizer crowd (20% of users) will skip it entirely.

### What I Like
- **Solves a real household problem** — Power Trackers (42%) and Guided Explorers (17%) who share a device with a partner finally have a structured way to work out together instead of awkwardly trading off. Danielle (Busy Optimizer cluster) specifically noted her household member adopted Amp because of convenience: "He's just really happy to have it honestly."
- **Guest-to-buyer conversion funnel** — Letting a guest experience Amp in a structured workout is smarter than just handing them the phone and saying "try it." This creates a natural acquisition moment.
- **Turn-based is the right model** — No extra hardware needed. One device, two people. This respects the product's physical constraint without forcing a multi-device solution.
- **Peloton competitive gap closure** — Peloton has community workouts and social features that Guided Explorers (17%, elevated to 34% via Peloton Parity) benchmark against constantly. Marilyn's cluster has 72 Peloton competitor mentions. This is a step toward social parity.

### What Confuses Me
- **Session duration is unaddressed** — Arthur (Power Tracker, 42%): "Will this slow down my workout flow or add unnecessary steps?" If a 30-minute workout becomes 60 minutes with turn-based alternation, that fundamentally changes the value proposition. The PRD doesn't clarify expected session length.
- **What does the non-active person do?** — When it's not my turn, am I just watching? Is there a rest timer? Can I see what's coming next for me? The in-between experience is undefined.
- **Guest profile and data** — The PRD mentions "capturing guest data for downstream conversion" but the Phase 1 non-goals exclude guest email summary and dual-summary screen. So what does the guest actually get out of this? If there's no summary or follow-up, the conversion funnel has no bottom.
- **0.25% adoption vs. 3% target** — The PRD acknowledges this is already shipped with terrible adoption. What's different about Phase 2 that will close this 12x gap? An entry animation alone won't do it.

### What Worries Me
- **Analytics blackout is a BLOCKER for everyone** — The PRD itself flags that the `is_workout_together` event property returns zero data. You cannot measure success of a retention/acquisition feature if you cannot track whether anyone is using it. This isn't a nice-to-have fix; it's a prerequisite. Every persona is affected because the team is flying blind.
- **Backend crash risk (SW-9981)** — A crash during a shared workout is worse than a crash during a solo session because you're embarrassing the owner in front of their guest. That guest will never buy an Amp. This is an NPS risk that disproportionately affects Recovery Seekers (4%) who are already cautious, and Guided Explorers (17%) who will compare unfavorably to Peloton's stability.
- **Discoverability is unsolved** — The feature sits on the pre-workout screen but 0.25% adoption means almost nobody finds it or bothers. Teresa (Busy Optimizer, 20%): "Does this require setup or configuration, or does it just work?" If she has to hunt for it, it doesn't exist for her.

### What's Missing
- **Session duration expectations** — Power Tracker (42%): How long will a WT session take compared to solo? This is the single most important missing piece for the highest-weight persona.
- **Rest/transition UX between turns** — All personas: What happens between turns? Is there guidance, a timer, warm-up suggestions? The mid-workout experience for the waiting partner is completely undefined.
- **Workout intensity calibration for two users** — Recovery Seeker (4%, NPS risk): If the owner is at 80 lbs and the guest is a beginner at 20 lbs, does the system handle weight adjustments between turns? Almond specifically said: "I would actually want to tell you that I'm struggling with this hamstring issue and stop giving me hamstring-related workouts." Intensity personalization per participant is absent.
- **Guest onboarding flow** — Busy Optimizer (20%): What does the guest need to do? Create a profile? Enter their weight preferences? Any setup beyond zero will trigger the Onboarding Tax.
- **Progress tracking for WT sessions** — Power Tracker (42%): Do WT sessions count toward my volume tracking, streaks, and personal records? Arthur cares deeply about seeing "weight numbers climb over weeks." If WT sessions don't feed into his progress data, he'll avoid them.
- **Floor exercise handling** — Tech-Savvy Engager (11%) and Recovery Seeker (4%): Chris Burke's cluster specifically called out no verbal cues during floor exercises. In a WT session with turn-taking, audio cues become even more critical for coordinating who goes when.

### The Real Test
Arthur (Power Tracker, 42%): "If I do Workout Together with my wife, do my sets still count toward my weekly volume and personal records — or am I sacrificing my tracking data to share the device?"

### Weighted Persona Reactions
(Ordered by weight — highest impact first)

1. **Arthur (Power Tracker) — 42% weight**: "I'd try this with my wife, but I need to know it doesn't mess up my tracking. My volume numbers, my progressive overload — that data is sacred. If WT sessions get logged differently or don't count toward my totals, I'll just let her do her own session separately." David from this cluster noted he cares about incremental weight increases: "On that last third or fourth set, it'll increase it by 2 to 5 pounds." WT must preserve per-user progressive overload tracking.
   --> Impact: **MILD CONCERN** — Will use it if tracking integrity is preserved, but the PRD doesn't confirm this. Not a blocker because he can simply not use the feature, but a missed opportunity for the highest-weight segment.

2. **Teresa (Busy Optimizer) — 20% weight**: "I have 20 minutes before picking up the kids. If Workout Together means my 20-minute session becomes 40 minutes of alternating, that's a hard no. Also — does my guest need to set up a profile? Because I'm not spending 5 minutes on that." Gabrielle from this cluster said: "I couldn't finish the program because some of the classes were just too long for what I had available." Session length is the deciding factor.
   --> Impact: **MILD CONCERN** — Applying the **Onboarding Tax Rule**: If the guest needs any setup (profile creation, weight calibration), Teresa's reaction drops to BLOCKER. The PRD doesn't specify the guest onboarding flow, so this is an open risk. If zero-setup, she's NEUTRAL — she'll use it occasionally but it's not her primary use case.

3. **Marilyn (Guided Explorer) — 17% weight** (Peloton Parity Rule: elevated to **34%**): "Finally! This is the kind of social thing Peloton has had forever. I've been wanting to work out with my partner but we always end up doing separate sessions. The structure of turn-based is good — it's like a class format where someone tells you what to do. But where are the badges? Where's the shared achievement? Peloton would gamify this." Nora from this cluster uses Peloton's stacking feature to plan routines, and Faith loves badges. WT without gamification is a half-measure for this persona.
   --> Impact: **STRONG POSITIVE** — This is table stakes social functionality that closes a Peloton gap. The 72 Peloton competitor mentions in this cluster confirm social features are a retention lever. Even without gamification in Phase 1, the core turn-based mode is valued.

4. **Chris (Tech-Savvy Engager) — 11% weight**: "Interesting concept. I want to see the data — does it track both users' metrics separately? Can I compare my performance to my workout partner? And what about rest periods between turns — are those configurable? I'm very particular about my rest intervals." Chris Burke looks at "all the insights — sleep performance, like every bit of these metrics." He'll want WT to feed into his data ecosystem, not exist as a separate silo.
   --> Impact: **NEUTRAL** — Interested but not a primary driver. Will engage if the data integration is clean. No blockers.

5. **Supriya (Self-Directed Builder) — 6% weight**: "Can I use this with my trainer? If my trainer is standing there and we're alternating sets, this could actually be useful for coached sessions. But I'd need to be able to build my own WT workout, not just pick from the library." Supriya values Build Your Own Workout: "One of the really cool things has been being able to build my own workout." If WT is library-only, this persona loses interest.
   --> Impact: **NEUTRAL** — Niche use case. Not blocked, not excited. Would become positive if custom WT workouts were supported.

6. **Almond (Recovery Seeker) — 4% weight** (NPS risk): "I'm worried about the intensity. When I work out with someone else, there's social pressure to keep up. If my partner is doing 60 lbs and the app doesn't adjust for my recovering hamstring, I'll push too hard and get hurt. Does the system know I have limitations even in WT mode?" Almond explicitly said: "I would actually want to tell you that I'm struggling with this hamstring issue." Social pressure in WT could override recovery-appropriate intensity.
   --> Impact: **MILD CONCERN** — Applying the **NPS Detractor Rule**: This feature touches workout intensity and personalization (two users at different fitness levels sharing a session). The PRD does NOT mention per-user intensity adaptation or opt-out/override for the less-fit participant. However, the turn-based model inherently allows each user to set their own weight, which partially mitigates this. Not a full blocker, but needs explicit acknowledgment. Recovery Seeker weight stays at 4% (does not triple to 12%) because the turn-based model provides implicit opt-out — each user controls their own resistance on their turn.

### Rule Checks
- [x] **Silent Persona**: No persona >= 15% weight is unaffected. All major personas have a reaction. PASS.
- [x] **Peloton Parity**: YES — Peloton has community challenges, group workouts, and friend activity feeds. Guided Explorer weight elevated from 17% to **34%** for this review. This is table-stakes social functionality.
- [ ] **NPS Detractor**: Feature touches workout intensity with two users at different levels. The turn-based model provides implicit per-user control (each sets their own weight on their turn), so the Recovery Seeker weight is NOT tripled. However, the PRD should explicitly address mixed-fitness-level pairing and confirm per-user intensity is preserved.
- [x] **Onboarding Tax**: Guest onboarding flow is undefined in the PRD. If ANY setup is required for the guest (profile, weight calibration, account creation), the Busy Optimizer (20%) reaction becomes BLOCKER. The PRD must specify a zero-friction guest entry. FLAG: "The guest onboarding experience must be explicitly zero-setup or Teresa's 20% weight becomes a blocker."
- [x] **Quote or Flag**: All persona reactions reference real interview data or behavioral data points. PASS.
  - Arthur: David quote on progressive overload
  - Teresa: Gabrielle quote on session length constraints
  - Marilyn: Nora on Peloton stacking, Faith on badges, 72 Peloton mentions in cluster
  - Chris: Chris Burke quote on metrics engagement
  - Supriya: Supriya quote on Build Your Own Workout
  - Almond: Almond quote on injury personalization
- [ ] **Cannibalization**: Does not replace an existing feature. WT is additive to solo workouts. PASS — no cannibalization risk.
- [x] **Mid-Workout Disruption**: YES — this fundamentally changes the in-workout experience by adding turn-based transitions. The PRD does not address: (a) what the non-active user sees during their partner's turn, (b) audio cues for turn transitions especially during floor exercises where users cannot see the screen, (c) whether the 90.4% completion rate will be affected by the added complexity. FLAG: "Turn transitions during floor exercises need audio/haptic cues. Users cannot see the screen during floor work — Chris Burke's cluster specifically flagged this gap."

### Verdict
**Feature type**: **Retention** (primary) / **Growth** (secondary — guest conversion)
**Positive weight**: **87%** — Power Tracker (42%, mild positive), Guided Explorer (34% via Peloton Parity, strong positive), Tech-Savvy Engager (11%, neutral-positive). Using strict STRONG POSITIVE only: **34%** (Guided Explorer).
**Blocked weight**: **0%** — No persona is fully blocked, though Busy Optimizer (20%) becomes blocked if guest setup is required (Onboarding Tax).
**Decision**: **Iterate** — Good direction but needs work to reach more personas.

The Guided Explorer (34% Peloton-adjusted weight) is strongly positive because this closes a social feature gap with Peloton. The Power Tracker (42%) is conditionally positive but the PRD fails to address whether WT sessions feed into individual tracking — the single most important data point for the largest persona. The analytics blackout (zero measurement capability) is a critical operational risk that affects all personas equally: you cannot iterate on what you cannot measure. Fix the `is_workout_together` event property before investing in Phase 2 features. The 0.25% adoption rate suggests the core concept may need rethinking beyond just an entry animation — consider lifecycle messaging, household detection, and contextual prompts when a second user is detected on the device.
