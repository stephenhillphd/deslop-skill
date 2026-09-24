#!/usr/bin/env python3
"""Flag mechanical AI-slop tells with line numbers.

Every hit is a candidate that needs judgment. Smooth aphorisms and
unverifiable claims match no regex, so read the prose too.

Usage:
    scan_tells.py [--fragments] [--allow-em-dash] FILE [FILE ...]

--fragments      adds a noisy verbless-sentence check (many false positives on
                 headings, list labels and legitimate short sentences).
--allow-em-dash  skips the em-dash check, for writers who do not ban them.
"""
import html
import re
import sys

TAG = re.compile(r"<[^>]+>")
SKIP_LINE = re.compile(r"^\s*(?:</?(?:script|style|nav|footer|head|meta|link)\b|\{|//)")
# Structured data and headings are terse by design; judging them as prose only
# produces noise. Em dashes still matter everywhere, so that check runs anyway.
SKIP_ALL = re.compile(r'"(?:description|headline|name|abstract)"\s*:|^\s*[\[{"]')
HEADING = re.compile(r"<h[1-6][\s>]", re.I)

CHECKS = [
    ("em-dash", re.compile(r"—|&mdash;")),
    ("not-X-but-Y", re.compile(r"\bnot\s+(?:just\s+|only\s+)?[^,.;:]{2,45},\s*but\b", re.I)),
    ("negative-parallelism", re.compile(
        r"\b(?:isn't|aren't|wasn't|weren't|is not|are not|was not|were not)\b[^.;!?]{2,70};\s*"
        r"(?:it's|they're|it is|they are|he's|she's|they just|it just)\b", re.I)),
    ("announced-idea", re.compile(
        r"\bthere (?:is|are) an? (?:obvious|interesting|important|simple|clear)\b"
        r"|\bwhat (?:this|that) (?:really )?(?:shows|means|tells us|reveals)\b"
        r"|\bthe (?:real|deeper|bigger|broader|interesting) (?:story|question|point|lesson|part|issue)\b"
        r"|\bthe honest answer\b|\bhonesty requires\b|\bit(?:'s| is) worth noting\b"
        r"|\bthe (?:key|crucial) (?:insight|takeaway) (?:here )?is\b", re.I)),
    ("personification", re.compile(
        r"\b(?:data|model|models|numbers|rating|ratings|stats|statistics|metrics?|"
        r"season|schedule|streak|spread|split|standings|scoreboard)\b"
        r"[^.,;:!?]{0,15}\b(?:does the work|doing the work|did the work|tells? the story|"
        r"telling the story|says?|said|speaks? to|knows?|argues?|arguing|lies? to|lying to|"
        r"writes? itself|carries the weight|drives? the|tempts?|buries|stitch(?:es)?|"
        r"proves? it|decides? who|deciding who|wants? to)\b", re.I)),
    # Banned outright whatever the subject.
    ("banned-idiom", re.compile(
        r"\b(?:doing|does|did)\s+(?:all\s+|as much\s+|most of\s+|the\s+)(?:the\s+)?work\b"
        r"|\bcarr(?:y|ies|ying) the weight\b"
        r"|\btells? the story\b|\bspeaks? volumes\b", re.I)),
    ("overclaim", re.compile(
        r"\btells you everything\b|\bproves? it\b|\breveals? powerful\b|\ban edge no (?:other|one)\b"
        r"|\bthe (?:biggest|greatest|most important|single most) [a-z ]{3,45}(?:ever|has seen|in the (?:sport|industry|field))\b"
        r"|\bgame[- ]?chang(?:er|ing)\b|\brevolution(?:ary|ize)\b|\bunlocks?\b|\bpowerful insights?\b"
        , re.I)),
    ("inflated-metaphor", re.compile(
        r"\bparting of the red sea\b|\bstitch(?:es|ing)? [^.;!?]{0,30}together\b"
        r"|\bweb that touches\b|\btapestry\b|\bsymphony\b|\bcrucible\b|\bbeating heart\b", re.I)),
    # Two full clauses joined by ", and" / ", so". Candidates only: a list whose last item
    # starts with "the" also matches, so every hit needs a read.
    ("spliced-clauses", re.compile(
        r",\s+(?:and|so)\s+(?:(?:I|you|we|they|he|she|it|there)\s+\w+"
        r"|(?:the|this|that|these|those)\s+(?:\w+\s+){0,3}?(?:is|are|was|were|has|have|had|"
        r"will|would|can|could|may|might|must|should|do|does|did|\w+s|\w+ed))\b")),
    ("hedge-as-profundity", re.compile(
        r"\b(?:one game|a single game|no single (?:game|number)) (?:cannot|can't|does not|doesn't) "
        r"(?:test|prove|settle|tell)\b", re.I)),
]

