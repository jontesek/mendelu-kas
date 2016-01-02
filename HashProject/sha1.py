#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import codecs
import locale
from src.Sha1Algo import Sha1Algo

# Create the main object
sa = Sha1Algo()
# Save terminal encoding
terminal_encoding = sys.stdin.encoding


# If the file was imported.
def hash_text(input_text):
    return sa.hash_text(input_text)

def hash_file(file_path):
    return sa.hash_file(os.path.abspath(file_path))


# If the script was run directly.
if __name__ == '__main__':
    # Imports required for command line parsing.
    import argparse

    # Parse the incoming arguments: sha1.py -s <string> OR -f <filename> OR -v
    parser = argparse.ArgumentParser(description='SHA1 in Python')
    parser.add_argument('-s', action='store', help='string to hash', metavar='<string>')
    parser.add_argument('-f', action='store', help='file to hash', metavar='<filename>')
    parser.add_argument('-v', action='store_true', help='verbose output - show some steps')
    args = parser.parse_args()

    # Check arguments and call the correct hashing method.
    if args.s:
        final_digest = sa.hash_text(args.s, terminal_encoding, args.v)
    elif args.f:
        file_path = os.path.abspath(args.f)
        final_digest = sa.hash_file(file_path, args.v)
        if not final_digest:
            raise SystemExit('The file ' + file_path + ' was not found.')
    else:
        raise SystemExit('Enter an argument to hash (-s for string and -f for file).\n'
                         'Use -h option to show all possible arguments.')

    # Show source and the final digest
    source = args.s if args.s else args.f
    print('string|filename: ' + source)
    print('SHA1 digest: ' + final_digest)
