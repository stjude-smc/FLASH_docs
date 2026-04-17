# -*- coding: utf-8 -*-
"""
Shared helpers to convert Word .docx files into reStructuredText for docs_flash.

Splits on Heading 1 (configurable). Section underlines follow the reference docs style:
  level 1: =  level 2: -  level 3: +  level 4+: ^ " ~
"""
from __future__ import annotations

import json
import re
import shutil
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator, Iterator, List, Optional, Sequence, Set, Tuple, Union

from docx import Document as open_docx_document
from docx.document import Document as DocumentClass
from docx.oxml.ns import qn
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from docx.text.run import Run

# --- RST underline characters by relative depth within a split file (0 = page title) ---
RST_CHARS = ("=", "-", "+", "^", '"', "~")

# Relationship type for external hyperlinks in OOXML
HYPERLINK_NS = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
)


def slugify(text: str, prefix: str = "") -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "_", s)
    s = s.strip("_") or "section"
    if prefix:
        return f"{prefix}__{s}"
    return s


def rst_escape_inline(text: str) -> str:
    """Escape characters that break inline RST."""
    if not text:
        return ""
    # Backticks and backslashes first
    text = text.replace("\\", "\\\\")
    text = text.replace("`", "\\`")
    return text


def rst_section(title: str, depth: int) -> List[str]:
    """Return title + underline lines (no trailing blank). depth 0 = top of page."""
    t = title.rstrip()
    char = RST_CHARS[min(depth, len(RST_CHARS) - 1)]
    line = char * max(len(t), 3)
    return [t, line, ""]


def iter_block_items(parent: Any) -> Generator[Union[Paragraph, Table], None, None]:
    """Yield paragraphs and tables in document order."""
    if isinstance(parent, DocumentClass):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("parent must be document or cell")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def style_to_heading_level(style_name: Optional[str]) -> Optional[int]:
    """
    Map Word paragraph style to heading level (1..9), or 0 for Title, or None for body.
    """
    if not style_name:
        return None
    sn = style_name.strip()
    if sn == "Title":
        return 0
    m = re.match(r"Heading\s*(\d+)$", sn, re.I)
    if m:
        return int(m.group(1))
    # Subtitle sometimes used like H2
    if sn == "Subtitle":
        return 2
    return None


def paragraph_outline_level(paragraph: Paragraph) -> Optional[int]:
    """OOXML outline level (0-based) -> 1-based heading level."""
    p_pr = paragraph._p.pPr
    if p_pr is None or p_pr.outlineLvl is None:
        return None
    try:
        return int(p_pr.outlineLvl.val) + 1
    except (TypeError, ValueError, AttributeError):
        return None


def effective_heading_level(paragraph: Paragraph) -> Optional[int]:
    """Prefer named style; fall back to outline level."""
    st = paragraph.style.name if paragraph.style else None
    hl = style_to_heading_level(st)
    if hl is not None:
        return hl
    return paragraph_outline_level(paragraph)


def _hyperlink_url(part: Any, r_id: Optional[str]) -> Optional[str]:
    if not r_id:
        return None
    rel = part.rels.get(r_id)
    if rel is None:
        return None
    if rel.reltype == HYPERLINK_NS:
        return rel.target_ref
    return None


def _runs_to_inline(
    element: Any,
    part: Any,
    bold: bool = False,
    italic: bool = False,
) -> str:
    """Serialize w:r elements under element to inline RST."""
    chunks: List[str] = []
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    for child in element:
        tag = child.tag
        if tag == qn("w:r"):
            r_text_parts: List[str] = []
            b, i = bold, italic
            for sub in child:
                if sub.tag == qn("w:t"):
                    r_text_parts.append(sub.text or "")
                elif sub.tag == qn("w:tab"):
                    r_text_parts.append("\t")
                elif sub.tag == qn("w:br"):
                    r_text_parts.append("\n")
                elif sub.tag == qn("w:rPr"):
                    for rpr in sub:
                        if rpr.tag == qn("w:b"):
                            b = True
                        if rpr.tag == qn("w:i"):
                            i = True
            raw = "".join(r_text_parts)
            if not raw:
                continue
            esc = rst_escape_inline(raw)
            if b and i:
                out = f"***{esc}***"
            elif b:
                out = f"**{esc}**"
            elif i:
                out = f"*{esc}*"
            else:
                out = esc
            chunks.append(out)
        elif tag == qn("w:hyperlink"):
            rid = child.get(qn("r:id"))
            url = _hyperlink_url(part, rid)
            inner = _runs_to_inline(child, part)
            if url:
                label = inner.strip() or url
                chunks.append(f"`{rst_escape_inline(label)} <{url}>`_")
            else:
                chunks.append(inner)
    return "".join(chunks)


