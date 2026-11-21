#!/usr/bin/env python3
"""Build a slide deck from its cited markdown outline.

The outline (.md) is the source of truth: slide titles, bullets, key lines and
speaker notes are parsed from it, so the deck and outline cannot drift apart.
Needs python-pptx (pip install python-pptx pillow).

Usage:
    build_deck.py [outline] [--out deck.pptx] [--overlay local.md] [--no-basics] [--standalone]

With no arguments it builds 1-understand/ai-lunch-and-learn.pptx.

Outline conventions:
    *Layout: name*        under a slide heading picks a layout (see LAYOUTS); default "standard".
    Generic layouts: title, three, standard, discussion, reading. ladder, data and tree hard-code
    the lunch-and-learn deck's captions and tiles; use them only there.
    ## Slide N · Basics · …   a basics slide: dropped by --no-basics, tagged "Basics".
    ## Slide N · Series · …   a series recap: dropped by --standalone, tagged "Recap".

Overlay (private, never committed to this repo):
    ## After slide N · Title   inserts a local slide after outline slide N (same body format).
    ## Notes for slide N       appends its lines to slide N's notes, prefixed "Local: ".
    Overlays carry no citations; local slides get the footer "Local example".
"""
import argparse
import os
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN, MSO_AUTO_SIZE
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.xmlchemy import OxmlElement
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt, Emu



def style_run(run, spec):
    font = run.font
    if spec.get("size"):
        font.size = Pt(spec["size"])
    if spec.get("bold") is not None:
        font.bold = spec["bold"]
    if spec.get("italic") is not None:
        font.italic = spec["italic"]
    if spec.get("font"):
        font.name = spec["font"]
    if spec.get("color"):
        font.color.rgb = RGBColor.from_string(spec["color"])
    if spec.get("link"):
        run.hyperlink.address = spec["link"]


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "1-understand", "ai-lunch-and-learn.md")

FONT = "Arial"
DARK = "1F2937"
ACCENT = "1D4ED8"
ACCENT_DARK = "1E3A8A"
TINT = "E8EEFB"
GREY = "6B7280"
LIGHT = "F1F5F9"
W, H = 13.333, 7.5
CITE = re.compile(r"\s*\[(\d+)\]")
LAYOUT = re.compile(r"^\*Layout:\s*([\w-]+)\s*\*\s*$", re.M)
PREFIX = re.compile(r"^(Basics|Series) · (.+)$")
SESSION = re.compile(r"^(Subtitle:\s*)Session \d+ of \d+:\s*(\S)")
LOCAL_LABEL = "Local example"
TAGS = {"basics": "Basics", "series": "Recap"}

# Footer labels for particular slides, keyed by (outline path relative to the repo, outline slide number).
FOOTER_LABELS = {
    ("1-understand/ai-lunch-and-learn.md", 15):
        "Suggestions for us, not findings from the sources \u00b7 links to the handbook in the outline",
}

LINK_NAMES = {}
SOURCE_COUNT = 0
OUTLINE_NAME = "1-understand/ai-lunch-and-learn.md"


# ---------------------------------------------------------------- parsing
def slide_body(sec):
    """Bullets, key line, notes and layout from one slide section."""
    on = re.search(r"\*\*On the slide\*\*\n(.*?)(?=\n\*\*|\Z)", sec, re.S)
    bullets = [l[2:].strip() for l in on.group(1).splitlines() if l.startswith("- ")] if on else []
    key = re.search(r"^\*\*Key line:\*\* (.+)$", sec, re.M)
    notes = re.search(r"\*\*Speaker notes\*\*\n(.*?)(?=\n---|\n\*\*|\Z)", sec, re.S)
    nl = [l.strip() for l in notes.group(1).splitlines()
          if l.strip() and not LAYOUT.match(l.strip())] if notes else []
    layout = LAYOUT.search(sec)
    return dict(bullets=bullets, key=key.group(1).strip() if key else None, notes=nl,
                layout=layout.group(1) if layout else "standard")


