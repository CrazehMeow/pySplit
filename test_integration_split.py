import unittest
import os
import subprocess


class TestCommandlineParserMethods(unittest.TestCase):

		def test_split_lines_equal(self):
				# split file with test data into lines
				subprocess.run(["python", "split.py", "-l", "4", "test_data"])
				# join file back together using system tools
				result_file = os.popen("cat x[0-9][0-9]")
				# open the file with test data for comparison
				test_data_file = open("test_data", 'r')

				result_line = result_file.readline()
				expected_line = test_data_file.readline()

				# iterate over result and expected until either is empty
				while result_line != '' or expected_line != '':
						if result_line != expected_line:
								self.fail()
						# read next lines from result and expected
						result_line = result_file.readline()
						expected_line = test_data_file.readline()


if __name__ == '__main__':
		unittest.main()