def paragraph_to_inline_rst(paragraph: Paragraph) -> str:
    """Full paragraph inline markup (headings should use .text for title)."""
    return _runs_to_inline(paragraph._p, paragraph.part).strip()


def is_list_paragraph(paragraph: Paragraph) -> bool:
    p = paragraph._p.pPr
    if p is None:
        return False
    return p.numPr is not None


def list_level(paragraph: Paragraph) -> int:
    p = paragraph._p.pPr
    if p is None or p.numPr is None or p.numPr.ilvl is None:
        return 0
    try:
        return int(p.numPr.ilvl.val)
    except (TypeError, ValueError):
        return 0


def is_numbered_list(paragraph: Paragraph) -> bool:
    p = paragraph._p.pPr
    if p is None or p.numPr is None or p.numPr.numId is None:
        return False
    # Heuristic: numbering id present; Word uses abstractNum for bullet vs decimal
    return True


@dataclass
class Block:
    kind: str
    data: Any


@dataclass
class ConversionContext:
    doc_key: str
    docs_flash: Path
    static_rel: Path  # relative to docs_flash, e.g. _static/flash_doc
    image_counter: int = 0
    figure_counter: int = 0

    def next_image_name(self, ext: str = "png") -> str:
        self.image_counter += 1
        return f"img_{self.doc_key}_{self.image_counter:04d}.{ext}"

    def next_figure_name(self) -> str:
        self.figure_counter += 1
        return f"fig-{self.doc_key}-{self.figure_counter}"