def parse(md):
    body = md.split("\n## Related")[0]
    slides = []
    for m in re.finditer(r"^## Slide (\d+) · (.+?)\n(.*?)(?=^## |\Z)", body, re.S | re.M):
        n, title, sec = int(m.group(1)), m.group(2).strip(), m.group(3)
        s = dict(n=n, title=title, basics=False, series=False, **slide_body(sec))
        pre = PREFIX.match(title)
        if pre:
            s[pre.group(1).lower()] = True
            s["title"] = pre.group(2).strip()
        if s["layout"] not in LAYOUTS:
            raise SystemExit(f"unknown layout '{s['layout']}' on slide {n}")
        if s["layout"] == "discussion" and not s["bullets"]:
            raise SystemExit(f"discussion layout needs a bullet on slide {n}")
        slides.append(s)
    return slides


def parse_overlay(md):
    """Return ({N: [slides to insert after N]}, {N: [extra note lines for N]})."""
    inserts, notes = {}, {}
    for m in re.finditer(r"^(## .*?)\n(.*?)(?=^## |\Z)", md + "\n", re.S | re.M):
        head, sec = m.group(1).strip(), m.group(2)
        after = re.match(r"^## After slide (\d+) · (.+)$", head)
        extra = re.match(r"^## Notes for slide (\d+)$", head)
        if after:
            n = int(after.group(1))
            s = dict(n=None, title=after.group(2).strip(), basics=False, series=False,
                     **slide_body(sec))
            if s["layout"] not in LAYOUTS:
                raise SystemExit(f"overlay: unknown layout '{s['layout']}' after slide {n}")
            if s["layout"] == "discussion" and not s["bullets"]:
                raise SystemExit(f"overlay: discussion layout needs a bullet after slide {n}")
            inserts.setdefault(n, []).append(s)
        elif extra:
            lines = [l.strip() for l in sec.splitlines() if l.strip() and l.strip() != "---"]
            notes.setdefault(int(extra.group(1)), []).extend(
                l[2:].strip() if l.startswith("- ") else l for l in lines)
        else:
            raise SystemExit(f"overlay: unrecognised heading '{head}'")
    return inserts, notes


def apply_overlay(slides, inserts, notes, outline_name):
    """Insert local slides and append local note lines, anchored on the outline's slide numbers."""
    known = {s["n"] for s in slides}
    for n in sorted(set(inserts) | set(notes)):
        if n not in known:
            raise SystemExit(f"overlay: no slide {n} in {outline_name}")
        texts = list(notes.get(n, []))
        for s in inserts.get(n, []):
            texts += [s["title"], *s["bullets"], s["key"] or "", *s["notes"]]
        if any(CITE.search(t) for t in texts):
            raise SystemExit(f"overlay: no citations in local material (slide {n})")
    out = []
    for s in slides:
        s = dict(s)
        if s["n"] in notes:
            s["notes"] = s["notes"] + [f"Local: {l}" for l in notes[s["n"]]]
        out.append(s)
        out += [dict(i, local=True) for i in inserts.get(s["n"], [])]
    return out


def select(slides, no_basics, standalone):
    """Drop basics and/or series slides, then renumber from 1.

    Overlay note lines on a dropped slide go with it, so each loss is reported on stderr.
    """
    keep = []
    for s in slides:
        flag = ("--no-basics" if no_basics and s["basics"] else
                "--standalone" if standalone and s["series"] else None)
        if not flag:
            keep.append(s)
            continue
        lost = sum(1 for l in s["notes"] if l.startswith("Local: "))
        if lost:
            print(f"warning: {flag} drops outline slide {s['n']} and its {lost} local note "
                  f"line{'' if lost == 1 else 's'}", file=sys.stderr)
    out = []
    for i, s in enumerate(keep, 1):
        s = dict(s, n=i)
        if standalone and s["layout"] == "title":
            s["bullets"] = [SESSION.sub(lambda m: m.group(1) + m.group(2).upper(), b)
                            for b in s["bullets"]]
        out.append(s)
    return out


def cites(*texts):
    ids = []
    for t in texts:
        for i in CITE.findall(t or ""):
            if int(i) not in ids:
                ids.append(int(i))
    return ids


def smart(s):
    s = CITE.sub("", s).strip()
    s = s.replace("*", "")
    out, open_q = [], True
    for ch in s:
        if ch == '"':
            out.append("\u201c" if open_q else "\u201d")
            open_q = not open_q
        else:
            out.append(ch)
    s = "".join(out)
    s = re.sub(r"(?<=\w)'", "\u2019", s)
    s = re.sub(r"'(?=\w)", "\u2018", s)
    return s.replace("'", "\u2019")


