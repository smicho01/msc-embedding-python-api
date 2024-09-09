import unittest
from apputils import nlp_utils


class TestIsEnglish(unittest.TestCase):

    def test_is_english_true_case(self):
        self.assertEqual(nlp_utils.is_english("Hello world! This is a simple English string."), True)

    def test_is_english_false_case(self):
        self.assertEqual(nlp_utils.is_english("Bonjour le monde! Ceci est une simple chaîne française."), False)

    def test_is_english_with_numbers(self):
        self.assertEqual(nlp_utils.is_english("Hello world! The year is 2024."), True)

    def test_is_english_empty_string(self):
        self.assertEqual(nlp_utils.is_english(""), False)

    def test_is_english_none(self):
        self.assertEqual(nlp_utils.is_english(None), False)

    def test_is_english_mixed_language(self):
        self.assertEqual(nlp_utils.is_english("Bonjour world! This est a simple string."), False)

    def setUp(self):
        self.true_not_spam_text = "Hello, how are you?"
        self.true_spam_text = "Congratulations! You've won a million dollars!"

    def test_is_not_spam_true(self):
        result = nlp_utils.is_not_spam(self.true_not_spam_text)
        self.assertTrue(result)


def test_is_not_spam_false(self):
    result = nlp_utils.is_not_spam(self.true_spam_text)
    self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
