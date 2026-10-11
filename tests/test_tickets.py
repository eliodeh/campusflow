import unittest 
from campusflow.tickets import calculate_priority

class TestCalculatePriority(unittest.TestCase):
    def test_high_urgency_and_10_users_is_critical(self):
        result = calculate_priority("high", 10)
        self.assertEqual(result, "critical")

    def test_high_urgency_and_2_users_is_high(self):
        result = calculate_priority("high", 2)
        self.assertEqual(result, "high")
    def test_low_urgency_and_1_users_is_low(self):
        result = calculate_priority("low", 1)
        self.assertEqual(result, "low")
    def test_low_urgency_and_3_users_is_medium(self):
        result = calculate_priority("low", 3)
        self.assertEqual(result, "medium")
    def test_low_urgency_and_9_users_is_medium(self):
        result = calculate_priority("low", 9)
        self.assertEqual(result, "medium")
    def test_low_urgency_and_10_users_is_high(self):
        result = calculate_priority("low", 10)
        self.assertEqual(result, "high")
    def test_medium_urgency_and_1_users_is_medium(self):
        result = calculate_priority("medium", 1)
        self.assertEqual(result, "medium")
    def test_medium_urgency_and_10_users_is_high(self):
        result = calculate_priority("medium", 10)
        self.assertEqual(result, "high")
    def test_high_urgency_and_9_users_is_high(self):
        result = calculate_priority("high", 9)
        self.assertEqual(result, "high")
    

if __name__ == "__main__":
    unittest.main()