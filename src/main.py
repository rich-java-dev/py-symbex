import argparse
from asttools import FileParser

parser = argparse.ArgumentParser('Static Parser - ')
parser.add_argument('--filename', '--f', '-f',
                    default="test-cases/test-bools.py")
args = parser.parse_args()
print(args)


# sanitize input...
filename: str = args.filename

# parse file

parser: FileParser = FileParser(filename)
# parser.print_ast()
parser.parse()
parser.results()
