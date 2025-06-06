import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def setUp(self):
        self.working_directory = "calculator"

    def test_valid_directory(self):
        result = get_files_info(self.working_directory, ".")
        self.assertIn("main.py", result)
        self.assertIn("pkg", result)
        print(f"\n{result}\n")

    def test_subdirectory(self):
        result = get_files_info(self.working_directory, "pkg")
        self.assertIn("calculator.py", result)
        self.assertIn("render.py", result)
        print(f"\n{result}\n")

    def test_invalid_directory(self):
        result = get_files_info(self.working_directory, "/bin")
        self.assertEqual(
            result,
            'Error: Cannot list "/bin" as it is outside the permitted working directory',
        )
        print(f"\n{result}\n")

    def test_outside_working_directory(self):
        result = get_files_info(self.working_directory, "../")
        self.assertEqual(result, 'Error: Cannot list "../" as it is outside the permitted working directory')
        print(f'\n{result}\n')

if __name__ == "__main__":
    unittest.main()