def notes_text(lines):
    def link(m):
        k = m.group(1)
        return LINK_NAMES.get(k, k.split("/")[-1].replace("-", " "))
    txt = " ".join(lines)
    txt = re.sub(r"\[\[([^\]|]+)\]\]", link, txt)
    txt = re.sub(r"\[([^\]]+)\]\((?:https?://|\.\./|[\w-]+\.md)[^)]*\)", r"\1", txt)
    return txt.replace("*", "")


# ---------------------------------------------------------------- drawing
def textbox(slide, left, top, width, height, anchor=MSO_ANCHOR.TOP, margin=0.05):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    return tb, tf


def add_par(tf, text, size, color=DARK, bold=False, italic=False, first=False,
            align=PP_ALIGN.LEFT, space_after=0, runs=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    if space_after:
        p.space_after = Pt(space_after)
    for txt, extra in (runs or [(text, {})]):
        r = p.add_run()
        r.text = txt
        spec = {"size": size, "color": color, "bold": bold, "italic": italic, "font": FONT}
        spec.update(extra)
        style_run(r, spec)
    return p


def bulletise(p, indent=0.42, color=ACCENT):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(Emu(Inches(indent))))
    pPr.set("indent", str(-Emu(Inches(indent))))
    clr = pPr.makeelement(qn("a:buClr"), {})
    srgb = clr.makeelement(qn("a:srgbClr"), {"val": color})
    clr.append(srgb)
    font = pPr.makeelement(qn("a:buFont"), {"typeface": FONT})
    char = pPr.makeelement(qn("a:buChar"), {"char": "\u2022"})
    for el in (clr, font, char):
        pPr.append(el)


