#!/usr/bin/env python3
# ##### Usage #####

# pySplit [-l line_count] [-a suffix_length] [file [name]]
# pySplit -b n[k|m] [-a suffix_length] [file [name]]

# -a        changes suffix length
# -b n      sets to pySplit into pieces of n bytes in size
# -b nk     sets to pySplit into pieces of n*1024 bytes in size (kb)
# -b nm     sets to pySplit into pieces of n*1038576 bytes in size (mb)
# -l        sets to pySplit into pieces of l lines

# STDOUT is not used
# STDERR is used for diagnostic messages
# EXIT CODE 0 for success, 1 for errors.

# ##### Program start #####

import sys
import re

# constants
MODE_LINES = 1
MODE_BYTES = 2

# default is 1000, modified by -l
lines_per_file = 1000

# no default is set
bytes_per_file = -1

# counts operands that are not preceded by a '-'
operand_count = 0

# default of '-' signifies input from stdin
input_file_name = "-"

# default is x
output_file_name = "x"

# default length is 2
# modified with -a
suffix_length = 2

split_mode = MODE_LINES

# filter out program name reference
_, *args = sys.argv

if "-l" in args and "-b" in args or args.count("-l") > 1 or args.count("-b") > 1:
    print("split: cannot split in more than one way")
    exit(1)

# process command line arguments
x = 0
while x < len(args):
    if args[x] in ["-a", '-b', '-l']:
        # test if there is an argument following the parameter
        if len(args) <= x+1:
            print("split: option requires an argument -- %s" % args[x][1])
            exit(1)

        parameterName = args[x]
        parameterValue = args[x+1]

        if parameterName == "-a":
            # check if value is numeric
            try:
                suffix_length = int(parameterValue)
            except ValueError:
                exit(1)

        if parameterName == "-b":
            split_mode = MODE_BYTES
            bytes_number = int(re.match("[0-9]+", parameterValue).group())
            if re.fullmatch("[0-9]+$", parameterValue) is not None:
                bytes_per_file = bytes_number
            # regex 2: [0-9]+k
            elif re.fullmatch("[0-9]+k$", parameterValue) is not None:
                bytes_per_file = bytes_number * 1024
            # regex 3: [0-9]+m
            elif re.fullmatch("[0-9]+m$", parameterValue) is not None:
                bytes_per_file = bytes_number * 1038576
            else:
                print("split: invalid number of bytes:", parameterValue)
                exit(1)

        if parameterName == "-l":
            split_mode = MODE_LINES
            try:
                lines_per_file = int(parameterValue)
            except ValueError:
                exit(1)

        # increment by two for args -a, -b, -l
        x += 2
    elif re.fullmatch("[a-zA-Z0-9_]*\\.?[a-zA-Z0-9]*", args[x]):
        if operand_count == 0:
            input_file_name = args[x]
        elif operand_count == 1:
            output_file_name = args[x]
        else:
            print("split: extra operand '%s'" % (args[x]))
            exit(1)
        operand_count += 1
        x += 1

# start processing file
# todo: implement
if input_file_name == "-":
    # use stdin
    print("Using stdin...")
else:
    if split_mode == MODE_LINES:
        input_file = open(input_file_name, 'r')
        line_count = 0
        output_file_suffix = str(0).zfill(suffix_length)
        output_file = open(output_file_name + output_file_suffix, 'x')
        for line in input_file:
            output_file.write(line)
            line_count += 1
            if line_count == lines_per_file:
                line_count = 0
                output_file.close()
                output_file_suffix = str(int(output_file_suffix) + 1).zfill(suffix_length)
                if len(output_file_suffix) > suffix_length:
                    print("split: reached maximum possible number of files with suffix length of %d" % suffix_length)
                    exit(1)
                output_file = open(output_file_name + output_file_suffix, 'x')
        output_file.close()
        input_file.close()
    elif split_mode == MODE_BYTES:
        input_file = open(input_file_name, 'rb')
        # f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.
    # output_file = open(output_file_name, 'x')


print("---DEBUG---")
print("mode_set is ", split_mode)
print("suffix_length is", suffix_length)
print("lines_per_file is", lines_per_file)
print("bytes_per_file is", bytes_per_file)
print("input_file_name is ", input_file_name)
print("output_file_name is ", output_file_name)

# for incrementing chars, this is helpful https://stackoverflow.com/questions/2156892/python-how-can-i-increment-a-char

# ##### Tallence/NEO requirements #####

# 1. Über die Kommandozeile oder die Einstellungen der IDE gibt der Benutzer eine Datei und eine Anzahl Zeilen vor.
# 2. Start des Programms
# 3. Das Programm teilt die Eingabedatei in mehrere Ausgabedateien auf, die jeweils die gewünschte Anzahl Zeilen enthalten.
# 4. Die Dateinamen enthalten eine fortlaufende Nummer
