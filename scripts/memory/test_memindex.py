#!/usr/bin/env python3
"""Tests for memindex.py."""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import memindex  # noqa: E402


def doc(name, kind="lookup", applies="[fo4-mod]", verified="2999-01-01", body="Body."):
    return (f"---\nname: {name}\ndescription: About {name}.\napplies-to: {applies}\n"
            f"kind: {kind}\nverified: {verified}\n---\n{body}\n")


class MemIndex(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.memory = Path(tmp.name) / "memory"
        self.project = Path(tmp.name) / "proj"
        (self.memory / "fo4-mod").mkdir(parents=True)
        (self.project / "docs").mkdir(parents=True)
        (self.project / "CLAUDE.md").write_text("# p\n\ntypes: [fo4-mod]\n")

    def write(self, filename, text):
        (self.memory / "fo4-mod" / filename).write_text(text)

    def run_it(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = memindex.main([*args, "--memory", str(self.memory)])
        return code, out.getvalue()

    def test_lists_gotchas_and_lookups_without_bodies(self):
        self.write("g.md", doc("g", "gotcha", body="SECRETBODY"))
        self.write("l.md", doc("l"))
        (self.project / "README.md").write_text("r")
        (self.project / "docs" / "s.md").write_text("s")
        (self.project / "docs" / "decisions.md").write_text("d")
        code, out = self.run_it(str(self.project))
        self.assertEqual(code, 0, out)
        self.assertLess(out.index("g.md"), out.index("## Lookups"))
        self.assertGreater(out.index("l.md"), out.index("## Lookups"))
        self.assertIn("README.md", out)
        self.assertIn("listed: " + str(self.project.resolve() / "docs" / "s.md"), out)
        self.assertEqual(out.count("decisions.md"), 1)
        self.assertIn("read: " + str(self.project.resolve() / "docs" / "decisions.md"), out)
        self.assertNotIn("SECRETBODY", out)

    def test_problems_fail_but_valid_docs_still_list(self):
        self.write("good.md", doc("good"))
        self.write("bare.md", "no frontmatter")
        self.write("wrong.md", doc("other"))
        self.write("typo.md", doc("typo", applies="[fo4mod]"))
        self.write("date.md", doc("date", verified="yesterday"))
        self.write("long.md", doc("long", "gotcha", body="x\n" * 61))
        self.write("huge.md", doc("huge", body="x" * 20001))
        code, out = self.run_it("--type", "fo4-mod")
        self.assertEqual(code, 1)
        self.assertIn("good.md", out)
        for text in ("no frontmatter", "does not match", "unknown or empty",
                     "not YYYY-MM-DD", "gotcha too long", "lookup too long"):
            self.assertIn(text, out)

    def test_limit_is_inclusive(self):
        self.write("edge.md", doc("edge", "gotcha", body="\n".join("x" * 1 for _ in range(60))))
        self.assertEqual(self.run_it("--check")[0], 0)

    def test_duplicate_name(self):
        self.write("a.md", doc("a"))
        (self.memory / "a.md").write_text(doc("a"))
        code, out = self.run_it("--check")
        self.assertEqual(code, 1)
        self.assertIn("duplicate name", out)

    def test_stale_is_marked_not_failed(self):
        self.write("old.md", doc("old", verified="2000-01-01"))
        code, out = self.run_it("--type", "fo4-mod")
        self.assertEqual(code, 0)
        self.assertIn("STALE", out)

    def test_missing_header_and_memory(self):
        (self.project / "CLAUDE.md").write_text("# nothing\n")
        code, out = self.run_it(str(self.project))
        self.assertEqual(code, 1)
        self.assertIn("no 'types:", out)
        self.memory = self.memory / "absent"
        self.assertEqual(self.run_it("--check")[0], 1)


if __name__ == "__main__":
    unittest.main()
