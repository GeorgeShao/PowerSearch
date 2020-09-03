import os
import logging
import argparse

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Command line tool for searching the content of multiple files at once')
parser.add_argument('--a', help='help_text_a')
parser.add_argument('--b', action='store_true', help='help_text_b')
parser.add_argument('--c', action='store_true', help='help_text_c')
args = parser.parse_args()

if args.a:
    logging.info('--a enabled. Accounting will not be disabled.')

if args.b:
    temp_a = "option_a"
else:
    temp_a = "option_b"

if args.c:
    temp_b = "option_c"
else:
    temp_b = "option_d"

logging.info(f"stuff: {temp_a,temp_b}")

