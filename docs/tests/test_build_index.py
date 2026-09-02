"""Regression tests for workshop assets in the static-site index."""

import importlib.util
import json
import pathlib
import tempfile
import unittest
from html import unescape


ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("build_index", ROOT / "docs" / "build_index.py")
build_index = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_index)


class WorkshopBuildTests(unittest.TestCase):
    def test_collect_workshops_exports_notebook_as_readable_html(self):
        """Missing notebook export would leave the website with a dead reader link."""
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            workshop = root / "Work-Shop" / "01-demo"
            workshop.mkdir(parents=True)
            notebook = {
                "nbformat": 4,
                "nbformat_minor": 5,
                "metadata": {},
                "cells": [
                    {"cell_type": "markdown", "metadata": {}, "source": ["# Hello workshop\n", "Useful notes."]},
                    {"cell_type": "code", "metadata": {}, "execution_count": 1,
                     "source": ["print('hello')"],
                     "outputs": [{"output_type": "stream", "name": "stdout", "text": "hello\n"}]},
                ],
            }
            (workshop / "lesson.ipynb").write_text(json.dumps(notebook), encoding="utf-8")

            workshops = build_index.collect_workshops(str(root), str(root / "docs"))

            self.assertEqual(workshops[0]["id"], "01-demo")
            self.assertEqual(workshops[0]["notebooks"][0]["path"], "Work-Shop/01-demo/lesson.ipynb")
            exported = root / "docs" / workshops[0]["notebooks"][0]["html"]
            self.assertTrue(exported.is_file())
            html = unescape(exported.read_text(encoding="utf-8"))
            self.assertIn("Hello workshop", html)
            self.assertIn("hello", html)
            self.assertIn('class="gutter"', html)
            self.assertIn('class="tok-bi">print</span>', html)
            self.assertIn('class="tok-str">&#x27;hello&#x27;</span>', exported.read_text(encoding="utf-8"))

    def test_collect_workshops_indexes_nested_code_and_images_as_resources(self):
        """Skipping nested workshop assets would hide the Pygame starter material."""
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            workshop = root / "Work-Shop" / "01-demo"
            assets = workshop / "source" / "sprites"
            assets.mkdir(parents=True)
            (workshop / "starter.py").write_text("print('ready')\n", encoding="utf-8")
            (assets / "hero.jpg").write_bytes(b"\xff\xd8\xff\xd9")

            resources = build_index.collect_workshops(str(root), str(root / "docs"))[0]["resources"]

            self.assertEqual(
                resources,
                [
                    {"name": "starter.py", "path": "Work-Shop/01-demo/starter.py", "kind": "code",
                     "size": 15, "text": "print('ready')\n"},
                    {"name": "source/sprites/hero.jpg", "path": "Work-Shop/01-demo/source/sprites/hero.jpg",
                     "kind": "image", "size": 4},
                ],
            )


if __name__ == "__main__":
    unittest.main()
