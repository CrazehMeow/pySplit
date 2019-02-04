import unittest
import split


class TestCommandlineParserMethods(unittest.TestCase):

		def test_parse_option_numeric_value_success(self):
				test_data = range(0, 10)
				for data in test_data:
					value = split.parse_option_numeric_value(data)
					self.assertEqual(value, data)

		def test_parse_option_numeric_value_exit(self):
				test_data = "-"
				try:
						split.parse_option_numeric_value(test_data)
						self.fail()
				except SystemExit as e:
						if e.code != 1:
								self.fail()

		def test_parse_option_bytes_success(self):
				test_data = [["5", 5], ["5k", 5120], ["5m", 5192880]]
				for data in test_data:
						value = split.parse_option_bytes(data[0])
						self.assertEqual(value, data[1])

		def test_parse_option_bytes_exit(self):
				test_data = ["-", "5kk", "k5", "5km", "5mk", "-1"]
				for data in test_data:
						try:
								split.parse_option_bytes(data)
								self.fail()
						except SystemExit as e:
								if e.code != 1:
										self.fail()

		def test_parse_operands_success(self):
				test_data = [[[""], ("", "x")], [["name"], ("name", "x")], [["in", "out"], ("in", "out")]]
				for data in test_data:
						value = split.parse_operands(data[0])
						self.assertEqual(value, data[1])

		def test_parse_operands_exit(self):
				test_data = ["in", "out", "three"]
				try:
						split.parse_operands(test_data)
						self.fail()
				except SystemExit as e:
						if e.code != 1:
								self.fail()


if __name__ == '__main__':
		unittest.main()