def rect(slide, left, top, width, height, fill, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(left), Inches(top), Inches(width), Inches(height))
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor.from_string(fill)
    s.line.fill.background()
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = 0.12
    tf = s.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    for side in ("left", "right"):
        setattr(tf, f"margin_{side}", Inches(0.18))
    for side in ("top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(0.06))
    return s, tf


def title(slide, text, size=34):
    _, tf = textbox(slide, 0.6, 0.2, 12.1, 1.3, anchor=MSO_ANCHOR.BOTTOM)
    add_par(tf, smart(text), size, DARK, bold=True, first=True)
    rect(slide, 0.6, 1.58, 1.3, 0.08, ACCENT)


def footer(slide, n, ids, total, label=None, color=GREY):
    _, tf = textbox(slide, 0.6, 6.98, 10.8, 0.36, anchor=MSO_ANCHOR.MIDDLE)
    if label is None:
        refs = " ".join(f"[{i}]" for i in sorted(ids))
        label = f"Sources {refs} \u00b7 full list and links in the outline" if ids else ""
    add_par(tf, label, 12, color, first=True)
    _, tf = textbox(slide, 11.6, 6.98, 1.13, 0.36, anchor=MSO_ANCHOR.MIDDLE)
    add_par(tf, f"{n} / {total}", 12, color, first=True, align=PP_ALIGN.RIGHT)


def slide_footer(slide, s, ids, total, label=None, color=GREY):
    """The footer, with local slides labelled as local and carrying no sources."""
    if s.get("local"):
        ids, label = [], LOCAL_LABEL
    footer(slide, s["n"], ids, total, label, color)


def corner_tag(slide, text):
    _, tf = textbox(slide, 10.73, 0.12, 2.0, 0.36, anchor=MSO_ANCHOR.TOP)
    add_par(tf, text, 14, GREY, first=True, align=PP_ALIGN.RIGHT)


def key_band(slide, text, top=None, height=None, size=22):
    long = len(smart(text)) > 80
    top = top if top is not None else (5.72 if long else 5.92)
    height = height if height is not None else (1.02 if long else 0.82)
    _, tf = rect(slide, 0.6, top, 12.13, height, TINT, MSO_SHAPE.ROUNDED_RECTANGLE)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    add_par(tf, smart(text), size, ACCENT_DARK, bold=True, first=True)


def bullets_box(slide, items, top=1.9, height=3.9, size=24, left=0.6, width=12.13, gap=14):
    _, tf = textbox(slide, left, top, width, height)
    for i, b in enumerate(items):
        p = add_par(tf, smart(b), size, DARK, first=(i == 0), space_after=gap)
        bulletise(p)
    return tf


def set_notes(slide, lines):
    slide.notes_slide.notes_text_frame.text = notes_text(lines)


# ---------------------------------------------------------------- slides
def s_title(prs, s, total):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = RGBColor.from_string("0F172A")
    rect(sl, 0.8, 2.15, 1.6, 0.1, "60A5FA")
    _, tf = textbox(sl, 0.8, 2.4, 11.7, 1.9, anchor=MSO_ANCHOR.TOP)
    words = smart(s["title"]).split(" ")
    add_par(tf, " ".join(words[:-2]), 50, "FFFFFF", bold=True, first=True)
    add_par(tf, " ".join(words[-2:]), 50, "FFFFFF", bold=True)
    subs = [b.split(":", 1)[1].strip() for b in s["bullets"] if b.startswith("Subtitle:")]
    _, tf = textbox(sl, 0.8, 4.35, 11.7, 1.6)
    for i, t in enumerate(subs):
        add_par(tf, smart(t), 26 if i == 0 else 22, "CBD5E1" if i == 0 else "94A3B8",
                first=(i == 0), space_after=10)
    ids = cites(*s["notes"])
    slide_footer(sl, s, ids, total, color="94A3B8")
    set_notes(sl, s["notes"])


def s_three(prs, s, total):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    title(sl, s["title"])
    for i, b in enumerate(s["bullets"]):
        top = 2.0 + i * 1.55
        o, tf = rect(sl, 0.6, top + 0.12, 0.95, 0.95, ACCENT, MSO_SHAPE.OVAL)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        add_par(tf, str(i + 1), 32, "FFFFFF", bold=True, first=True, align=PP_ALIGN.CENTER)
        head, rest = CITE.sub("", b).split(":", 1)
        _, tf = textbox(sl, 1.85, top, 10.9, 1.3, anchor=MSO_ANCHOR.MIDDLE)
        add_par(tf, smart(head), 30, DARK, bold=True, first=True, space_after=4)
        add_par(tf, smart(rest.strip()[0].upper() + rest.strip()[1:]), 24, GREY)
    slide_footer(sl, s, cites(*s["bullets"], *s["notes"]), total)
    set_notes(sl, s["notes"])


def s_standard(prs, s, total):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    title(sl, s["title"])
    long_key = s["key"] and len(smart(s["key"])) > 80
    bullets_box(sl, s["bullets"], height=(3.7 if long_key else 3.9) if s["key"] else 4.8)
    if s["key"]:
        key_band(sl, s["key"])
    ids = cites(*s["bullets"], s["key"] or "", *s["notes"])
    slide_footer(sl, s, ids, total, s.get("label"))
    set_notes(sl, s["notes"])


def s_ladder(prs, s, total):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    title(sl, s["title"])
    rungs = [b for b in s["bullets"] if re.match(r"L\d ·", b)]
    other = [b for b in s["bullets"] if not re.match(r"L\d ·", b)]
    fills = ["BFDBFE", "93C5FD", "3B82F6", "1D4ED8"]
    txtc = [ACCENT_DARK, ACCENT_DARK, "FFFFFF", "FFFFFF"]
    for i, r in enumerate(rungs):
        lvl, txt = [x.strip() for x in CITE.sub("", r).split("·", 1)]
        left, top = 0.6 + i * 3.08, 4.55 - i * 0.78
        _, tf = rect(sl, left, top, 2.95, 1.3, fills[i], MSO_SHAPE.ROUNDED_RECTANGLE)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        add_par(tf, lvl, 28, txtc[i], bold=True, first=True)
        add_par(tf, smart(txt), 18, txtc[i])
    _, tf = textbox(sl, 0.6, 1.9, 5.9, 1.95)
    for i, b in enumerate(other):
        add_par(tf, smart(b), 22, DARK, bold=True, first=(i == 0), space_after=8)
    add_par(tf, "L1\u2013L3: Meta\u2019s on-call agent \u00b7 L4: Factory\u2019s workstreams", 16, GREY)
    key_band(sl, s["key"], top=6.0, height=0.78)
    slide_footer(sl, s, cites(*s["bullets"], s["key"] or "", *s["notes"]), total)
    set_notes(sl, s["notes"])


def s_data(prs, s, total):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    title(sl, s["title"])
    tiles = [("+44%", "lines of code (not significant)"), ("+36%", "pull requests"),
             ("Only +14%", "resolved issues (borderline)"), ("+56%", "time to review approval")]
    for i, (big, small) in enumerate(tiles):
        left = 0.6 + i * 3.08
        _, tf = rect(sl, left, 1.9, 2.95, 1.55, LIGHT if i < 2 else TINT, MSO_SHAPE.ROUNDED_RECTANGLE)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        add_par(tf, big, 36 if len(big) < 8 else 24, ACCENT_DARK, bold=True, first=True,
                align=PP_ALIGN.CENTER)
        add_par(tf, small, 18, DARK, align=PP_ALIGN.CENTER)
    _, tf = textbox(sl, 0.6, 3.5, 12.13, 0.4)
    add_par(tf, "Harvard study of 655 firms (Chen & Stratton, Nov 2026 revision), coding agents vs before adoption",
            16, GREY, italic=True, first=True)
    bullets_box(sl, s["bullets"][2:], top=4.05, height=1.8, size=22, gap=10)
    key_band(sl, s["key"])
    slide_footer(sl, s, cites(*s["bullets"], s["key"] or "", *s["notes"]), total)
    set_notes(sl, s["notes"])


def s_tree(prs, s, total):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    _, tf = textbox(sl, 0.6, 0.35, 7.0, 1.15, anchor=MSO_ANCHOR.BOTTOM)
    add_par(tf, smart(s["title"]), 34, DARK, bold=True, first=True)
    _, tf = textbox(sl, 7.4, 0.35, 5.33, 1.15, anchor=MSO_ANCHOR.BOTTOM)
    add_par(tf, "Run it per task or step. Go down the list until a question sends you out.",
            16, GREY, italic=True, first=True, align=PP_ALIGN.RIGHT)
    rect(sl, 0.6, 1.58, 1.3, 0.08, ACCENT)
    rows = [b for b in s["bullets"] if re.match(r"\d ·", b)]
    then = [b for b in s["bullets"] if b.startswith("Then")][0]
    top = 1.8
    for i, r in enumerate(rows):
        q, outs = [x.strip() for x in CITE.sub("", r).split("|", 1)]
        h = 0.58 if i < 5 else 0.9
        _, tf = rect(sl, 0.6, top, 5.8, h, ACCENT, MSO_SHAPE.ROUNDED_RECTANGLE)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        add_par(tf, smart(q), 22, "FFFFFF", bold=True, first=True)
        _, tf = rect(sl, 6.55, top, 6.18, h, LIGHT, MSO_SHAPE.ROUNDED_RECTANGLE)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        for j, o in enumerate(outs.split(" / ")):
            ans, res = [x.strip() for x in o.split("\u2192", 1)]
            add_par(tf, "", 20 if i < 5 else 18, first=(j == 0),
                    runs=[(ans + " \u2192 ", {"bold": True, "color": ACCENT}), (smart(res), {})])
        top += h + 0.1
    head, rest = CITE.sub("", then).split("|", 1)
    _, tf = rect(sl, 0.6, top + 0.02, 12.13, 0.78, TINT, MSO_SHAPE.ROUNDED_RECTANGLE)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    add_par(tf, "", 19, ACCENT_DARK, first=True,
            runs=[(head.strip() + " ", {"bold": True}), (smart(rest.strip()), {})])
    slide_footer(sl, s, cites(*s["bullets"], *s["notes"]), total)
    set_notes(sl, s["notes"])


def s_reading(prs, s, total):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    title(sl, s["title"])
    bullets_box(sl, s["bullets"], height=4.9, size=24, gap=16)
    slide_footer(sl, s, cites(*s["bullets"], *s["notes"]), total,
                 label=f"All {SOURCE_COUNT} sources, with links, are listed in the outline: "
                       f"{OUTLINE_NAME}")
    set_notes(sl, s["notes"])


def s_discussion(prs, s, total):
    """One large question (the first bullet) with open space under it for the room's answers."""
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    title(sl, s["title"])
    _, tf = textbox(sl, 0.6, 1.95, 12.13, 1.75)
    add_par(tf, smart(s["bullets"][0]), 36, ACCENT_DARK, bold=True, first=True)
    if s["key"]:
        key_band(sl, s["key"])
    # Cite only what is shown: the question, the key line and the notes, not the hidden bullets.
    slide_footer(sl, s, cites(s["bullets"][0], s["key"] or "", *s["notes"]), total)
    set_notes(sl, s["notes"])


LAYOUTS = {
    "title": s_title, "three": s_three, "ladder": s_ladder, "data": s_data,
    "tree": s_tree, "reading": s_reading, "standard": s_standard, "discussion": s_discussion,
}


def rel_name(path):
    """The path relative to the repo root, or just the file name if it lies outside the repo."""
    rel = os.path.relpath(os.path.abspath(path), ROOT)
    return os.path.basename(path) if rel.startswith("..") else rel.replace(os.sep, "/")


def inside_repo(path):
    """True if path, existing or not, lies inside the repo.

    Compares by file identity, not spelling, so a differently cased path on a
    case-insensitive disk is still caught: it checks every existing ancestor of
    the resolved path against ROOT with os.path.samefile.
    """
    d = os.path.realpath(path)
    while True:
        try:
            if os.path.samefile(d, ROOT):
                return True
        except OSError:
            pass  # this ancestor doesn't exist (yet); keep walking up
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent


def register_notes_master(prs):
    """List the notes master in presentation.xml, which python-pptx forgets to do.

    python-pptx adds the notes master part and its relationship when the first speaker note is
    written, but never adds <p:notesMasterIdLst>. PowerPoint and Google Slides tolerate that;
    Keynote and Quick Look refuse to open the file. See python-pptx issue #1051 / PR #1128.
    """
    pres = prs.part._element
    if pres.find(qn("p:notesMasterIdLst")) is not None:
        return
    rid = next((r.rId for r in prs.part.rels.values() if r.reltype == RT.NOTES_MASTER), None)
    if rid is None:
        return
    lst = OxmlElement("p:notesMasterIdLst")
    entry = OxmlElement("p:notesMasterId")
    entry.set(qn("r:id"), rid)
    lst.append(entry)
    pres.find(qn("p:sldMasterIdLst")).addnext(lst)


def main(argv=None):
    global SOURCE_COUNT, OUTLINE_NAME
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("outline", nargs="?", default=MD, help="outline .md (default: the lunch-and-learn deck)")
    ap.add_argument("--out", help="output .pptx (default: the outline path with .pptx; "
                                  "required with --overlay, and must then be outside this repo)")
    ap.add_argument("--overlay", help="private overlay .md with local slides and notes")
    ap.add_argument("--no-basics", action="store_true", help="drop the 'Basics ·' slides")
    ap.add_argument("--standalone", action="store_true",
                    help="drop the 'Series ·' slides and the 'Session N of M: ' subtitle prefix")
    args = ap.parse_args(argv)
    if args.overlay:
        # A deck with local content must never land in (or overwrite a deck in) the public repo.
        if not args.out:
            raise SystemExit("overlay: --out is required and must be outside the handbook repo")
        if inside_repo(args.out):
            raise SystemExit("overlay: --out must be outside the handbook repo")
    out = args.out or os.path.splitext(args.outline)[0] + ".pptx"
    OUTLINE_NAME = rel_name(args.outline)

    with open(args.outline, encoding="utf-8") as f:
        _md = f.read()
    SOURCE_COUNT = len(re.findall(r"^\[\d+\] ", _md.split("\n## Sources", 1)[-1], re.M))
    slides = parse(_md)
    for s in slides:
        s["label"] = FOOTER_LABELS.get((OUTLINE_NAME, s["n"]))
    if args.overlay:
        with open(args.overlay, encoding="utf-8") as f:
            inserts, extra = parse_overlay(f.read())
        slides = apply_overlay(slides, inserts, extra, OUTLINE_NAME)
    slides = select(slides, args.no_basics, args.standalone)

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    total = len(slides)
    for s in slides:
        LAYOUTS[s["layout"]](prs, s, total)
        for flag, tag in TAGS.items():
            if s[flag]:
                corner_tag(prs.slides[-1], tag)
    prs.core_properties.title = slides[0]["title"]
    prs.core_properties.author = ""
    register_notes_master(prs)
    prs.save(out)
    print({"ok": True, "output": out, "slides": total})
    return 0


if __name__ == "__main__":
    sys.exit(main())
