#!/usr/bin/env python3
# ##### Usage #####

# pySplit [-l line_count] [-a suffix_length] [file [name]]
# pySplit -b n[k|m] [-a suffix_length] [file [name]]

# -a        changes suffix length
# -b n      sets to pySplit into pieces of n bytes in size
# -b nk     sets to pySplit into pieces of n*1024 bytes in size (kb)
# -b nm     sets to pySplit into pieces of n*1038576 bytes in size (mb)
# -l        sets to pySplit into pieces of l lines

# EXIT CODE 0 for success, 1 for errors.

# ##### Program start #####

import sys
import re

# constants
MODE_LINES = 1
MODE_BYTES = 2

DEFAULT_LINES_PER_FILE = 1000

DEFAULT_OUTPUT_FILE_NAME = "x"

DEFAULT_SUFFIX_LENGTH = 2

DEBUG = False


def get_arguments():
		"""
		Helper method to filter out first command line parameter (self-reference)
		:return: An object containing the parameters of the invocation, omitting the first.
		"""
		_, *args = sys.argv
		return args


def pre_check():
		"""
		Helper method to check if invocation is legal parameter wise
		"""
		args = get_arguments()
		if "-l" in args and "-b" in args or args.count("-l") > 1 or args.count("-b") > 1:
				print("split: cannot split in more than one way")
				exit(1)


def parse_option_lines(value):
		"""
		Parses the value for the parameter option -l
		:param value: the numeric value representing the number of lines per file
		:return: int representing lines per file, exits with code 1 if value was not numeric
		"""
		try:
				return int(value)
		except ValueError:
				exit(1)


def parse_option_bytes(value):
		"""
		Parses the value for the parameter option -b
		:param value: contains a numeric value, optionally followed by k or m
		:return: int representing bytes per file, exits with code 1 if value was wrong format
		"""
		bytes_number = int(re.match("[0-9]+", value).group())
		if re.fullmatch("[0-9]+$", value) is not None:
				return bytes_number
		# regex 2: [0-9]+k
		elif re.fullmatch("[0-9]+k$", value) is not None:
				return bytes_number * 1024
		# regex 3: [0-9]+m
		elif re.fullmatch("[0-9]+m$", value) is not None:
				return bytes_number * 1038576
		else:
				print("split: invalid number of bytes:", value)
				exit(1)


def parse_option_suffix(value):
		# check if value is numeric
		try:
				return int(value)
		except ValueError:
				exit(1)


def parse_options():
		args = get_arguments()
		x = 0

		suffix_length = None
		bytes_per_file = None
		lines_per_file = None

		while x < len(args):
				if args[x] in ["-a", '-b', '-l']:
						# test if there is an argument following the parameter
						if len(args) <= x + 1:
								print("split: option requires an argument -- %s" % args[x][1])
								exit(1)

						parameter_name = args[x]
						parameter_value = args[x + 1]

						args.remove(parameter_name)
						args.remove(parameter_value)

						if parameter_name == "-a":
								suffix_length = parse_option_suffix(parameter_value)

						elif parameter_name == "-b":
								bytes_per_file = parse_option_bytes(parameter_value)

						elif parameter_name == "-l":
								lines_per_file = parse_option_lines(parameter_value)

						# increment by two for args -a, -b, -l
						x += 2
				else:
						x += 1

		# setting defaults, if applicable
		if not lines_per_file and not bytes_per_file:
				lines_per_file = DEFAULT_LINES_PER_FILE

		if not suffix_length:
				suffix_length = DEFAULT_SUFFIX_LENGTH

		return suffix_length, lines_per_file, bytes_per_file, args


def parse_operands(args):
		# args = get_arguments()
		x = 0
		operand_count = 0

		input_file_name = None
		output_file_name = None

		while x < len(args):
				if re.fullmatch("[a-zA-Z0-9_]*\\.?[a-zA-Z0-9]*", args[x]):
						if operand_count == 0:
								input_file_name = args[x]
						elif operand_count == 1:
								output_file_name = args[x]
						else:
								print("split: extra operand '%s'" % (args[x]))
								exit(1)
						operand_count += 1
				x += 1
		return input_file_name, output_file_name if output_file_name else DEFAULT_OUTPUT_FILE_NAME


