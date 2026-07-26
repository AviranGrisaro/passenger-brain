# Customer Perspective Review: Workout Together

## Overall Impression

As someone who owns a home fitness device and shares it with my partner, I was excited to see a "Workout Together" feature. The core idea makes sense -- my partner and I constantly negotiate who gets the machine, and working out side by side (even taking turns) would be way more motivating than working out alone. The concept clicks immediately.

But after reading this PRD, I have more questions than answers about what the experience would actually be like.

## What I Like

**The problem is real.** The PRD nails it when it says owners have to choose between their own session and letting someone else try. My partner has been curious about the amp but there has never been a natural way to get her involved. A structured shared workout would solve that.

**Turn-based makes sense for a single device.** I was initially hoping for something simultaneous, but thinking about it, turn-based is practical. You take turns on the machine, and having the software manage that flow means neither person is just standing around awkwardly.

## What Concerns Me

### I have no idea what the actual experience looks like

This is my biggest frustration with this document. It tells me the feature exists, but I cannot picture what happens when I actually use it. How do I start a Workout Together session? What does the screen look like when it is my partner's turn? Do we pick exercises together or does the app decide? How long are the turns? Can we customize the workout? Is there a shared timer? What happens if one person wants to quit early?

The PRD says there is an "entry animation" that shipped, and that the feature is accessible from the "pre-workout screen," but that is all I get. As a customer, I need to understand the flow before I would try something new, especially if it involves convincing my partner to join me.

### The feature seems to be struggling already

The document mentions 0.25% adoption against a 3% target. That is a huge miss. As a customer, this makes me wonder: is the feature hard to find? Is it confusing to use? Did people try it and not come back? The PRD acknowledges low discoverability but does not dig into whether people who found it actually liked it. If the people who tried it are not coming back, that is a different problem than people not knowing it exists.

### Analytics are broken, so how do you know if it works?

The PRD lists an "analytics blackout" as a critical risk, saying the tracking property returns zero data. This is alarming from a customer perspective -- not because I care about internal metrics, but because it means the team cannot tell whether this feature is actually working for people like me. If they cannot measure it, they cannot improve it. That makes me less confident the experience will get better over time.

### There is a backend crash risk

The PRD mentions a crash bug (SW-9981) that is still being assessed. As a user, nothing kills my trust in a feature faster than the app crashing mid-workout. If I am working out with a friend or my partner and the app crashes, that is embarrassing, and I probably will not try the feature again.

### No summary or follow-up for my partner

Under "Non-Goals," the PRD says a dual-summary screen and guest email summary are deferred to Phase 2. This is a missed opportunity. If my partner works out with me and gets nothing afterward -- no stats, no summary, no encouragement to come back -- the experience feels incomplete. The moment after a shared workout is when someone is most likely to think "hey, maybe I should get my own subscription." Without a follow-up, you lose that moment.

## What is Missing

### The customer experience, in any detail

There is no user story, no flow description, no wireframes referenced (the Figma link is there but I cannot access it). I want to know:
- What workout types support this? All of them? Only certain ones?
- Can I pair with a guest who does not have an account?
- What does the guest see vs. what the owner sees?
- Is there a competitive element (like a leaderboard between the two of us)?
- Can I do this with my kid? Are there age or difficulty adjustments?

### Who is the guest?

The PRD talks about "guest-to-buyer conversion" but never describes who this guest is. Is it my partner who lives with me and uses the machine regularly? A friend visiting for the weekend? My parent who is curious about fitness tech? Each of these people has very different needs and very different likelihood of converting. The feature should probably behave differently for a household member who works out weekly vs. a one-time visitor.

### What happens after the workout?

There is zero information about the post-workout experience. Do both people see their stats? Can we compare how we did? Is there a social sharing moment? Can I save my partner as a recurring workout buddy so setup is faster next time? The workout itself is only half the value -- the social and reflective moment afterward matters just as much.

### Household use case vs. guest use case

These feel like fundamentally different scenarios that are lumped together. If my partner and I work out together three times a week, we need profile support, history tracking, and personalized difficulty. If a friend visits once, we need frictionless onboarding with zero sign-up barriers. The PRD does not distinguish between these.

### Motivation and social dynamics

Why would I choose a turn-based workout over just doing my workout and then handing the device to my partner? The feature needs to offer something that makes sharing better than taking turns informally. Shared goals, friendly competition, synchronized coaching, encouragement between sets -- something that makes it feel like we are doing this together rather than just waiting for our turn.

## Bottom Line

I want this feature to exist. The problem it solves is real and personal to me. But this PRD reads like an internal tracking document for the team, not a blueprint for a great customer experience. It focuses on metrics (WAU, retention, conversion) without describing the experience that would drive those metrics. The critical risks around analytics, crashes, and low adoption suggest the feature shipped in a minimal state that has not yet found product-market fit.

If I were a customer seeing "Workout Together" on the device today, I would try it once. Whether I come back depends entirely on how the experience feels -- and this PRD does not give me confidence that the experience has been deeply thought through from the customer's side.

My advice: before adding lifecycle messaging or entry animations to boost discoverability, make sure the people who do find it have a reason to come back. Fix the tracking so you can learn from actual usage. Ship the post-workout summary so guests feel valued. And talk to the couples and households already using it to understand what makes them stay or leave.