# A colon late in a line, followed by a short verdict-like clause and nothing else.
COLON_APHORISM = re.compile(r"[a-z]{3,}[^.;!?]{8,}?:\s+(?:a|an|the|you|it|they|we|that|no|every)\b[^.:;!?\d]{5,60}\.\s*$", re.I)

VERBS = set("""is are was were be been being am has have had do does did will would can could
should may might must shall won lost beat tie tied scored held ran run came come went go goes
took take takes gave give gives made make makes sits sit sat begin begins began carry carries
carried left leave leaves finished finish stands stand stood stayed stay played play plays
means meant shows show showed looks look looked ended end ends started start starts kept keep
needs need needed puts put gets get got say says said includes include included covers cover
covered adds add added rose fell drew draw counts count counted allow allows allowed reached
reach requires require required produces produce produced moves move moved tells tell told
happens happen happened works work worked matters matter mattered depends depend applies apply
let lets turn turns use uses used call calls track tracks watch watches build builds find finds
expect expects treat treats read reads write writes know knows think thinks see sees""".split())


def sentences(text):
    for s in re.split(r"(?<=[.!?])\s+", text):
        s = s.strip()
        if s:
            yield s


def scan(path, check_fragments=False, allow_em_dash=False):
    hits = []
    try:
        raw = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError as exc:
        print(f"cannot read {path}: {exc}", file=sys.stderr)
        return hits

    for n, line in enumerate(raw, 1):
        if SKIP_LINE.match(line):
            continue
        text = html.unescape(TAG.sub(" ", line))
        text = " ".join(text.split())
        if len(text) < 12:
            continue
        skip_prose = bool(SKIP_ALL.search(line) or HEADING.search(line))
        for name, pattern in CHECKS:
            if allow_em_dash and name == "em-dash":
                continue
            if skip_prose and name != "em-dash":
                continue
            m = pattern.search(line if name == "em-dash" else text)
            # A negated verb ("does not see", "hasn't recorded") is a statement of
            # limits, which is the opposite of the pattern being hunted.
            if m and not re.search(r"\b(?:not|n't|never|cannot)\b", m.group(0), re.I):
                hits.append((n, name, text[:180]))
        if not skip_prose and COLON_APHORISM.search(text):
            hits.append((n, "colon-aphorism?", text[:180]))
        if check_fragments and not skip_prose:
            for s in sentences(text):
                words = s.split()
                if not 2 <= len(words) <= 12 or s.endswith(":"):
                    continue
                if any(re.sub(r"[^a-z]", "", w.lower()) in VERBS for w in words):
                    continue
                hits.append((n, "fragment?", s))
    return hits


def main():
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--help" in flags or "-h" in sys.argv[1:]:
        print(__doc__.strip())
        return 0
    check_fragments = "--fragments" in flags
    allow_em_dash = "--allow-em-dash" in flags
    if not args:
        print(__doc__.strip())
        return 2
    total = 0
    for path in args:
        hits = scan(path, check_fragments, allow_em_dash)
        if not hits:
            continue
        print(f"\n{path}")
        for n, name, text in hits:
            print(f"  {n:>5}  {name:<22} {text}")
        total += len(hits)
    print(f"\n{total} candidate(s). Each needs judgment; the scanner cannot see an aphorism.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
