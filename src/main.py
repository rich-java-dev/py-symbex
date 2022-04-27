from os import path
import argparse
from symbex import FileParser


parser = argparse.ArgumentParser('Static Parser - ')
parser.add_argument('--filename', '--f', '-f',
                    default="test-cases/testboolfunc.py")
args = parser.parse_args()
print(args)


# sanitize input...
filename: str = args.filename

# parse file

parser: FileParser = FileParser(filename)
# parser.print_ast()
parser.parse()
parser.results()
