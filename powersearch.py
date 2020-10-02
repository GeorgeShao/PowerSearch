import os
import re
import sys
import argparse
from multiprocessing import Pool
import textract
from itertools import product

parser = argparse.ArgumentParser(
    description="Command line tool for searching the content of multiple files at once"
)
parser.add_argument("--path", help="Select a path")
parser.add_argument("--keyword", help="Search for a keyword")
parser.add_argument("--encoding", help="Set an encoding (default=utf8)")
parser.add_argument(
    "--include-dot-dirs",
    action="store_true",
    help="Include directories that only have an extension and no name",
)
parser.add_argument(
    "--include-dot-files",
    action="store_true",
    help="Include files that only have an extension and no name",
)
parser.add_argument(
    "--include-no-ext", action="store_true", help="Include files with no extension"
)
parser.add_argument(
    "--show-errors",
    action="store_true",
    help="Show errors, will not return results if errors are found",
)
parser.add_argument(
    "--show-received", action="store_true", help="Show received file status"
)
parser.add_argument("--show-read", action="store_true", help="Show read file status")
parser.add_argument(
    "--show-skipped",
    action="store_true",
    help="Show skipped dot dirs, dot files, noext files, and stdignored files",
)
parser.add_argument(
    "--case-sensitive",
    action="store_true",
    help="Enable case-sensitive keyword searching",
)

args = parser.parse_args()

if args.keyword == "" or args.keyword == None:
    print("ERROR: keyword argument missing")
    exit()
else:
    keyword = args.keyword
    # print(f"KEYWORD = {keyword}")

if args.encoding == "" or args.encoding == None:
    encoding = "utf8"
else:
    encoding = args.encoding
    print(f"ENCODING = {encoding}")

if args.show_errors:
    error_handling_type = "strict"
else:
    error_handling_type = "ignore"

if args.case_sensitive:
    case_sensitive = True
else:
    case_sensitive = False
    keyword = keyword.lower()

if args.show_read:
    show_read = True
else:
    show_read = False

files = []
total_occurences = 0


def main():
    global files, keyword, encoding, error_handling_type, case_sensitive, show_read

    def getValidFiles(path):
        global files, keyword, encoding, error_handling_type, case_sensitive, show_read
        if path == "" or path == None:
            path = os.getcwd()

        print(f"PATH = {path}")

        if args.show_received:
            show_received = True
        else:
            show_received = False

        if args.show_skipped:
            show_skipped = True
        else:
            show_skipped = False

        std_ignored_exts = [
            ".cache",
            ".pyc",
            "toc",
            ".zip",
            ".pkg",
            ".pyz",
            ".map",
            ".eot",
            ".ttf",
            ".woff",
            ".woff2",
            ".class",
            ".jar",
            ".veg",
            ".bak",
            ".mp4",
            ".mov",
            ".ini",
            ".gif",
            ".jpg",
            ".jpeg",
            ".mp3",
            ".ogg",
            ".png",
            ".tiff",
            ".tif",
            ".wav",
            ".svg",
        ]

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

            # check if dot dir is in a dot dir
            for dir in d:
                if dir.startswith(".") and not args.include_dot_dirs:
                    for dir1 in skipped_dot_dirs:
                        if ("\\" + dir1) in r:
                            try:
                                del skipped_dot_dirs[skipped_dot_dirs.index(dir)]
                            except:
                                pass

            # check validity of files
            for filename in f:

                # check if file is in a dot dir
                full_file_path = os.path.join(r, filename)
                in_dot_dir = False
                for dir in skipped_dot_dirs:
                    if ("\\" + dir + "\\") in full_file_path:
                        in_dot_dir = True
                        break
                if in_dot_dir:
                    continue

                # check if the file only has an extension and no name
                if filename.startswith(".") and not args.include_dot_files:
                    if filename not in skipped_dot_files:
                        skipped_dot_files.append(filename)
                    continue

                # check if filename doesn't have an extension
                if "." not in filename and not args.include_no_ext:
                    if filename not in skipped_noext_files:
                        skipped_stdignored_files.append(full_file_path)
                    continue

                # check if filename has a standard ignored extension
                hide_file_status = False
                for ext in std_ignored_exts:
                    if filename.endswith(ext):
                        if filename not in skipped_stdignored_files:
                            hide_file_status = True
                            skipped_stdignored_files.append(full_file_path)
                        break

                # output filenames that meet all criteria
                if not hide_file_status:
                    if full_file_path not in files:
                        files.append(full_file_path)

        # output skipped dirs/files stats
        if show_skipped:
            print(f"SKIPPED DOT DIRS = {len(skipped_dot_dirs)} {skipped_dot_dirs}")
            print(f"SKIPPED DOT FILES = {len(skipped_dot_files)} {skipped_dot_files}")
            print(
                f"SKIPPED NOEXT FILES = {len(skipped_noext_files)} {skipped_noext_files}"
            )
            print(
                f"SKIPPED STDIGNORED EXTS = {len(skipped_stdignored_files)} {skipped_stdignored_files}"
            )
        print(f"# FILES RECEIVED = {len(files)}")

        for filepath in files:
            if show_received:
                print(f"RECEIVED: {filepath}")

        return files

    def parallelization():
        global files, keyword, encoding, error_handling_type, case_sensitive, show_read, total_occurences
        pool = Pool()
        valid_files = getValidFiles(args.path)
        results = pool.map(scanFiles, valid_files)
        pool.close()
        pool.join()
        k = input("Finished. Press enter to exit.")

    parallelization()


