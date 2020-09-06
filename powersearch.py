import os
import logging
import argparse

# logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Command line tool for searching the content of multiple files at once')
parser.add_argument('--path', help='Select a path')
parser.add_argument('--b', action='store_true', help='help_text_b')
parser.add_argument('--c', action='store_true', help='help_text_c')
args = parser.parse_args()

if args.path:
    logging.info(f'path={args.path}')

if args.b:
    temp_a = "option_a"
else:
    temp_a = "option_b"

if args.c:
    temp_b = "option_c"
else:
    temp_b = "option_d"

# logging.info(f"stuff: {temp_a,temp_b}")
# print(f"stuff: {temp_a,temp_b}")

def listfiles(path):
    if path == "" or path == None:
        path = os.getcwd()
    print(path)
    files = []
    # r=root, d=directories, f=files
    for r, d, f in os.walk(path):
        for filename in f:
            files.append(os.path.join(r, filename))
            print(filename)

listfiles(args.path)

k = input("Finished.") 
