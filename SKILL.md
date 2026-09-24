---
name: deslop
description: |
  Remove AI-slop patterns from prose using a strict set of plain-writing rules:
  no verbless emphasis fragments, no announcing an idea before stating it, no
  colon-delivered aphorisms, no formulaic contrast ("not X, but Y"), no
  personified data or models, no overclaims or promotional lines, no
  manufactured one-liners chasing quotability, no two full clauses spliced with
  ", and", and (optionally) no em dashes.
  Use this whenever the user calls text AI slop, says "fix this language",
  "avoid this pattern", "de-slop", "this reads like AI", or asks to scan,
  review, audit or clean up articles, site copy, drafts, README prose or any
  writing before publishing. Use it too when writing new prose for the user's
  sites, so the patterns never land in the first place. Suited to plain,
  factual writing such as data journalism, reports and documentation. It does
  not add personality or opinions, so it is a poor fit for voice-heavy writing.
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash
---

# De-slop

The target is plain, direct prose where every sentence carries information. The
skill fixes writing that sounds emphatic while saying little, usually because a
plain fact has been given rhetorical decoration.

Most of these patterns come from an instinct to make prose feel significant.
Removing them should leave the facts alone and add nothing in their place. In
analytics writing the numbers are already interesting. The decoration makes a
reader trust the work less.

## Workflow

**When the user points at one sentence** ("fix this language"), rewrite it, then
grep the rest of the file and its siblings for the same construction. The user
usually wants the pattern removed everywhere. Report what else
you found with `file:line` and the exact quote, and ask before widening the edit
unless they already said to fix everything.

**When the user asks for a scan**, run `scripts/scan_tells.py` first to catch
the mechanical tells, then read each article's text end to end. The worst
offenders (an aphorism that reads smoothly, a manufactured one-liner, a claim
nobody can check) match no regex. Report findings
grouped by pattern, most severe first, each as `file:line` plus the quoted text
so the user can judge it in one pass. Recommend which to fix; let them choose.

**One pass is rarely enough on a document written to sound polished.** A
three-pass review of one slide deck found personification the first time
through, more personification the second time (hiding behind a domain-standard
verb like "explains" used with a vague subject), and a batch of manufactured
one-liners the third time that were not personification at all. After a scan
comes back clean, do not report it as done; reread it once more looking
specifically for pattern 11, since it is the pattern most likely to survive
a check built around the other ten.

**When fixing**, preserve the fact and the tone. After each edit, re-read the
whole paragraph, because a rewrite commonly introduces a word repeat the
original avoided ("a run that had lasted... The run reached 62 games").

**Verify before claiming done.** Confirm tag balance for HTML, confirm no em
dash slipped in, and show the user the rewritten passages in context.

## The patterns

### 1. Verbless noun-phrase fragments for emphasis

A fragment tacked after a full sentence to give a number extra weight. Write it
as a sentence with a subject and a verb.

- Before: "...a run that had lasted since November 2022 was over. Sixty-two games, with three consecutive state titles inside them."
- After: "...a run that had lasted since November 2022 was over. It reached 62 games and included three consecutive state titles."
- Before: "Bigger schools, deeper rosters, better average teams. No surprise."
- After: "Bigger schools draw from more students and field better teams on average."

A short sentence that carries content is fine ("It isn't." "They didn't.").
The test is whether the fragment adds information or just cadence.

### 2. Announcing an idea before stating it

"There is an obvious hypothesis sitting in that", "what this really shows is",
"the deeper point here", "the honest answer is", "honesty requires saying". Drop
the announcement and make the claim.

- Before: "There is an obvious hypothesis sitting in that, and one game cannot test it: a team winning by 39 every week gets no practice at winning by four."
- After: "These files cannot say whether a team that wins by 39 every week is any worse at winning by four. The two close games on record both came in the last two weeks, which is not enough to test it."