def scanFiles(filepath):
    global files, keyword, encoding, error_handling_type, case_sensitive, show_read
    global total_occurences
    filename, file_extension = os.path.splitext(filepath)
    if file_extension in [
        ".csv",
        ".docx",
        ".eml",
        ".epub",
        ".pdf",
        # ".gif",  does not work due to dependencies
        # ".jpg", does not work due to dependencies
        # ".jpeg", does not work due to dependencies
        # ".json", just use raw text searching instead, faster
        # ".html", just use raw text searching instead, faster, more accurate
        # ".htm", just use raw text searching instead, faster, more accurate
        # ".mp3", does not work due to dependencies
        ".msg",
        ".odt",
        # ".ogg",  does not work due to dependencies
        # ".png",  does not work due to dependencies
        ".pptx",
        ".ps",
        ".rtf",
        # ".tiff",  does not work due to dependencies
        # ".tif",  does not work due to dependencies
        # ".wav", does not work due to dependencies
        ".xlsx",
        ".xls",
    ]:
        try:
            if show_read:
                print(f"READ: {filepath}")
            file_content = textract.process(filepath).decode("utf8")
            file_content = str(file_content)
            file_content = re.sub(r"\u003c\\1", "", file_content)
            if not args.case_sensitive:
                file_content = file_content.lower()
            num_occurences = str(file_content).count(keyword)
            if num_occurences > 0:
                print(f"RESULT: {num_occurences} occurences in {filepath}")
                total_occurences += num_occurences
        except Exception as e:
            if error_handling_type == "strict":
                print("ERROR1:", e, "[" + filepath + "]")

    else:
        with open(filepath, "r", encoding=encoding, errors=error_handling_type) as file:
            try:
                if show_read:
                    print(f"READ: {filepath}")
                file_content = file.read()
                file_content = str(file_content)
                file_content = re.sub(r"\u003c\\1", "", file_content)
                if not args.case_sensitive:
                    file_content = re.escape(file_content).lower()
                num_occurences = file_content.count(keyword)
                if num_occurences > 0:
                    print(f"RESULT: {num_occurences} occurences in {filepath}")
                    total_occurences += num_occurences
            except Exception as e:
                print("ERROR:", e, "[" + filepath + "]")


if __name__ == "__main__":
    main()
