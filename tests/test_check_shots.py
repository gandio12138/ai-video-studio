import json
import tempfile
import unittest
from pathlib import Path
from tools.check_shots import validate

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "examples" / "watch_note"


class ShotChecks(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((EX / "shots.json").read_text(encoding="utf-8"))
        self.assets = json.loads((EX / "assets.json").read_text(encoding="utf-8"))

    def check(self):
        return validate(self.doc, self.assets, EX)

    def test_valid_example(self):
        errors, warnings, summary = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(summary["total_duration_s"], 30)
        self.assertEqual(summary["shot_count"], 6)
        self.assertTrue(any("计划素材" in w for w in warnings))

    def test_duplicate_shot_id(self):
        self.doc["shots"][1]["shot_id"] = self.doc["shots"][0]["shot_id"]
        self.assertTrue(any("重复镜号" in e for e in self.check()[0]))

    def test_missing_field(self):
        del self.doc["shots"][0]["action"]
        self.assertTrue(any("缺字段" in e for e in self.check()[0]))

    def test_unknown_asset(self):
        self.doc["shots"][0]["asset_ids"].append("P999")
        self.assertTrue(any("未登记素材" in e for e in self.check()[0]))

    def test_negative_duration(self):
        self.doc["shots"][0]["edit_duration_s"] = -1
        self.assertTrue(any("edit_duration_s" in e for e in self.check()[0]))

    def test_boolean_duration(self):
        self.doc["shots"][0]["edit_duration_s"] = True
        self.assertTrue(any("edit_duration_s" in e for e in self.check()[0]))

    def test_nan_duration(self):
        self.doc["shots"][0]["edit_duration_s"] = float("nan")
        self.assertTrue(any("edit_duration_s" in e for e in self.check()[0]))

    def test_total_mismatch(self):
        self.doc["target_duration_s"] = 60
        self.assertTrue(any("采用总时长" in e for e in self.check()[0]))

    def test_generated_without_file(self):
        self.assets["assets"][0]["status"] = "generated"
        self.assertTrue(any("没有真实 path" in e for e in self.check()[0]))

    def test_path_escape(self):
        self.assets["assets"][0]["path"] = "../../AGENTS.md"
        self.assertTrue(any("超出项目" in e for e in self.check()[0]))

    def test_audio_warning(self):
        self.doc["shots"][1]["recorded_audio_duration_s"] = 12
        self.assertTrue(any("实测声音" in w for w in self.check()[1]))

    def test_empty_template(self):
        self.doc["shots"] = []
        self.assertTrue(any("非空列表" in e for e in self.check()[0]))

    def test_approved_with_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / "ref.txt").write_text("test reference existence only", encoding="utf-8")
            self.assets["assets"][0]["status"] = "approved"
            self.assets["assets"][0]["path"] = "ref.txt"
            errors, _, _ = validate(self.doc, self.assets, Path(folder))
            self.assertEqual(errors, [])

    def test_unhashable_enum(self):
        self.doc["shots"][0]["framing"] = []
        self.doc["status"] = []
        self.assertTrue(self.check()[0])

    def test_invalid_asset_status(self):
        self.assets["assets"][0]["status"] = []
        self.assertTrue(self.check()[0])

    def test_invalid_top_level(self):
        errors, _, _ = validate([], self.assets, EX)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
