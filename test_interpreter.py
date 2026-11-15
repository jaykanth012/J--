import unittest
from interpreter import JDashError, execute

class InterpreterTests(unittest.TestCase):
    def test_one_print(self):
        self.assertEqual(execute('print("Hello");'), ["Hello"])
    def test_multiple_prints(self):
        self.assertEqual(execute('print("Hello");\nprint("J--");'), ["Hello", "J--"])
    def test_comments_and_blank_lines(self):
        self.assertEqual(execute('// comment\n\nprint("OK");\n  // another'), ["OK"])
    def test_escaped_quote(self):
        self.assertEqual(execute(r'print("say \"hi\"");'), ['say "hi"'])
    def test_invalid_syntax_has_line_number(self):
        with self.assertRaisesRegex(JDashError, "Line 2"):
            execute('print("OK");\nprnt("wrong");')
    def test_non_string_is_rejected(self):
        with self.assertRaisesRegex(JDashError, "Line 1"):
            execute("print(123);")

if __name__ == "__main__":
    unittest.main()
