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
# EXIT CODE 0 for success, >0 for errors.

# ##### Program start #####

import sys

# default is 1000, modified by -l
lines_per_file = 1000

# default is x
output_file_name = "x"

# default length is 2, pattern is 'aa', 'ab' 'ac' etc. for a max of 676 files with a suffix length of 2.
# If the suffix limit is exceeded, files up to the last allowed suffix are created and then pySplit fails.
# If the suffix limit is not exceeded, the last created file contains the remainder of content from input.
# If the input is empty, no output file is created. This is not an error.
# modified with -a
suffix_length = 2

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

# iterate over arguments, analyze each argument and react accordingly.

# debate: lookahead for tokens such as -a or -b or -l?

# output file name prefix is always the last argument if it exists
# input file name is always the last or second last argument if it exists

# for incrementing chars, this is helpful https://stackoverflow.com/questions/2156892/python-how-can-i-increment-a-char

# ##### Tallence/NEO requirements #####

# 1. Über die Kommandozeile oder die Einstellungen der IDE gibt der Benutzer eine Datei und eine Anzahl Zeilen vor.
# 2. Start des Programms
# 3. Das Programm teilt die Eingabedatei in mehrere Ausgabedateien auf, die jeweils die gewünschte Anzahl Zeilen enthalten.
# 4. Die Dateinamen enthalten eine fortlaufende Nummer
