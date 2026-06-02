"""Regression tests for update_repo.py."""

from pathlib import Path
import unittest

from update_repo import (
    build_zsh_snippet,
    extract_section,
    generate_outputs,
    render_zsh_template_for_docs,
)
from utils.constants import SectionMarker
from utils.file_utils import read_text


class ExtractSectionTests(unittest.TestCase):
    def test_default_behavior_includes_start_and_excludes_end(self) -> None:
        lines = ["before\n", "# start\n", "body\n", "# end\n", "after\n"]
        markers = SectionMarker(start_marker="# start", end_marker="# end")

        self.assertEqual(
            extract_section(lines, markers, source_label="test"),
            ["# start\n", "body\n"],
        )

    def test_can_exclude_start_and_include_end(self) -> None:
        lines = ["# start\n", "body\n", "# end\n"]
        markers = SectionMarker(start_marker="# start", end_marker="# end")

        self.assertEqual(
            extract_section(
                lines,
                markers,
                include_start=False,
                include_end=True,
                source_label="test",
            ),
            ["body\n", "# end\n"],
        )

    def test_missing_required_marker_raises(self) -> None:
        markers = SectionMarker(start_marker="# start", end_marker="# end")

        with self.assertRaisesRegex(ValueError, "start marker not found"):
            extract_section(["body\n"], markers, source_label="test")

    def test_missing_optional_marker_returns_empty_list(self) -> None:
        markers = SectionMarker(start_marker="# start", end_marker="# end")

        self.assertEqual(
            extract_section(["body\n"], markers, required=False, source_label="test"),
            [],
        )


class ChezmoiRenderingTests(unittest.TestCase):
    def test_gui_block_with_else_uses_else_branch(self) -> None:
        lines = [
            "before\n",
            "{{ if $data.isGUIEnvironment -}}\n",
            "gui\n",
            "{{- else -}}\n",
            "server\n",
            "{{- end }}\n",
            "after\n",
        ]

        self.assertEqual(
            render_zsh_template_for_docs(lines, source_label="test"),
            ["before\n", "server\n", "after\n"],
        )

    def test_gui_block_without_else_keeps_body(self) -> None:
        lines = [
            "before\n",
            "{{ if $data.isGUIEnvironment -}}\n",
            "gui-only-line\n",
            "{{- end }}\n",
            "after\n",
        ]

        self.assertEqual(
            render_zsh_template_for_docs(lines, source_label="test"),
            ["before\n", "gui-only-line\n", "after\n"],
        )

    def test_standalone_template_directive_is_dropped(self) -> None:
        lines = ["{{ $data := (include \".precomputed_data.json\" | fromJson) -}}\n", "body\n"]

        self.assertEqual(
            render_zsh_template_for_docs(lines, source_label="test"),
            ["body\n"],
        )

    def test_unknown_if_directive_raises(self) -> None:
        lines = ["{{ if $data.someOtherCondition -}}\n", "body\n", "{{- end }}\n"]

        with self.assertRaisesRegex(ValueError, "unsupported chezmoi if directive"):
            render_zsh_template_for_docs(lines, source_label="test")


class ZshSnippetTests(unittest.TestCase):
    def test_snippet_wraps_extracted_sections(self) -> None:
        rendered_lines = [
            "####[ Aliases ]################################################################\n",
            "alias python=\"python3\"\n",
            "####[ Environmental Variables ]###############################################\n",
            "# Modifies the colors of files and directories in the terminal.\n",
            "export LS_COLORS=\"di=34\"\n",
            "## Set default editor.\n",
        ]

        snippet = build_zsh_snippet(rendered_lines, source_label="test")

        self.assertIn("# --8<-- [start:user_config]\n", snippet)
        self.assertIn("alias python=\"python3\"\n", snippet)
        self.assertNotIn("####[ Environmental Variables ]", snippet)
        self.assertIn("# --8<-- [start:ls_colors]\n", snippet)
        self.assertIn("zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}\n", snippet)
        self.assertNotIn("## Set default editor.", snippet)


class GeneratedOutputRegressionTests(unittest.TestCase):
    def test_generated_outputs_match_checked_in_files(self) -> None:
        for generated_file in generate_outputs():
            with self.subTest(destination=generated_file.destination):
                self.assertTrue(Path(generated_file.destination).exists())
                self.assertEqual(read_text(generated_file.destination), generated_file.content)


if __name__ == "__main__":
    unittest.main()
