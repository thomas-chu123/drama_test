"""多圖首幀的輸入、接線與回收回歸測試；不提交生成。"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import comfyui_edit_adapter as edit
from comfyui_image_adapter import AdapterFailure


class MultiReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        for name in ("one.png", "two.png"):
            (root / name).write_bytes(b"\x89PNG\r\n\x1a\n" + b"fixture")
        self.job = {
            "modality": "image", "prompt": "雙人首幀測試", "project_root": str(root),
            "output_root": str(root / "output"), "outputs": ["test.png"],
            "parameters": {"reference_resolution": 512},
            "reference_bindings": [
                {"role": "reference_image", "order": i, "path": name}
                for i, name in enumerate(("one.png", "two.png"), 1)
            ],
        }

    def test_ordered_images_reach_distinct_encoder_slots(self):
        params, paths = edit.preflight(self.job)
        graph = edit.build(self.job, params, [path.name for path in paths])
        inputs = graph["474"]["inputs"]
        self.assertEqual(inputs["images.image_1"], ["100", 0])
        self.assertEqual(inputs["images.image_2"], ["101", 0])
        self.assertEqual(graph["101"]["inputs"]["image"], "two.png")
        self.assertEqual(inputs["resolution"], 512)

    def test_invalid_inputs_fail_before_submission(self):
        for change in ("role", "order", "path"):
            with self.subTest(change=change):
                binding = self.job["reference_bindings"][1]
                original = dict(binding)
                binding[change] = {"role": "first_frame", "order": 4, "path": "../outside.png"}[change]
                with patch.object(edit, "request_json") as request:
                    with self.assertRaises(AdapterFailure):
                        edit.run(self.job)
                    request.assert_not_called()
                binding.update(original)

    def test_collect_does_not_upload_or_submit(self):
        self.job["collect_provider_job_id"] = "existing-job"
        with patch.object(edit, "get_history", return_value={"status": {"completed": True}}), patch.object(edit, "request_json") as request, patch.object(edit, "upload") as upload:
            with self.assertRaises(AdapterFailure) as caught:
                edit.run(self.job)
            self.assertEqual(caught.exception.request_id, "existing-job")
            self.assertTrue(caught.exception.submitted)
            request.assert_not_called()
            upload.assert_not_called()

    def test_single_image_keeps_original_connection(self):
        graph = edit.build(self.job, {}, "single.png")
        self.assertEqual(graph["474"]["inputs"]["images.image_1"], ["100", 0])
        self.assertNotIn("images.image_2", graph["474"]["inputs"])
        self.assertEqual(graph["474"]["inputs"]["resolution"], 0)


if __name__ == "__main__":
    unittest.main()
