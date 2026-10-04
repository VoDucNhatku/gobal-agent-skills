#!/usr/bin/env python3
"""Compute WCAG 2.2 contrast for token pairs. Never judge contrast by eye.

Three real failures shipped past a careful visual review in one session:
1.34:1 on the border of every interactive control, 3.70:1 and 4.31:1 on
metadata text. All three looked fine on screen. Ratios are arithmetic; a
designer's confidence is not.

Usage
  contrast.py --pair "#eceadf" "#080d1c"
  contrast.py --pair "#6f6152" "#141d38" --need 3.0
  contrast.py --css src/styles/tokens.css --on=--s0,--s1,--s3
      (note the = : a value starting with -- is otherwise read as a flag)
  contrast.py --fix "#6f6152" --on "#141d38,#2e2820" --need 3.0

Thresholds (WCAG 2.2)
  4.5  body text
  3.0  large text (>=24px, or >=19px bold) AND non-text UI boundaries (1.4.11)
"""
import argparse
import re
import sys

# Token names that denote a SURFACE rather than ink laid on one. Used to keep
# the bulk scan from comparing every panel colour against every other one.
GROUND_NAME = re.compile(
    r"(^--s\d|bg|background|ground|surface|panel|field|ink$|canvas|base|paper)", re.I
)


def _lin(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6:
        raise ValueError(f"not a hex colour: {hex_colour}")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def read_tokens(path: str) -> dict:
    """Pull `--name: #hex;` declarations out of a stylesheet."""
    text = open(path, encoding="utf-8").read()
    return {
        m.group(1): m.group(2)
        for m in re.finditer(r"(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\s*;", text)
    }


def suggest(colour: str, grounds: list, need: float, step: int = 2) -> str | None:
    """Walk the colour lighter until it clears `need` against every ground.

    Keeps the hue by moving all three channels together, so a token stays
    recognisably itself instead of turning grey.
    """
    h = colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    for k in range(0, 200, step):
        cand = f"#{min(r + k, 255):02x}{min(g + k, 255):02x}{min(b + k, 255):02x}"
        if all(ratio(cand, ground) >= need for ground in grounds):
            return cand
    for k in range(0, 200, step):
        cand = f"#{max(r - k, 0):02x}{max(g - k, 0):02x}{max(b - k, 0):02x}"
        if all(ratio(cand, ground) >= need for ground in grounds):
            return cand
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pair", nargs=2, metavar=("FG", "BG"))
    ap.add_argument("--css", help="stylesheet to read --tokens from")
    ap.add_argument("--on", help="comma-separated grounds (hex or --token names)")
    ap.add_argument("--fix", metavar="HEX", help="suggest a compliant replacement")
    ap.add_argument("--need", type=float, default=4.5)
    args = ap.parse_args()

    tokens = read_tokens(args.css) if args.css else {}
    resolve = lambda v: tokens.get(v.strip(), v.strip())  # noqa: E731

    if args.pair:
        fg, bg = (resolve(x) for x in args.pair)
        r = ratio(fg, bg)
        ok = r >= args.need
        print(f"{fg} on {bg}: {r:.2f} (need {args.need}) {'PASS' if ok else 'FAIL'}")
        if not ok:
            better = suggest(fg, [bg], args.need)
            if better:
                print(f"  try {better} -> {ratio(better, bg):.2f}")
        return 0 if ok else 1

    if args.fix:
        grounds = [resolve(x) for x in (args.on or "").split(",") if x.strip()]
        if not grounds:
            print("--fix needs --on", file=sys.stderr)
            return 2
        better = suggest(resolve(args.fix), grounds, args.need)
        if not better:
            print("no candidate clears the threshold — rethink the surface, not the ink")
            return 1
        print(f"{args.fix} -> {better}")
        for ground in grounds:
            print(f"   vs {ground}: {ratio(better, ground):.2f}")
        return 0

    if args.css:
        grounds = [resolve(x) for x in (args.on or "").split(",") if x.strip()]
        if not grounds:
            grounds = [v for k, v in tokens.items()
                       if re.search(r"(bg|ground|surface|panel|field|ink|s[0-9])", k)]
        if not grounds:
            print("no grounds found; pass --on", file=sys.stderr)
            return 2

        # Only INK is tested against grounds. Comparing one surface to another
        # surface is meaningless — a panel is not text sitting on the page — and
        # a check that fails 21 of 22 tokens teaches you to ignore it.
        ink = {n: v for n, v in tokens.items()
               if not GROUND_NAME.search(n) and v not in grounds}
        if not ink:
            print("no ink tokens found — name them so they are not read as surfaces")
            return 2

        fails = 0
        for name, value in sorted(ink.items()):
            worst = min(((ratio(value, g), g) for g in grounds), key=lambda t: t[0])
            if worst[0] < args.need:
                fails += 1
                print(f"FAIL {name} ({value}) on {worst[1]}: {worst[0]:.2f} < {args.need}")
                better = suggest(value, grounds, args.need)
                if better:
                    print(f"     try {better}")
        print(f"\n{len(ink)} ink tokens vs {len(grounds)} grounds — "
              f"{fails} below {args.need}")
        return 1 if fails else 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
