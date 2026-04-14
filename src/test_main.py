import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        text = extract_title("# Title 1")
        self.assertEqual(text, "Title 1")

        with self.assertRaises(Exception) as context:            
            text = extract_title("## Title 2")
            self.assertEqual(str(context.exception), "No h1 header found in markdown")

        with self.assertRaises(Exception):
            extract_title("#hello !")

        with self.assertRaises(Exception):
            extract_title("hello !")

        