def parse_arguments():
		# process command line arguments
		suffix_length, lines_per_file, bytes_per_file, remaining_args = parse_options()
		input_file_name, output_file_name = parse_operands(remaining_args)

		is_lines = lines_per_file is not None
		length_limit = lines_per_file if is_lines else bytes_per_file

		return is_lines, length_limit, suffix_length, input_file_name, output_file_name


def validate_suffix_length(output_file_suffix, suffix_length):
		if len(output_file_suffix) > suffix_length:
				print("split: reached maximum possible number of files with suffix length of %d" % suffix_length)
				exit(1)


def split_lines(lines_per_file, suffix_length, input_file, output_file_name):
		"""
				Writes the input_file to multiple output files with each file having lines_per_file lines.
				File name is based on the output_file_name parameter.
				A incrementing numeric suffix of suffix_length is appended to the output_file_name.
				:param input_file: File to read from
				:param suffix_length: Number of digits to add to each filename
				:param lines_per_file: Number of lines each output file has
				:param output_file_name: Output file name prefix
		"""

		output_file_suffix = str(0).zfill(suffix_length)
		output_file = open(output_file_name + output_file_suffix, 'x')

		line_count = 0
		for line in input_file:
				output_file.write(line)

				line_count += 1
				if line_count == lines_per_file:
						line_count = 0

						output_file.close()
						output_file_suffix = str(int(output_file_suffix) + 1).zfill(suffix_length)

						validate_suffix_length(output_file_suffix, suffix_length)
						output_file = open(output_file_name + output_file_suffix, 'x')

		output_file.close()
		input_file.close()
		return


def split_bytes(bytes_per_file, suffix_length, input_file, output_file_name):
		"""
				Writes the input_file to multiple output files with each having bytes_per_file bytes.
				File name is based on the output_file_name parameter.
				A incrementing numeric suffix of suffix_length is appended to the output_file_name.
				:param input_file: File to read from
				:param suffix_length: Number of digits to add to each filename
				:param bytes_per_file: Output file size
				:param output_file_name: Output file name prefix
		"""

		output_file_suffix = str(0).zfill(suffix_length)
		output_file = open(output_file_name + output_file_suffix, 'xb')

		bytes_value = input_file.read(bytes_per_file)
		while bytes_value != b"":
				output_file.write(bytes_value)

				output_file.close()
				output_file_suffix = str(int(output_file_suffix) + 1).zfill(suffix_length)

				validate_suffix_length(output_file_suffix, suffix_length)
				output_file = open(output_file_name + output_file_suffix, 'xb')

				bytes_value = input_file.read(bytes_per_file)

		output_file.close()
		input_file.close()
		return


def split():
		is_lines, length_limit, suffix_length, input_file_name, output_file_name = parse_arguments()

		if DEBUG:
				print_debug(is_lines, length_limit, suffix_length, input_file_name, output_file_name)

		if input_file_name is None:
				if is_lines:
						split_lines(length_limit, suffix_length, sys.stdin, output_file_name)
				else:
						print("split: warning, byte mode not yet supported for stdin")
						split_bytes(length_limit, suffix_length, sys.stdin, output_file_name)
		else:
				if is_lines:
						split_lines(length_limit, suffix_length, open(input_file_name, 'r'), output_file_name)
				else:
						split_bytes(length_limit, suffix_length, open(input_file_name, 'rb'), output_file_name)


def print_debug(is_lines, length_limit, suffix_length, input_file_name, output_file_name):
		print("---DEBUG---")
		print("lines mode ", is_lines)
		print("delimiter is ", length_limit)
		print("suffix_length is", suffix_length)
		print("input_file_name is ", input_file_name)
		print("output_file_name is ", output_file_name)


if __name__ == "__main__":
		pre_check()
		split()

# ##### Tallence/NEO requirements #####

# 1. Über die Kommandozeile oder die Einstellungen der IDE gibt der Benutzer eine Datei und eine Anzahl Zeilen vor.
# 2. Start des Programms
# 3. Das Programm teilt die Eingabedatei in mehrere Ausgabedateien auf,
# die jeweils die gewünschte Anzahl Zeilen enthalten.
# 4. Die Dateinamen enthalten eine fortlaufende Nummer