The fix names the question the data cannot answer and says what evidence
would settle it, where the original only hinted at a limitation.

### 3. A colon that delivers an aphorism

Explanatory colons are fine and common in plain writing ("The exception:
if the team that just scored is still trailing..."). The banned move is building
a sentence toward a colon that pays off in a slogan.

- Before: "This is the cleanest example in our data of a lesson that applies to every stat a coach keeps: a raw split will happily lie to you if you don't ask who was on each side of it."
- After: "The same correction applies to any split a coach keeps. A raw comparison of two groups of games measures the thing you split on only if the teams on each side are otherwise comparable."
- Before: "The retention election is precisely that: a possession you can purchase, at a price."
- After: "The retention election supplies one, in exchange for a fourth-down snap from your own 20."

The second fix shows the general repair, which is to replace the abstraction
with the concrete thing it stood for.

### 4. Formulaic contrast and negative parallelism

"not X, but Y", "X did not do the work; Y did", "aren't always the most
athletic; they're often the best prepared", "Enrollment sorts the averages, not
the contenders". Use contrast only where the distinction carries meaning, never
to make a sentence land.

- Before: "Not a talent for close finishes, because there were none. What it took instead was holding 80% of opponents scoreless..."
- After: "The streak required holding 80% of opponents scoreless, averaging 42 points, and doing it again through five playoff rounds. It did not require any skill at close finishes, because there were none."

### 5. Personified data, models, games and events

Data, models, metrics, seasons, games and schedules do not act, know, tell,
argue, decide, lie, carry weight or do work. State the causal or statistical
relationship instead. This is the pattern the user catches most often, and the
giveaway phrase is "doing the work".

- Before: "because who you played is doing as much work as whether you won"
- After: "because opponent strength affects the rating as much as the win-loss record does"
- Before: "which teams the model was still arguing with itself about"
- After: "where the two ratings disagreed most"
- Before: "your red zone playbook writes itself"
- After: "you can build the red zone playbook around beating man"

Sports idiom is not automatically personification. "The margins never
compressed" and "the schedule connects the divisions" describe real patterns.
"The season buries it" and "the data proves it every season" do not.

Causal verbs like "explains" and "predicts" are domain-standard, not
personification, when the subject is a concrete named variable: "Age explains
the gap" is a statistical claim, not a colorful one. The same verb turns back
into personification when the subject is vague or refers to itself: "Nothing
about the row explains it" and "The value explains its own absence" both read
as something abstract doing the explaining. Judge the subject, not just the
verb.

- Before: "The value explains its own absence."
- After: "The number itself is why it is missing."

### 6. Overclaims and promotional lines

Superlatives nobody can check, and copy that sells rather than reports.
"the biggest strategic change the sport has seen", "an edge no other coach is
using", "tells you everything about coverage", "Simple tracking reveals powerful
tendencies", "the data proves it". Replace with the specific claim the evidence
supports, or cut.

- Before: "The retention rule is the biggest strategic change flag football has seen since states began sanctioning the sport."
- After: "The retention rule gives trailing teams a late-game option they have never had."

### 7. Inflated metaphor

Extended figures that add grandeur: threads forming a web that touches everyone,
scheduling that stitches a state together, a defense parting like the Red Sea.
One plain clause does the job.

- Before: "Every one of those games is a thread tying two teams together, and with hundreds of games a season, the threads form a web that touches everyone."
- After: "Each of those games links two teams, and with hundreds of games a season almost every team connects to every other through some chain of opponents."

### 8. Rule of three and anaphora

Three parallel clauses, or three sentences opening with the same words
("Nobody knows... Nobody knows... Nobody knows"), used for rhythm. Collapse into
one sentence with a list. Genuine three-item lists (three things to do before a
game) are fine.

### 9. Em dashes (optional rule)

This rule is on by default. If the user does not ban em dashes, skip it and
pass `--allow-em-dash` to the scanner. When it applies, use a comma, a period,
or a colon where a colon genuinely introduces. Check for em dashes after every
edit, including the character inside HTML entities.

### 10. Dramatic setup followed by reversal

"Read those numbers naively and home field looks like a touchdown of advantage.
It isn't." is fine, because the reversal is the finding. Cut a setup that exists only to
make the next sentence feel like a revelation, and write one straightforward
sentence instead.

### 11. The manufactured one-liner

A sentence built to be quotable rather than to state the fact plainly: an
ironic reveal, a wry aside, or a turn of phrase doing more work than the
underlying claim needs. This is not personification and it is not any of the
other ten patterns; there is no construction to grep for. The tell is whether
the sentence would work as a pull-quote. If it would, flatten it, even if that
costs some rhythm.

- Before: "Errors survive all of it."
- After: "Errors go undetected."
- Before: "Now nobody has an age, including the five people who reported one."
- After: "The age is gone for every row, including the ones that had one."
- Before: "Two good incomes went out with the two missing ages."
- After: "The two dropped rows also had complete incomes."
- Before: "each one costs something different"
- After: name the actual cost, or tie it to a fact already on the page, rather
  than promising one in the abstract.

This is the hardest pattern to self-check, because a writer reaches for
exactly these lines when a paragraph feels flat and needs a landing sentence.
Reread the sentence that closes each point and ask whether it says anything
the plain version does not. If the only difference is rhythm, cut the rhythm.
Expect this pattern to survive a first and even a second pass: it hides behind
sentences that already passed the other checks, so a scan that stops once
those are clean is not done.

### 12. Two independent clauses spliced with ", and"

When a sentence joins two complete clauses with ", and" (or a loose ", so"),
write them as two sentences. A spliced sentence carries two claims. The reader
has to find where one ends.

- Before: "You get two attempts, and I keep the higher score."
- After: "You get two attempts. I keep the higher score."
- Before: "You may use Claude or ChatGPT, and the last question asks how you used it."
- After: "You may use Claude or ChatGPT. The last question asks how you used it."
- Before: "I am away for this class meeting, so you will complete this quiz instead."
- After: "I am away for this class meeting. You will complete this quiz instead."

Leave three things joined. The first is a real list ("best-of-3, best-of-5 and
best-of-7"). The second is a compound with one subject ("name the tool and say
what you asked it"). The third is a ", so" whose causal link is the point of
the sentence: "The better team wins exactly when it takes 4 of the 7 games, so
this formula scores the series" stays as one sentence, because splitting it
loses the reason.

## What to leave alone

- Explanatory colons, ordinary idiom, and the author's first person. A line
  like "This is the number that changed how I read the streak" stays.
- Short sentences and one-line paragraphs that carry content.
- The author's voice. Do not add personality, opinions or edge to
  replace what you removed. The plain version is complete as written.
- Deliberate brand lines on marketing pages, unless the user asks. Flag them
  instead.
- Facts. Never adjust a number, a date or a claim to make a sentence flow. If a
  rewrite would change what is being asserted, report that instead of editing.

## Reporting format

```
**Pattern name** (what it is in four words)

- `path/to/file.html:107`: "the exact quoted sentence"
- `path/to/other.html:193`: "the exact quoted sentence"
```

Group by pattern, most severe first, and end with a recommendation and a plain
question about scope. Keep the quotes exact so the user can search for them.

## The scanner

`scripts/scan_tells.py` flags mechanical tells with line numbers and works on
`.html`, `.md` and `.txt`:

```bash
python3 ~/.claude/skills/deslop/scripts/scan_tells.py public/articles/*.html
python3 ~/.claude/skills/deslop/scripts/scan_tells.py --fragments drafts/post.md
python3 ~/.claude/skills/deslop/scripts/scan_tells.py --allow-em-dash README.md
```

Every hit is a candidate that needs judgment. The scanner misses smooth
aphorisms entirely, so read the prose as well.
