import os


CUR_DIR = os.path.split(os.path.abspath(__file__))[0]
PROJ_DIR = CUR_DIR
COMPUTED = os.path.join(PROJ_DIR, "computed")

if os.path.exists(COMPUTED):
    if os.path.isfile(COMPUTED):
        raise Exception(f"{COMPUTED} is not a directory!")
else:
    os.makedirs(COMPUTED)

PATH_ORIGINAL = os.path.join(COMPUTED, "computed/wiki.txt")
PATH_STRIP = os.path.join(COMPUTED, "computed/strip_lines.txt")
PATH_NEWLINE = os.path.join(COMPUTED, "computed/new_lines.txt")
PATH_WORDS = os.path.join(COMPUTED, "computed/word_lines.txt")
PATH_LEM_WORDS = os.path.join(COMPUTED, "computed/lem_word_lines.txt")
PATH_NO_STOP = os.path.join(COMPUTED, "computed/no_stop_word_lines.txt")
