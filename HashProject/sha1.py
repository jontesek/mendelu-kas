#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys

from src.Sha1Algo import Sha1Algo

# Create the main object
sa = Sha1Algo()

# If the file was imported (as module).
def hash_text(input_text):
    return sa.hash_text(input_text)

def hash_file(file_path):
    return sa.hash_file(os.path.abspath(file_path))


# If the file was run directly (as script).
if __name__ == '__main__':
    # Module required for parsing of command line.
    import argparse

    # Save terminal encoding
    terminal_encoding = sys.stdin.encoding

    # Parse the incoming arguments: sha1.py -s <string> OR -f <filename> OR -v OR <input>
    parser = argparse.ArgumentParser(description='SHA1 in Python')
    parser.add_argument('-s', action='store', help='string to hash', metavar='<string>')
    parser.add_argument('-f', action='store', help='file to hash', metavar='<filename>')
    parser.add_argument('-v', action='store_true', help='verbose output - show some steps')
    parser.add_argument('input', nargs="?", help='string to hash')
    args = parser.parse_args()

    # Check arguments and call the correct hashing method.
    if args.input:
        final_digest = sa.hash_text(args.input, terminal_encoding, args.v)
        source = args.input
    elif args.s:
        final_digest = sa.hash_text(args.s, terminal_encoding, args.v)
        source = args.s
    elif args.f:
        file_path = os.path.abspath(args.f)
        final_digest = sa.hash_file(file_path, args.v)
        if not final_digest:
            raise SystemExit('The file ' + file_path + ' was not found.')
        source = args.f
    else:
        raise SystemExit('Enter an argument to hash (-s for string and -f for file).\n'
                         'Use -h option to show all possible arguments.')

    # Show source and the final digest.
    print('string|filename: ' + source)
    print('SHA1 digest: ' + final_digest)
