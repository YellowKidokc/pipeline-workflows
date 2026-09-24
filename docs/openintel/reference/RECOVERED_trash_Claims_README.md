# Claims — The specific things you're trying to prove

> A "claim" is one specific assertion. Not your whole theory — just one piece of it.

## What goes here

A claim is one sentence that could be true or false. Examples:

- *"John Smith sold his stock on April 19, 2019."*
- *"The hospital closed because of a federal investigation, not because of finances."*
- *"There were three vans, not two, at the warehouse on April 12."*
- *"The official cause of death is incompatible with the autopsy report."*

Notice how each one is **specific and testable.** You could in principle find evidence that proves or disproves each one.

## Claims are not the same as your hunch

Your overall hunch (in `HUNCH.md`) might be big and complicated. *"I think there was a cover-up."* That's a hunch.

A **claim** is a small piece of that hunch that can be checked. *"The press conference happened before the autopsy was complete."* That's a claim. You can check it. You can be right or wrong about it.

Most cases have **3 to 10 claims.** Each one is a smaller fight. The case wins if enough of the small fights are won.

## How to add a claim (the easy way)

Create a file named with a short tag: `claim_stock_sale.md`, `claim_press_conference_timing.md`. Inside:

```
The claim: (one sentence — must be specific and testable)

Why I think this is true:
- (evidence point 1)
- (evidence point 2)

What would prove me wrong:
- (specific evidence that, if found, would mean my claim is false)

How sure am I right now: (gut percentage, 0-100%)
```

## The "what would prove me wrong" question is the most important

If you can't answer it, you might not actually have a claim — you might have a feeling that's not testable yet. That's fine, but mark it as such. The system rewards investigators who know the difference.

## Three flavors of claim

When curators map your claims into the database, they tag them:

- **CORE** — claims your whole case depends on. If a CORE claim falls, the case falls.
- **SUPPORTING** — claims that strengthen the case but aren't load-bearing.
- **PERIPHERAL** — claims that are interesting context but don't make or break anything.
- **CONTESTED** — claims you and the official version disagree on.

You don't have to assign these yourself. Just write the claims; curators will tag them.

## What this becomes on the back end

Each claim becomes a row that links to: the evidence supporting it, the evidence against it, an NLI score (an AI checks whether your claim contradicts other claims in the database), and a confidence number. Over time, claims get reviewed and re-tiered as new evidence comes in.

---
*One folder up: `../START_HERE.md` · The case file: `../HUNCH.md`*
