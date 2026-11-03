import unittest
from milyar.boot_security_audit import classify_result


class BootAuditClassificationTests(unittest.TestCase):
    def test_success(self):
        self.assertEqual(
            classify_result("نجاح: الفحص سليم")[0], "PASS"
        )

    def test_warning(self):
        self.assertEqual(
            classify_result("تحذير: مراجعة مطلوبة")[0], "WARNING"
        )

    def test_failure(self):
        self.assertEqual(
            classify_result("خطأ: ملف مفقود")[0], "FAIL"
        )

    def test_unknown_is_incomplete(self):
        self.assertEqual(
            classify_result("نتيجة غير معروفة")[0], "INCOMPLETE"
        )


if __name__ == "__main__":
    unittest.main()
