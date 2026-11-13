import unittest
from src.audit import apply_human_confirmation, review_fingerprint


class HumanConfirmationTests(unittest.TestCase):
    def setUp(self):
        self.row = {"id": "COH-01-A", "kind": "coherence", "label": "1", "reason": "Incomplete sentence.",
                    "human_label": "", "human_reason": "", "reviewer": "", "reviewed_at": ""}
        self.confirmation = {"reviewer": "Student", "recorded_at": "2026-11-13T12:00:00+00:00",
                             "accepted_rows": {self.row["id"]: review_fingerprint(self.row)}}

    def test_explicit_confirmation_accepts_exact_reviewed_row(self):
        apply_human_confirmation([self.row], self.confirmation)
        self.assertEqual(self.row["human_label"], "1")
        self.assertEqual(self.row["reviewer"], "Student")
        self.assertEqual(self.row["review_status"], "human reviewed and accepted")

    def test_changed_content_invalidates_previous_confirmation(self):
        apply_human_confirmation([self.row], self.confirmation)
        self.row["reason"] = "A revised interpretation that was not accepted."
        apply_human_confirmation([self.row], self.confirmation)
        self.assertEqual(self.row["human_label"], "")
        self.assertEqual(self.row["reviewer"], "")
        self.assertIn("re-review required", self.row["review_status"])

    def test_unapproved_row_cannot_be_auto_confirmed(self):
        self.row["id"] = "COH-02-A"
        apply_human_confirmation([self.row], self.confirmation)
        self.assertEqual(self.row["human_label"], "")


if __name__ == "__main__":
    unittest.main()
