"""Offline document/reference contracts; no agent, media or aesthetic execution."""
import hashlib
import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples/cinematic_look"


class CinematicLookContracts(unittest.TestCase):
    def test_route_table_resolves_current_project_paths(self):
        body = (ROOT / "CINEMATIC_LOOK.md").read_text()
        routes = {}
        for row in body.splitlines():
            if row.startswith("| prompts/"):
                cells = [cell.strip() for cell in row.strip("|").split("|")]
                routes[cells[0]] = cells[1:]
                self.assertTrue((ROOT / cells[0]).is_file(), cells[0])
        expected_full = {"prompts/entry_novel_direct.md", "prompts/entry_original_script.md",
                         "prompts/complete_visual_pack.md"}
        self.assertTrue(expected_full.issubset(routes))
        for path in expected_full:
            self.assertTrue(routes[path][0].startswith("full_pack"), path)
            self.assertTrue(routes[path][1].startswith("optional"), path)
        self.assertTrue(routes["prompts/rebuild_cinematic_visuals.md"][0].startswith("calibrate_only"))
        self.assertEqual(routes["prompts/complete_design_sheets.md"][1], "explicitly_requested")

    def test_full_entry_declarations_and_conditional_board_boundary(self):
        for name in ("entry_novel_direct", "entry_original_script", "complete_visual_pack"):
            with self.subTest(entry=name):
                body = (ROOT / f"prompts/{name}.md").read_text()
                declarations = dict(re.findall(r"^(look_mode|visual_scope|asset_sheet_mode): (\S+)$",
                                               body, re.M))
                self.assertEqual(declarations, {"look_mode": "cinematic_live_action",
                    "visual_scope": "full_pack", "asset_sheet_mode": "optional"})
                primary, optional = body.split("【可选设定板与单图交付：仅用户显式要求时启用】", 1)
                self.assertNotRegex(primary, r"本轮必须写完整整板|两个入口都交角色/场景设定板|并继续下方设定板")
                self.assertIn("整板探索提示词", optional)
                # This checks declared scope only, not what a model would actually output.

    def test_current_instruction_references_do_not_use_missing_package_aliases(self):
        paths = [ROOT / p for p in ("AGENTS.md", "WORKFLOW_ENTRYPOINTS.md",
                                   "VISUAL_PRODUCTION.md", "CHATGPT_PROJECT_INSTRUCTIONS.md")]
        paths += list((ROOT / ".agents/skills").glob("*/SKILL.md"))
        paths += [ROOT / f"prompts/{p}.md" for p in ("entry_novel_direct", "entry_original_script",
            "complete_visual_pack", "complete_design_sheets", "rebuild_cinematic_visuals")]
        for path in paths:
            body = path.read_text()
            self.assertNotIn("ASSET_SHEETS.md", body, path)
            self.assertNotIn("prompts/asset_reference_sheets.md", body, path)
            for target in re.findall(r"\b(?:CINEMATIC_LOOK\.md|templates/cinematic_image_prompt\.md|prompts/rebuild_cinematic_visuals\.md)\b", body):
                self.assertTrue((ROOT / target).is_file(), (path, target))

    def test_reference_frame_bytes_dimensions_and_safe_paths(self):
        manifest = json.loads((EXAMPLES / "reference_manifest.json").read_text())
        frames = manifest["frames"]
        self.assertEqual(len(frames), 8)
        self.assertEqual(len({f["path"] for f in frames}), 8)
        for frame in frames:
            path = (EXAMPLES / frame["path"]).resolve()
            self.assertTrue(path.is_relative_to(EXAMPLES.resolve()))
            data = path.read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), frame["sha256"])
            self.assertEqual(struct.unpack(">II", data[16:24]), (frame["width"], frame["height"]))
            self.assertEqual((frame["width"], frame["height"]), (448, 252))

    def test_reference_roles_are_analysis_not_story_identity(self):
        manifest = json.loads((EXAMPLES / "reference_manifest.json").read_text())
        self.assertEqual(manifest["reference_status"], "user_supplied_look_analysis_not_story_asset")
        self.assertEqual({f["role"] for f in manifest["frames"]}, {"look_analysis_only"})
        self.assertFalse(manifest["audio_reviewed"])
        self.assertFalse(manifest["ocr_used"])
        self.assertEqual(manifest["enhancement"], "none")

    def test_look_settings_are_not_injected_into_runtime_or_provider_contracts(self):
        forbidden = {"look_mode", "visual_scope", "asset_sheet_mode", "look_status"}
        def keys(value):
            if isinstance(value, dict):
                for k, v in value.items():
                    yield k
                    yield from keys(v)
            elif isinstance(value, list):
                for v in value:
                    yield from keys(v)
        for relative in ("config/runtime.json", "config/providers.json",
                         "templates/image_job.json", "templates/video_job.json"):
            value = json.loads((ROOT / relative).read_text())
            self.assertFalse(forbidden.intersection(keys(value)), relative)

    def test_cinematic_teaching_prompts_are_complete_separate_examples(self):
        body = (EXAMPLES / "detailed_prompts.md").read_text()
        example_ids = re.findall(r"^## (EX\d+)｜", body, re.M)
        self.assertEqual(len(example_ids), 6)
        self.assertEqual(len(set(example_ids)), 6)
        prompts = re.findall(r"^### 可复制正文[^\n]*\n(.*?)(?=^### 验收\s*$)",
                             body, re.S | re.M)
        self.assertEqual(len(prompts), 6)
        for prompt in prompts:
            self.assertNotRegex(prompt, r"\[填写|\{.*?待填|服装同上")
            self.assertGreater(len(prompt), 120)


if __name__ == "__main__":
    unittest.main()
