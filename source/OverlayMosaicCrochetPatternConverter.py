# This script converts a crochet pattern into a specific format for overlay mosaic crochet.
# The input is a CSV file with the following format:
# Line Number, Color, Row Pattern
# The row pattern is a comma-separated list of stitch counts and types, e.g. "2sc,3hdc,4dc".
# The output is a formatted string for each row, with the line number, color, and stitch pattern.
# The stitch pattern is formatted as [starting stitch] stitch count and type, e.g. "[1] 2sc, [3] 3hdc, [6] 4dc".
# A border stitch is added at the start and end of each row pattern.


import sys

border_stitch = 'bs'


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
    return


def format_row_color(color):
    return color + ' '

def format_row_number(row_number):
    return str(row_number) + '. '

def format_row_pattern_segment(stitch_count, stitch_type):
    return str(stitch_count) + stitch_type + ', '

def format_starting_stitch(stitch_number):
    return '[' + str(stitch_number) + '] '

def load_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip().split(',') for line in lines]

def parse_row(row):
    output = []
    output.append(format_row_number(row[0]))
    output.append(format_row_color(row[1]))
    output.append(border_stitch + ', ')
    output.append(parse_row_pattern(row[2:]))
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
    for row in rows:
        output.append(parse_row(row))
    return output
