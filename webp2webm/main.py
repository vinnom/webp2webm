import sys
import os
from convert_and_resize import convert_webp_to_webm


def main():
    files_to_convert = [f for f in sys.argv[1:] if os.path.isfile(f) and f.endswith(".webp")]
    convert_webp_to_webm(files_to_convert)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: webp2webm <files-to-convert>")
        sys.exit(1)
    else:
        main()
