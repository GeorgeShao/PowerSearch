import os
import logging
import argparse

# logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Command line tool for searching the content of multiple files at once')
parser.add_argument('--path', help='Select a path')
parser.add_argument('--include-ext-only', action='store_true', help='Include files that only have an extension')
parser.add_argument('--include-no-ext', action='store_true', help='Include files with no extension')
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

std_ignored_exts = [".cache"]

def listfiles(path):
    if path == "" or path == None:
        path = os.getcwd()
    print(path)
    files = []
    num_skipped_hidden_dirs = 0
    skipped_hidden_files = 0
    num_skipped_noext_files = 0
    num_skipped_stdignored_files = 0

    skipped_hidden_dirs = []
    skipped_hidden_files = []
    skipped_noext_files = []
    skipped_stdignored_files = []
    
    # r=root, d=directories, f=files
    for r, d, f in os.walk(path):
        # check if the folder is hidden
        for dir in d:
            if not dir.startswith("."):
                for filename in f:
                    hide_file_status = False
                    # check if the file is hidden
                    if filename.startswith(".") and not args.include_ext_only:
                        num_skipped_hidden_files += 1
                        skipped_noext_files.append(filename)
                        break
                    # check if filename has an extension
                    if "." not in filename and not args.include_no_ext:
                        num_skipped_noext_files += 1
                        skipped_noext_files.append(filename)
                        break
                    # check if filename has a standard ignored extension
                    for ext in std_ignored_exts:
                        if filename.endswith(ext):
                            hide_file_status = True
                            num_skipped_stdignored_files += 1
                            skipped_stdignored_files.append(filename)
                            break
                    # output filenames that meet all criteria
                    if not hide_file_status:
                        files.append(os.path.join(r, filename))
                        print(filename)
            else:
                num_skipped_hidden_dirs += 1
                skipped_hidden_dirs.append(dir)
    # output skipped dirs/files stats
    print(f"skipped hidden dirs = {num_skipped_hidden_dirs} {skipped_hidden_dirs}")
    print(f"skipped noext files = {num_skipped_noext_files} {skipped_noext_files}")
    print(f"skipped stdignored exts = {num_skipped_stdignored_files} {skipped_stdignored_files}")
    

listfiles(args.path)

k = input("Finished.") 
