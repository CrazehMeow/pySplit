# pySplit by Christian Bodenbender

This is a python implementation of the popular unix tool split. 

## Features

Using this tool you can split a file into multiple files.

You can specify the size of each file, and implicitly the number of files, by providing either an argument for the target number of lines or an argument for the target number of byter per file.

## Examples

```
split.py -l 10 sales.txt
```
This will split the file 'sales.txt' into multiple files, each containing 10 lines of text. The files are named x00, x01, x02 and so on. 

```
split.py -b 4k input.mp3 split
```
This will split the binary file 'input.mp3' into multiple files, each containing 4096 Bytes of data. The files are named split00, split01, split02 and so on.

```
split.py -l 5
```
This will take the standard input as input and split it in files, each containing 5 lines of text. The files are named x00, x01, x02 and so on. The files are only written after all 5 lines for one file have been collected.

## Usage

```
pySplit [-l line_count] [-a suffix_length] [file [name]]
```
or
```
pySplit -b n[k|m] [-a suffix_length] [file [name]]
```

-a        changes suffix length

-b n      sets to pySplit into pieces of n bytes in size

-b nk     sets to pySplit into pieces of n*1024 bytes in size (kb)

-b nm     sets to pySplit into pieces of n*1038576 bytes in size (mb)

-l        sets to pySplit into pieces of l lines