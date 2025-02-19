# This script converts a crochet pattern into a specific format for overlay mosaic crochet.

# The input is a TSV file with a pattern row on each line, formatted as "[Row number]\t[Row color]\t[Row pattern].
# The row number is optional; if not provided, it will be generated sequentially starting from 1.
# The row color is optional; if not provided, it will alternate between 'A' for odd rows and 'B' for even rows.
# The row pattern is a comma-separated list that describes the stitches in the row as segments of repeated stitch types.
# Each segment of the pattern is in the format "[Stitch count][Stitch type], e.g. "2sc,3hdc,4dc".

# The output is a formatted string for each row, with the row number, color, and stitch pattern.
# The row number and color are padded to fixed widths for readability.
# The stitch pattern adds a starting stitch number to each segment, e.g. "[1] 2sc, [3] 3hdc, [6] 4dc".
# A border stitch is added at the start and end of each row.

# The script also handles the case where the input file is empty or not provided.
# The output is written to a new file with "_output" appended to the original filename.
# The script is designed to be run from the command line with the input file as an argument.

# Example input file:
# 1	red	2sc,3hdc,4dc
# 2	blue	5dc,6sc

# Example output file:
#     1. red        bs, [1] 2sc, [3] 3hdc, [6] 4dc, bs
#     2. blue       bs, [1] 5dc, [6] 6sc, bs


import sys

border_stitch = 'bs'
row_color_right_padding = 10
row_elements_number_color_pattern = 3
row_elements_color_pattern = 2
row_elements_pattern = 1
row_number_left_padding = 5


def format_row_color(color):
    return color.ljust(row_color_right_padding) + ' '

def format_row_number(row_number):
    return str(row_number).rjust(row_number_left_padding) + '. '

def format_row_pattern_segment(stitch_count, stitch_type):
    return str(stitch_count) + stitch_type + ', '

def format_starting_stitch(stitch_number):
    return '[' + str(stitch_number) + '] '

def is_even(number):
    return number % 2 == 0

def is_odd(number):
    return number % 2 == 1

def load_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip().split('\t') for line in lines]

def parse_row(row, row_number=None):
    if len(row) == row_elements_number_color_pattern:
        row_number = row[0]
        row_color = row[1]
        row_pattern = row[2]
    elif len(row) == row_elements_color_pattern:
        row_color = row[0]
        row_pattern = row[1]
    else:
        row_color = 'A' if is_odd(int(row_number)) else 'B'
        row_pattern = row[0]
    output = []
    output.append(format_row_number(row_number))
    output.append(format_row_color(row_color))
    output.append(border_stitch + ', ')
    output.append(parse_row_pattern(row_pattern))
    output.append(border_stitch)
    return ''.join(output)

def parse_row_pattern(row_pattern):
    output = []
    segments = row_pattern.split(',')
    starting_stitch = 1
    for segment in segments:
        stitch_count = int(segment[:-2])
        stitch_type = segment[-2:]
        output.append(format_starting_stitch(starting_stitch))
        output.append(format_row_pattern_segment(stitch_count, stitch_type))
        starting_stitch += stitch_count
    return ''.join(output)

def parse_rows(rows):
    output = []
    row_count = 1
    for row in rows:
        if not row or len(row) < row_elements_pattern:
            continue
        row_number = row_count
        output.append(parse_row(row, row_number))
        row_count += 1
    return output


def main():
    input_file_path = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    rows = load_input_file(input_file_path)
    if not rows:
        print("The input file is empty.")
        return
    formatted_rows = parse_rows(rows)
    output_file_path = input_file_path.split('.')[0] + '_output.txt'
    with open(output_file_path, 'w') as file:
        for row in formatted_rows:
            file.write(row + '\n')
    print(f"Formatted rows have been written to {output_file_path}.")
    return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python OverlayMosaicCrochetPatternConverter.py <input_file>")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("Warning: Only the first argument will be used as the input file.")
        sys.exit(1)
    main()
