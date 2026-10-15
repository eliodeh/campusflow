import unittest
from validation import validate_affected_users, validate_title
from validation import ValidationError


class TestValidateAffectedUsers(unittest.TestCase):

    def test_accepts_positive_int(self):
        self.assertEqual(validate_affected_users(5), 5)

    def test_rejects_true(self):
        with self.assertRaises(ValidationError):
            validate_affected_users(True)

    # ... other affected_users tests ...


class TestValidateTitle(unittest.TestCase):

    def test_rejects_blank_title(self):
        with self.assertRaises(ValidationError):
            validate_title(" ")

    def test_rejects_non_string_title(self):
        with self.assertRaises(ValidationError):
            validate_title(None)


if __name__ == "__main__":
    unittest.main()
