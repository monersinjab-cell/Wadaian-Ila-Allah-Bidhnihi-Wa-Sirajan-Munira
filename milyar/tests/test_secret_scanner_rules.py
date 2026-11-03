import re
import unittest

class SecretScannerRuleTests(unittest.TestCase):
    def test_private_key_header_is_detected(self):
        rule = re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
        )
        self.assertIsNotNone(
            rule.search("-----BEGIN PRIVATE KEY-----")
        )

    def test_regex_definition_is_not_a_private_key(self):
        rule = re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
        )
        self.assertIsNone(
            rule.search('re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")')
        )

    def test_non_key_text_is_not_detected(self):
        rule = re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
        )
        self.assertIsNone(rule.search("ordinary project documentation"))

if __name__ == "__main__":
    unittest.main()