def looks_like_figure_caption(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    if re.match(r"^(figure|fig\.)\s", t, re.I):
        return True
    return len(t) < 400


def is_caption_paragraph(paragraph: Paragraph, after_figure: bool) -> bool:
    st = (paragraph.style.name or "").lower()
    if "caption" in st:
        return True
    if after_figure and looks_like_figure_caption(paragraph.text or ""):
        return True
    return False


def paragraph_is_image_only(paragraph: Paragraph, num_images: int) -> bool:
    if num_images == 0:
        return False
    return not (paragraph.text or "").strip()


def emit_figure_rst(
    lines: List[str],
    rel_path: str,
    *,
    caption: Optional[str] = None,
    name: Optional[str] = None,
    alt: Optional[str] = None,
) -> None:
    """Append a .. figure:: block with blank lines before and after."""
    lines.append("")
    lines.append(f".. figure:: {rel_path}")
    if name:
        lines.append(f"   :name: {name}")
    lines.append(f"   :alt: {alt or caption or 'Figure'}")
    if caption:
        lines.append("")
        for cl in caption.strip().split("\n"):
            lines.append(f"   {cl}")
    lines.append("")


def extract_blip_images(
    paragraph: Paragraph,
    ctx: ConversionContext,
    dest_dir: Path,
) -> List[str]:
    """
    Extract drawing images from paragraph; save under dest_dir.
    Returns list of paths relative to docs_flash/rst/ (for .. figure::).
    """
    out: List[str] = []
    docs_flash = ctx.docs_flash
    rst_dir = docs_flash / "rst"
    for run in paragraph.runs:
        el = run._element
        blips = el.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
        for blip in blips:
            embed = blip.get(qn("r:embed"))
            if not embed:
                continue
            part = paragraph.part
            rel = part.rels.get(embed)
            if rel is None:
                continue
            try:
                image_part = part.related_parts[embed]
            except KeyError:
                continue
            blob = image_part.blob
            ctype = getattr(image_part, "content_type", "") or ""
            ext = "png"
            if "jpeg" in ctype or "jpg" in ctype:
                ext = "jpg"
            elif "gif" in ctype:
                ext = "gif"
            elif "wmf" in ctype:
                ext = "wmf"
            name = ctx.next_image_name(ext)
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / name
            dest.write_bytes(blob)
            # rst/ lives under docs_flash; image under docs_flash/_static/...
            rel_from_rst = (Path("..") / dest.relative_to(docs_flash)).as_posix()
            out.append(rel_from_rst)
    return out


def table_to_rst(table: Table) -> str:
    rows: List[List[str]] = []
    for row in table.rows:
        cells = [cell.text.replace("\n", " ").strip() for cell in row.cells]
        rows.append(cells)
    if not rows:
        return ""
    ncols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < ncols:
            r.append("")
    lines: List[str] = ["", ".. list-table::"]
    if len(rows) > 1:
        lines.append("   :header-rows: 1")
    lines.append("")
    header_rows = 1 if len(rows) > 1 else 0
    data_rows = rows[header_rows:]
    if header_rows:
        hdr = rows[0]
        line = f"   * - {rst_escape_inline(hdr[0])}"
        for c in hdr[1:]:
            line += f"\n     - {rst_escape_inline(c)}"
        lines.append(line)
    for row in data_rows:
        line = f"   * - {rst_escape_inline(row[0])}"
        for c in row[1:]:
            line += f"\n     - {rst_escape_inline(c)}"
        lines.append(line)
    lines.append("")
    return "\n".join(lines)


def normalize_heading_stack_for_file(word_level: int, split_level: int) -> int:
    """
    Map Word heading level to RST depth within one split file.
    split_level=1: split on Heading 1. First H1 in file -> depth 0, H2 -> 1, etc.
    """
    if word_level < split_level:
        return 0
    return word_level - split_level


def render_section_blocks(
    blocks: List[Block],
    lines: List[str],
    ctx: ConversionContext,
    static_dir: Path,
    split_level: int,
) -> None:
    """Walk blocks with optional caption peek for figure-only paragraphs."""
    consumed: Set[int] = set()
    i = 0
    n = len(blocks)
    while i < n:
        if i in consumed:
            i += 1
            continue
        b = blocks[i]
        if b.kind == "table":
            lines.append(table_to_rst(b.data))
            i += 1
            continue

        para: Paragraph = b.data
        hl = effective_heading_level(para)

        if hl is not None and hl >= split_level:
            title_text = para.text.strip()
            if title_text:
                d = normalize_heading_stack_for_file(hl, split_level)
                lines.extend(rst_section(title_text, d))
            i += 1
            continue

        imgs = extract_blip_images(para, ctx, static_dir)
        num_imgs = len(imgs)

        caption_after: Optional[str] = None
        if num_imgs and paragraph_is_image_only(para, num_imgs) and i + 1 < n:
            nb = blocks[i + 1]
            if nb.kind == "paragraph":
                np = nb.data
                if effective_heading_level(np) is None and is_caption_paragraph(
                    np, after_figure=True
                ):
                    caption_after = (np.text or "").strip()
                    consumed.add(i + 1)

        for j, rel in enumerate(imgs):
            is_last = j == num_imgs - 1
            cap = caption_after if (is_last and caption_after) else None
            fname = ctx.next_figure_name()
            alt = cap or Path(rel).name
            emit_figure_rst(lines, rel, caption=cap, name=fname, alt=alt)

        if num_imgs and paragraph_is_image_only(para, num_imgs):
            i += 1
            continue

        if is_list_paragraph(para):
            txt = paragraph_to_inline_rst(para) or para.text
            lines.append(f"- {txt}")
            lines.append("")
            i += 1
            continue

        inline = paragraph_to_inline_rst(para)
        if not inline.strip():
            lines.append("")
            i += 1
            continue

        st = (para.style.name or "").lower()
        if "code" in st or "macro" in st:
            lines.append(".. code-block:: text")
            lines.append("")
            for pl in inline.split("\n"):
                lines.append(f"\t{pl}")
            lines.append("")
        else:
            for para_line in inline.split("\n"):
                if para_line.strip():
                    lines.extend(textwrap.wrap(para_line, width=100) or [para_line])
                else:
                    lines.append("")
            lines.append("")
        i += 1


def convert_docx_to_rst_tree(
    docx_path: Path,
    docs_flash: Path,
    doc_key: str,
    *,
    split_level: int = 1,
    doc_title: Optional[str] = None,
    copy_manual_images: Optional[Path] = None,
) -> dict:
    """
    Convert one .docx into multiple .rst files under docs_flash/rst/.

    Returns manifest dict with keys: doc_key, files (list of rst stems), static_prefix.
    """
    docs_flash = docs_flash.resolve()
    docx_path = docx_path.resolve()
    rst_dir = docs_flash / "rst"
    rst_dir.mkdir(parents=True, exist_ok=True)
    static_dir = docs_flash / "_static" / doc_key
    static_dir.mkdir(parents=True, exist_ok=True)

    if copy_manual_images and copy_manual_images.is_dir():
        dest_manual = static_dir / "manual_images"
        if dest_manual.exists():
            shutil.rmtree(dest_manual)
        shutil.copytree(copy_manual_images, dest_manual)

    document = open_docx_document(str(docx_path))

    # Collect blocks with heading boundaries
    sections: List[Tuple[str, List[Block]]] = []
    current_title = "_preamble"
    current_blocks: List[Block] = []

    def flush_section():
        nonlocal current_blocks, current_title
        if current_blocks or current_title != "_preamble":
            sections.append((current_title, list(current_blocks)))
        current_blocks = []

    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            hl = effective_heading_level(block)
            if hl is not None and hl == split_level:
                flush_section()
                current_title = block.text.strip() or "Untitled"
                current_blocks = []
                continue
            if hl == 0 and not sections and not current_blocks:
                current_title = block.text.strip() or "Title"
                continue
            current_blocks.append(Block("paragraph", block))
        elif isinstance(block, Table):
            current_blocks.append(Block("table", block))

    flush_section()

    if not sections:
        sections = [("document", [b for b in iter_blocks_from_doc(document)])]

    # Build RST files per section
    written: List[dict] = []
    for sec_title, blocks in sections:
        if sec_title == "_preamble" and not blocks:
            continue
        stem = slugify(sec_title, doc_key)
        lines: List[str] = []
        ref = slugify(sec_title, doc_key).replace("__", "-")
        lines.append(f".. _{ref}:")
        lines.append("")
        depth0 = 0
        lines.extend(rst_section(sec_title if sec_title != "_preamble" else doc_title or "Section", depth0))

        per_ctx = ConversionContext(
            doc_key=doc_key,
            docs_flash=docs_flash,
            static_rel=Path("_static") / doc_key,
        )
        render_section_blocks(blocks, lines, per_ctx, static_dir, split_level)

        out_path = rst_dir / f"{stem}.rst"
        out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        written.append({"stem": stem, "title": sec_title, "path": f"rst/{stem}.rst"})

    manifest = {
        "doc_key": doc_key,
        "docx": str(docx_path),
        "split_level": split_level,
        "files": written,
        "static_web": f"_static/{doc_key}",
    }
    man_path = docs_flash / f"manifest_{doc_key}.json"
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def iter_blocks_from_doc(document: DocumentClass) -> Iterator[Block]:
    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            yield Block("paragraph", block)
        else:
            yield Block("table", block)


def regenerate_toctree_include(
    docs_flash: Path,
    doc_configs: Sequence[dict],
) -> None:
    """
    Write rst/_toctree_generated.rst with all listed stems (no .rst suffix in toctree).
    doc_configs: list of {"caption": str, "entries": ["stem1", "stem2", ...]}
    """
    rst_dir = docs_flash / "rst"
    rst_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        ".. This file is generated by import_doc*.py — do not edit by hand.",
        "",
    ]
    for cfg in doc_configs:
        cap = cfg.get("caption", "")
        entries = cfg.get("entries", [])
        if cap:
            lines.append(f".. toctree::")
            lines.append(f"   :caption: {cap}")
            lines.append(f"   :maxdepth: 2")
            lines.append("")
        else:
            lines.append(".. toctree::")
            lines.append("   :maxdepth: 2")
            lines.append("")
        for e in entries:
            # Docnames are relative to the Sphinx root (docs_flash/); generated pages live under rst/.
            docname = e if "/" in e else f"rst/{e}"
            lines.append(f"   {docname}")
        lines.append("")
    out = rst_dir / "_toctree_generated.rst"
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def collect_stems_from_manifests(docs_flash: Path, doc_keys: Sequence[str]) -> List[str]:
    stems: List[str] = []
    for dk in doc_keys:
        p = docs_flash / f"manifest_{dk}.json"
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        for f in data.get("files", []):
            stems.append(f["stem"])
    return stems


# Order and captions for the master toctree (used after any import_doc*.py run).
TOCTREE_DOC_ORDER: Sequence[Tuple[str, str]] = (
    ("flash_documentation", "FLASH Documentation"),
    ("flash_development_guide", "FLASH Development Guide"),
    ("ui_window_actor", "Creating a New UI Window Actor"),
)


def regenerate_full_toctree(docs_flash: Path) -> None:
    """Rebuild rst/_toctree_generated.rst from all manifest_*.json files."""
    docs_flash = docs_flash.resolve()
    configs: List[dict] = []
    for doc_key, caption in TOCTREE_DOC_ORDER:
        man = docs_flash / f"manifest_{doc_key}.json"
        if not man.exists():
            continue
        data = json.loads(man.read_text(encoding="utf-8"))
        stems = [f["stem"] for f in data.get("files", [])]
        if stems:
            configs.append({"caption": caption, "entries": stems})
    regenerate_toctree_include(docs_flash, configs)
