import os
import argparse

parser = argparse.ArgumentParser(description='Command line tool for searching the content of multiple files at once')
parser.add_argument('--path', help='Select a path')
parser.add_argument('--include-dot-dirs', action='store_true', help='Include directories that only have an extension and no name')
parser.add_argument('--include-dot-files', action='store_true', help='Include files that only have an extension and no name')
parser.add_argument('--include-no-ext', action='store_true', help='Include files with no extension')
args = parser.parse_args()

std_ignored_exts = [".cache", ".pyc"]

valid_dir_name = True

def listfiles(path):
    if path == "" or path == None:
        path = os.getcwd()
    print(f'PATH = {args.path}')

    files = []
    skipped_dot_dirs = []
    skipped_dot_files = []
    skipped_noext_files = []
    skipped_stdignored_files = []
    
    # r=root, d=directories, f=files
    for r, d, f in os.walk(path):
        # check if dir is a dot dir
        for dir in d:
            if dir.startswith(".") and not args.include_dot_dirs:
                skipped_dot_dirs.append(dir)
                valid_dir_name = False
            else:
                valid_dir_name = True
        if valid_dir_name:
            for filename in f:
                # print(r, d, f, filename)
                hide_file_status = False
                # check if the file only has an extension and no name
                if filename.startswith(".") and not args.include_dot_files:
                    if filename not in skipped_dot_files:
                        skipped_dot_files.append(filename)
                        hide_file_status = True
                    continue
                # check if filename doesn't have an extension
                if "." not in filename and not args.include_no_ext:
                    if filename not in skipped_noext_files:
                        skipped_noext_files.append(filename)
                        hide_file_status = True
                    continue
                # check if filename has a standard ignored extension
                for ext in std_ignored_exts:
                    if filename.endswith(ext):
                        if filename not in skipped_stdignored_files:
                            hide_file_status = True
                            skipped_stdignored_files.append(filename)
                        break
                # output filenames that meet all criteria
                if not hide_file_status:
                    # files.append(os.path.join(r, filename))
                    if filename not in files:
                        files.append(filename)
                
    # output skipped dirs/files stats
    print(f"SKIPPED DOT DIRS = {len(skipped_dot_dirs)} {skipped_dot_dirs}\n")
    print(f"SKIPPED DOT FILES = {len(skipped_dot_files)} {skipped_dot_files}\n")
    print(f"SKIPPED NOEXT FILES = {len(skipped_noext_files)} {skipped_noext_files}\n")
    print(f"SKIPPED STDIGNORED EXTS = {len(skipped_stdignored_files)} {skipped_stdignored_files}\n")
    print(f"FILES = {len(files)} {files}\n")


listfiles(args.path)

k = input("Finished.")
