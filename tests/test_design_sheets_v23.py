"""Static harness-contract checks only; not image quality or agent execution tests."""
import hashlib
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def text(relative):
    return (ROOT / relative).read_text(encoding="utf-8")

class DesignSheetContracts(unittest.TestCase):
    def test_shared_spec_and_templates_exist(self):
        for name in ("DESIGN_SHEETS.md", "templates/character_sheet.md",
                     "templates/location_sheet.md", "templates/sheet_manifest.md"):
            with self.subTest(name=name):
                self.assertGreater(len(text(name)), 500)

    def test_fifteen_skills_with_matching_names(self):
        skills = list((ROOT / ".agents/skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 15)
        for path in skills:
            body = path.read_text(encoding="utf-8")
            self.assertTrue(body.startswith("---\n"))
            self.assertIn("name: " + path.parent.name, body.split("---", 2)[1])

    def test_agent_reads_sheet_spec(self):
        self.assertIn("DESIGN_SHEETS.md", text("AGENTS.md"))
        self.assertIn("layout_only", text("AGENTS.md"))

    def test_both_entrypoints_preserve_explicit_optional_board_delivery(self):
        for path in ("prompts/entry_novel_direct.md", "prompts/entry_original_script.md"):
            with self.subTest(path=path):
                body = text(path)
                for token in ("DESIGN_SHEETS.md", "整板探索提示词", "俯视布局",
                              "拼版映射", "本轮不实际生成"):
                    self.assertIn(token, body)

    def test_existing_visual_completion_keeps_optional_sheet_branch(self):
        body = text("prompts/complete_visual_pack.md")
        self.assertIn("DESIGN_SHEETS.md", body)
        self.assertIn("【可选设定板与单图交付：仅用户显式要求时启用】", body)

    def test_new_completion_entry_preserves_story_and_plan(self):
        body = text("prompts/complete_design_sheets.md")
        for token in ("不改已确认剧情", "不执行生图", "unconfigured",
                      "整板探索提示词", "每格独立可复制正文"):
            self.assertIn(token, body)

    def test_downstream_skills_reference_spec(self):
        for skill in ("producer", "visual", "prompts", "images", "shots", "video", "audit"):
            with self.subTest(skill=skill):
                self.assertIn("DESIGN_SHEETS.md", text(f".agents/skills/manju-{skill}/SKILL.md"))

    def test_reference_png_dimensions_and_recorded_hash(self):
        path = ROOT / "06_assets/references/layout/character_sheet_layout_user_01.png"
        data = path.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", data[16:24]), (900, 900))
        record = text("04_visual/references/RF_LAYOUT_USER_01.md")
        self.assertIn(hashlib.sha256(data).hexdigest(), record)
        self.assertIn("layout_only", record)
        self.assertIn("不是正式C001", record)

    def test_character_modules_and_optional_state_are_present(self):
        body = text("DESIGN_SHEETS.md")
        for token in ("正面", "90°侧面", "背面", "五种", "四分之三",
                      "至少三类", "not_applicable", "人物自身左右"):
            self.assertIn(token, body)

    def test_location_layout_is_required(self):
        body = text("DESIGN_SHEETS.md")
        for token in ("俯视布局示意", "关键交互区", "世界结构不变",
                      "水平翻转", "文字/坐标"):
            self.assertIn(token, body)

    def test_independent_images_and_no_video_first_frame_rule(self):
        body = text("DESIGN_SHEETS.md")
        for token in ("独立原图", "纯拼版不得重新绘制", "不得默认直接作为图生视频首帧"):
            self.assertIn(token, body)

    def test_manifest_is_not_fake_executable_schema(self):
        body = text("templates/sheet_manifest.md")
        self.assertIn("不是旧image_job或timeline的可执行JSON", body)
        for token in ("unconfigured", "not_generated", "null", "未执行"):
            self.assertIn(token, body)

    def test_examples_have_substantial_prompts_not_placeholders(self):
        body = text("examples/design_sheets/worked_prompts.md")
        prompts = re.findall(r"```text\n(.*?)\n```", body, flags=re.S)
        self.assertEqual(len(prompts), 22)  # 2 boards, 14 unique character tasks (one reused), 6 scene images
        for prompt in prompts:
            self.assertGreater(len(prompt), 120)
            self.assertNotRegex(prompt, r"\[填写|\{.*?待填|服装同上")
        self.assertIn("图路径null", body)

    def test_capabilities_do_not_claim_new_media_backend(self):
        body = text("CAPABILITIES.md")
        self.assertIn("没有新媒体执行代码", body)
        self.assertIn("执行后端未接入", body)

if __name__ == "__main__":
    unittest.main()
