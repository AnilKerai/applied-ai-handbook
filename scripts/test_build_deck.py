#!/usr/bin/env python3
"""Tests for build_deck.py.

Run from the repo root:
    uv run --with python-pptx --with pillow python -m unittest scripts/test_build_deck.py -v
"""
import contextlib
import io
import os
import re
import sys
import tempfile
import unittest

from pptx import Presentation
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_deck as bd  # noqa: E402

ROOT = os.path.dirname(HERE)
LUNCH_PPTX = os.path.join(ROOT, "1-understand", "ai-lunch-and-learn.pptx")
PAGE = re.compile(r"^\d+ / \d+$")

# A four-slide talk: a title slide, a Series recap, a Basics slide and a content slide.
TALK = """---
title: Building AI features
---

# Building AI features

Intro paragraph.

---

## Slide 1 · Building AI features

*Layout: title*

**On the slide**

- Subtitle: Session 2 of 2: the model is one part
- Subtitle: November 2026

**Speaker notes**

Opening note.[1]

---

## Slide 2 · Series · What did you turn into a check?

*Layout: discussion*

**On the slide**

- What did you turn into a check this week?
- A second bullet the layout ignores

**Speaker notes**

Ask the room for one example.

---

## Slide 3 · Basics · What an agent is

**On the slide**

- A model, some tools and a loop [1]

**Key line:** An agent is a loop.

**Speaker notes**

Basics note.[1]

---

## Slide 4 · Evals gate production

**On the slide**

- Build evals from real cases [1]

**Key line:** No evals, no launch.

**Speaker notes**

Evals note.[1]

---

## Related

- Nothing

**Read next:** nothing

## Sources

[1] https://example.com/a — Example source
"""

READING = """# Reading talk

## Slide 1 · Further reading

*Layout: reading*

**On the slide**

- The outline that goes with this deck [1]

**Speaker notes**

Read the outline.[1]

---

## Related

**Read next:** nothing

## Sources

[1] https://example.com/a — Example source
[2] https://example.com/b — Another source
"""


def frames(slide):
    """Every text frame's text on a slide, in shape order."""
    return [sh.text_frame.text for sh in slide.shapes if sh.has_text_frame]


def paras(slide):
    """Every paragraph's text on a slide, across all text frames."""
    return [p.text for sh in slide.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs]


def notes(slide):
    return slide.notes_slide.notes_text_frame.text


def pages(prs):
    """The page-number footer of each slide, e.g. '2 / 4'."""
    return [[t for t in frames(sl) if PAGE.match(t)][0] for sl in prs.slides]


def run_main(argv):
    """build_deck.main, with its one-line progress print kept out of the test output."""
    with contextlib.redirect_stdout(io.StringIO()):
        return bd.main(argv)


def shape_with_text(slide, text):
    hits = [sh for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text == text]
    return hits[0] if hits else None


class BuildDeckTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = tmp.name

    def write(self, name, text):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def build(self, *flags, outline_text=TALK, overlay_text=None, out_name="out.pptx"):
        outline = self.write("talk.md", outline_text)
        out = os.path.join(self.tmp, out_name)
        argv = [outline, "--out", out, *flags]
        if overlay_text is not None:
            argv += ["--overlay", self.write("talk.local.md", overlay_text)]
        self.assertEqual(run_main(argv), 0)
        return Presentation(out)

    def assertFails(self, message, *flags, outline_text=TALK, overlay_text=None):
        out = os.path.join(self.tmp, "failed.pptx")
        with self.assertRaises(SystemExit) as cm:
            self.build(*flags, outline_text=outline_text, overlay_text=overlay_text,
                       out_name="failed.pptx")
        self.assertEqual(str(cm.exception), message)
        self.assertFalse(os.path.exists(out), "a failed build must write no pptx")

    # ------------------------------------------------------------ regression
    def test_regression_lunch_and_learn(self):
        out = os.path.join(self.tmp, "lunch.pptx")
        self.assertEqual(run_main(["--out", out]), 0)
        built, committed = Presentation(out), Presentation(LUNCH_PPTX)
        self.assertEqual(len(built.slides), 16)
        self.assertEqual(len(committed.slides), 16)
        for i, (b, c) in enumerate(zip(built.slides, committed.slides), 1):
            with self.subTest(slide=i):
                self.assertEqual(frames(b), frames(c))
                self.assertEqual(notes(b), notes(c))
                geom = lambda sl: [(sh.left, sh.top, sh.width, sh.height) for sh in sl.shapes]
                self.assertEqual(geom(b), geom(c))

    def test_lunch_data_tiles_keep_hedges(self):
        """The Harvard tiles on slide 13 keep the paper's caveats: lines not significant, issues borderline."""
        out = os.path.join(self.tmp, "lunch.pptx")
        self.assertEqual(run_main(["--out", out]), 0)
        for prs in (Presentation(out), Presentation(LUNCH_PPTX)):
            tiles = frames(prs.slides[12])
            self.assertIn("+44%\nlines of code (not significant)", tiles)
            self.assertIn("Only +14%\nresolved issues (borderline)", tiles)

    # ------------------------------------------------------------ layouts
    def test_layout_hint(self):
        prs = self.build()
        discussion = prs.slides[1]
        q = shape_with_text(discussion, "What did you turn into a check this week?")
        self.assertIsNotNone(q, "the first bullet should be the question, alone in its frame")
        size = q.text_frame.paragraphs[0].runs[0].font.size
        self.assertGreaterEqual(size, Pt(32), "the question should be large")
        self.assertNotIn("A second bullet the layout ignores", "\n".join(frames(discussion)))

        bad = TALK.replace("## Slide 3 · Basics · What an agent is\n",
                           "## Slide 3 · Basics · What an agent is\n\n*Layout: bogus*\n")
        self.assertFails("unknown layout 'bogus' on slide 3", outline_text=bad)

    def test_discussion_footer_cites_shown_bullet_only(self):
        talk = (TALK.replace("- What did you turn into a check this week?\n",
                             "- What did you turn into a check this week? [1]\n")
                    .replace("- A second bullet the layout ignores\n",
                             "- A second bullet the layout ignores [2]\n")
                    .replace("Ask the room for one example.\n", "Ask the room for one example.[3]\n"))
        prs = self.build(outline_text=talk)
        self.assertIn("Sources [1] [3] \u00b7 full list and links in the outline",
                      frames(prs.slides[1]))

    def test_discussion_without_bullet_fails(self):
        no_bullets = TALK.replace("**On the slide**\n\n- What did you turn into a check this week?\n"
                                  "- A second bullet the layout ignores\n\n", "")
        self.assertNotEqual(no_bullets, TALK)
        self.assertFails("discussion layout needs a bullet on slide 2", outline_text=no_bullets)
        self.assertFails("overlay: discussion layout needs a bullet after slide 4",
                         overlay_text="## After slide 4 · Local question\n\n*Layout: discussion*\n\n"
                                      "**Speaker notes**\n\nA local note.\n")

    def test_prefixes_dropped_and_corner_tags(self):
        prs = self.build()
        for idx, title, tag in [(1, "What did you turn into a check?", "Recap"),
                                (2, "What an agent is", "Basics")]:
            sl = prs.slides[idx]
            with self.subTest(slide=idx + 1):
                self.assertIn(title, frames(sl))
                self.assertFalse(any(("Series ·" in t or "Basics ·" in t) for t in frames(sl)))
                corner = shape_with_text(sl, tag)
                self.assertIsNotNone(corner)
                run = corner.text_frame.paragraphs[0].runs[0]
                self.assertLessEqual(run.font.size, Pt(16))
                self.assertEqual(str(run.font.color.rgb), bd.GREY)
                self.assertGreater(corner.left, Inches(bd.W / 2))
                self.assertLess(corner.top, Inches(1))
        self.assertFalse({"Basics", "Recap"} & set(frames(prs.slides[3])))

    def test_reading_footer_names_outline(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as inside:
            outline = os.path.join(inside, "talk.md")
            with open(outline, "w", encoding="utf-8") as f:
                f.write(READING)
            out = os.path.join(self.tmp, "reading.pptx")
            self.assertEqual(run_main([outline, "--out", out]), 0)
            rel = os.path.basename(inside) + "/talk.md"
            self.assertIn(f"All 2 sources, with links, are listed in the outline: {rel}",
                          frames(Presentation(out).slides[0]))
        # Outside the repo, only the file name appears: no local paths in a deck.
        prs = self.build(outline_text=READING)
        self.assertIn("All 2 sources, with links, are listed in the outline: talk.md",
                      frames(prs.slides[0]))

    # ------------------------------------------------------------ variants
    def test_no_basics_and_standalone(self):
        def titles(prs):
            return [frames(sl) for sl in prs.slides]

        full = self.build()
        self.assertEqual(pages(full), ["1 / 4", "2 / 4", "3 / 4", "4 / 4"])
        self.assertIn("Session 2 of 2: the model is one part", paras(full.slides[0]))

        nb = self.build("--no-basics")
        self.assertEqual(pages(nb), ["1 / 3", "2 / 3", "3 / 3"])
        self.assertIn("What did you turn into a check?", frames(nb.slides[1]))
        self.assertIn("Evals gate production", frames(nb.slides[2]))
        self.assertIn("Session 2 of 2: the model is one part", paras(nb.slides[0]))

        sa = self.build("--standalone")
        self.assertEqual(pages(sa), ["1 / 3", "2 / 3", "3 / 3"])
        self.assertIn("What an agent is", frames(sa.slides[1]))
        self.assertIn("Evals gate production", frames(sa.slides[2]))
        self.assertIn("The model is one part", paras(sa.slides[0]))
        self.assertNotIn("Session 2 of 2", "\n".join(sum(titles(sa), [])))

        both = self.build("--no-basics", "--standalone")
        self.assertEqual(pages(both), ["1 / 2", "2 / 2"])
        self.assertIn("Evals gate production", frames(both.slides[1]))

    # ------------------------------------------------------------ overlays
    def test_overlay_notes_and_insert(self):
        overlay = """# Local overlay

## After slide 3 · How we check it here

**On the slide**

- Our pipeline runs evals on every merge

**Key line:** Local key line.

**Speaker notes**

A local story.

---

## Notes for slide 3

- First local line.
Second local line.
"""
        prs = self.build(overlay_text=overlay)
        self.assertEqual(len(prs.slides), 5)
        self.assertEqual(pages(prs), ["1 / 5", "2 / 5", "3 / 5", "4 / 5", "5 / 5"])
        anchor, local, after = prs.slides[2], prs.slides[3], prs.slides[4]
        self.assertIn("What an agent is", frames(anchor))
        self.assertTrue(notes(anchor).endswith("Local: First local line. Local: Second local line."),
                        notes(anchor))
        self.assertTrue(notes(anchor).startswith("Basics note."))
        self.assertIn("How we check it here", frames(local))
        self.assertIn("Local example", frames(local))
        self.assertFalse(any("Sources" in t for t in frames(local)))
        self.assertEqual(notes(local), "A local story.")
        self.assertIn("Evals gate production", frames(after))

    def test_overlay_unknown_slide_fails(self):
        for overlay in ["## Notes for slide 9\n\n- A line.\n",
                        "## After slide 9 · Local\n\n**On the slide**\n\n- A bullet\n"]:
            with self.subTest(overlay=overlay.splitlines()[0]):
                self.assertFails("overlay: no slide 9 in talk.md", overlay_text=overlay)

    def test_overlay_unrecognised_heading_fails(self):
        self.assertFails("overlay: unrecognised heading '## After Slide 3 · Local'",
                         overlay_text="## After Slide 3 · Local\n\n- A bullet\n")

    def test_insert_survives_dropped_anchor(self):
        overlay = "## After slide 3 · Local thing\n\n**On the slide**\n\n- A local bullet\n"
        prs = self.build("--no-basics", overlay_text=overlay)
        self.assertEqual(pages(prs), ["1 / 4", "2 / 4", "3 / 4", "4 / 4"])
        self.assertIn("What did you turn into a check?", frames(prs.slides[1]))
        self.assertIn("Local thing", frames(prs.slides[2]))
        self.assertIn("Local example", frames(prs.slides[2]))
        self.assertIn("Evals gate production", frames(prs.slides[3]))

    def test_dropped_slide_warns_about_local_notes(self):
        overlay = "## Notes for slide 3\n\n- One local line.\n- Another.\n\n## Notes for slide 2\n\n- A recap line.\n"
        no_basics = "warning: --no-basics drops outline slide 3 and its 2 local note lines\n"
        standalone = "warning: --standalone drops outline slide 2 and its 1 local note line\n"
        for flags, warning, count in [((), "", 4),
                                      (("--no-basics",), no_basics, 3),
                                      (("--standalone",), standalone, 3),
                                      (("--no-basics", "--standalone"), standalone + no_basics, 2)]:
            with self.subTest(flags=flags):
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    prs = self.build(*flags, overlay_text=overlay)
                self.assertEqual(err.getvalue(), warning)
                self.assertEqual(len(prs.slides), count, "the build still succeeds")

    def overlay_paths(self):
        return (self.write("talk.md", TALK),
                self.write("talk.local.md", "## Notes for slide 4\n\n- A local line.\n"))

    def pptx_in(self, folder):
        return [f for f in os.listdir(folder) if f.endswith(".pptx")]

    def test_overlay_without_out_fails(self):
        outline, overlay = self.overlay_paths()
        with self.assertRaises(SystemExit) as cm:
            run_main([outline, "--overlay", overlay])
        self.assertEqual(str(cm.exception),
                         "overlay: --out is required and must be outside the handbook repo")
        self.assertEqual(self.pptx_in(self.tmp), [], "a failed build must write no pptx")
        # Without an overlay, the default output (the outline path with .pptx) still applies.
        self.assertEqual(run_main([outline]), 0)
        self.assertEqual(self.pptx_in(self.tmp), ["talk.pptx"])

    def test_overlay_out_inside_repo_fails(self):
        outline, overlay = self.overlay_paths()
        with tempfile.TemporaryDirectory(dir=ROOT) as inside:
            target = os.path.join(inside, "talk.pptx")
            for out in [target, os.path.relpath(target)]:
                with self.subTest(out=out):
                    with self.assertRaises(SystemExit) as cm:
                        run_main([outline, "--out", out, "--overlay", overlay])
                    self.assertEqual(str(cm.exception),
                                     "overlay: --out must be outside the handbook repo")
                    self.assertEqual(self.pptx_in(inside), [], "a failed build must write no pptx")
            self.assertEqual(self.pptx_in(self.tmp), [])

    @unittest.skipUnless(os.path.exists(ROOT.swapcase()), "case-sensitive file system")
    def test_overlay_out_case_variant_fails(self):
        outline, overlay = self.overlay_paths()
        out = os.path.join(ROOT.swapcase(), "probe.pptx")
        with self.assertRaises(SystemExit) as cm:
            run_main([outline, "--out", out, "--overlay", overlay])
        self.assertEqual(str(cm.exception), "overlay: --out must be outside the handbook repo")
        self.assertFalse(os.path.exists(os.path.join(ROOT, "probe.pptx")))

    def test_overlay_citation_fails(self):
        for overlay in ["## Notes for slide 4\n\n- A cited line.[1]\n",
                        "## After slide 4 · Local\n\n**On the slide**\n\n- A cited bullet [2]\n"]:
            with self.subTest(overlay=overlay.splitlines()[0]):
                self.assertFails("overlay: no citations in local material (slide 4)",
                                 overlay_text=overlay)


if __name__ == "__main__":
    unittest.main()
