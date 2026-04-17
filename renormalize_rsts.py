#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-shot and reusable normalization for FLASH docs_flash/rst/*.rst

Fixes Word-export glitches: unbalanced ** / *, bullet+link indentation, and
path-like ***VI.vi*** star runs. Aligns with plain RST style used in docs/*.rst.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def sanitize_word_rst_markup(s: str) -> str:
    """Fix common Word→RST bold glitches."""
    if not s:
        return s
    # "**Label: **rest" -> "**Label:** rest"
    s = re.sub(r"\*\*([^*\n]+?):\s*\*\*(\s*)", r"**\1:**\2", s)
    # "****2023 Q****3**" -> "**2023 Q3**"
    for _ in range(16):
        s2 = re.sub(r"\*\*\*\*([^*]+?)\*\*\*\*([^*]+?)\*\*", r"**\1\2**", s)
        if s2 == s:
            break
        s = s2
    # Word split: "**** *" at end of a bold run
    s = re.sub(r"\*\*\*\*\s+\*", "** ", s)
    # Path segments: extra stars before ".vi***"
    s = re.sub(r"([A-Za-z0-9\)\]])\*{4,}(\.vi\*\*\*)", r"\1\2", s)
    # Collapse absurd star runs (keep docutils from choking)
    for _ in range(24):
        if "******" not in s:
            break
        s = s.replace("******", "**")
    while "****" in s and s.count("*") > 12:
        s = s.replace("****", "**", 1)
    # Known mangled emphasis: *S**hut **D**own** Msg* -> *Shutdown Msg*
    s = re.sub(
        r"\*S\*\*hut \*\*D\*\*own\*\* Msg\*",
        r"*Shutdown Msg*",
        s,
    )
    return s


def collapse_path_star_runs(s: str) -> str:
    """Normalize ***path*** / ***path.vi*** style lines with duplicated ** segments."""
    # "<Sync Device>/******Shut Down" style
    s = re.sub(r"(/[A-Za-z <>\*]+)\*{4,}(Shut Down)", r"\1\2", s)
    # "AutomationContext******/******Compile" -> single slash between starred parts
    s = re.sub(r"(\*{3}[A-Za-z][^*\n]*?)\*{4,}/\*{4,}", r"\1**/**", s)
    s = re.sub(r"(\*{3}<[^>\n]+>[^*\n]*?)\*{4,}/\*{4,}", r"\1**/**", s)
    # "<******Sync Device******>" -> "<Sync Device>"
    s = re.sub(r"<(\*{4,})([^*<>\n]+?)(\*{4,})>", r"<\2>", s)
    # Remaining "/******Word" -> "/Word" inside angle paths
    s = re.sub(r"/\*{4,}([A-Za-z][A-Za-z ]{0,40}?)(\*{4,})", r"/\1", s)
    return s


def fix_bullet_link_continuations(content: str) -> str:
    """
    Indent bare `` `https...`_ `` lines that follow a bullet so the list item does not break.
    """
    lines = content.splitlines()
    n = len(lines)
    i = 0
    while i < n:
        cur = lines[i]
        m = re.match(r"^(\s*)- (.*)$", cur)
        if not m:
            i += 1
            continue
        base = m.group(1)
        j = i + 1
        while j < n:
            nxt = lines[j]
            if not nxt.strip():
                break
            if re.match(rf"^{re.escape(base)}- ", nxt):
                break
            st = nxt.strip()
            is_link_only = st.startswith("`http") or (
                st.startswith("http") and "`_" in st
            )
            if is_link_only:
                if not nxt.startswith(base + "  "):
                    lines[j] = base + "  " + nxt.lstrip()
                j += 1
                continue
            break
        i += 1
    sep = "\n" if content.endswith("\n") else ""
    return "\n".join(lines) + sep


def normalize_rst_text(content: str) -> str:
    lines_out = []
    for line in content.splitlines():
        line = sanitize_word_rst_markup(line)
        line = collapse_path_star_runs(line)
        lines_out.append(line)
    text = "\n".join(lines_out)
    if content.endswith("\n") and not text.endswith("\n"):
        text += "\n"
    elif not content.endswith("\n") and text.endswith("\n"):
        text = text.rstrip("\n")
    return fix_bullet_link_continuations(text)


def main() -> int:
    root = Path(__file__).resolve().parent
    rst_dir = root / "docs_flash" / "rst"
    if not rst_dir.is_dir():
        print("docs_flash/rst not found", file=sys.stderr)
        return 1
    for path in sorted(rst_dir.glob("*.rst")):
        raw = path.read_text(encoding="utf-8")
        new = normalize_rst_text(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            print("updated", path.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())