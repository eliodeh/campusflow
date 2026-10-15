import unittest
from validation import validate_affected_users, ValidationError


class TestValidateAffectedUsers(unittest.TestCase):
    def test_accepts_positive_int(self):
        self.assertEqual(validate_affected_users(5), 5)

    def test_rejects_true(self):
        with self.assertRaises(ValidationError):
            validate_affected_users(True)

    def test_rejects_negative(self):
        with self.assertRaises(ValidationError):
            validate_affected_users(-3)

    def test_rejects_string(self):
        with self.assertRaises(ValidationError):
            validate_affected_users("5")

import unittest
from validation import validate_affected_users, ValidationError


class TestValidateAffectedUsers(unittest.TestCase):
    def test_accepts_positive_int(self):
        self.assertEqual(validate_affected_users(5), 5)

    def test_rejects_true(self):
        with self.assertRaises(ValidationError):
            validate_affected_users(True)

    def test_rejects_negative(self):
        with self.assertRaises(ValidationError):
            validate_affected_users(-3)

    def test_rejects_string(self):
        with self.assertRaises(ValidationError):
            validate_affected_users("5")

    def test_rejects_blank_title(self):
    with self.assertRaises(ValidationError):
        validate_title("   ")

def test_rejects_non_string_title(self):
    with self.assertRaises(ValidationError):
        validate_title(None)
        
if __name__ == "__main__":
    unittest.main()
if __name__ == "__main__":
    unittest.main()