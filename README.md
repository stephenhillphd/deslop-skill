# deslop

A [Claude Code](https://claude.com/claude-code) skill that removes AI-slop patterns from prose. It targets writing that sounds emphatic while saying little, and it aims for plain, direct sentences that keep the original facts.

The rules were developed on data-journalism and sports-analytics writing, so the examples lean that way. The patterns apply to any factual writing.

## What it catches

1. Verbless noun-phrase fragments tacked on for emphasis
2. Announcing an idea before stating it ("what this really shows is")
3. A colon that delivers an aphorism
4. Formulaic contrast ("not X, but Y")
5. Personified data, models and events ("the data tells the story")
6. Overclaims and promotional lines
7. Inflated metaphor
8. Rule of three and anaphora
9. Em dashes (optional)
10. Dramatic setup followed by a reversal

`SKILL.md` gives a before/after example for each, plus a list of things to leave alone.

## Example

Before:

> A run that had lasted since November 2022 was over. Sixty-two games, with three consecutive state titles inside them.

After:

> A run that had lasted since November 2022 was over. It reached 62 games and included three consecutive state titles.

## Install

```bash
git clone https://github.com/stephenhillphd/deslop-skill ~/.claude/skills/deslop
```

Claude Code picks the skill up automatically. Ask it to "de-slop" a file, scan a folder of articles, or write new prose without the patterns.

## The scanner

`scripts/scan_tells.py` flags the mechanical tells with line numbers. It uses only the Python standard library and reads `.html`, `.md` and `.txt` files.

```bash
python3 scripts/scan_tells.py drafts/*.md
python3 scripts/scan_tells.py --fragments drafts/post.md   # noisy verbless-sentence check
python3 scripts/scan_tells.py --allow-em-dash README.md    # skip the em-dash check
```

Every hit is a candidate for judgment. The scanner cannot see a smooth aphorism or an uncheckable claim, so it supplements reading the text.

To add a pattern, append a `(name, regex)` pair to `CHECKS` in the script.

## License

MIT
