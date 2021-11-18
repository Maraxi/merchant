"""Main Method; allows the package to be called from the command line."""
import argparse

from merchant import merchants_guide

parser = argparse.ArgumentParser(
    description="Merchant's guide to the galaxy. Leave input file empty for interactive mode."
)
parser.add_argument(
    "inputfile",
    nargs="?",
    type=argparse.FileType("rt"),
    help="file containing conversation notes",
)
args = parser.parse_args()

guide = merchants_guide.Guide()


def generator():
    """Iterate over lines in the given file or acquire infinite user input."""
    if args.inputfile is not None:
        for line in args.inputfile:
            print(line, end="")
            yield line
    else:
        while True:
            yield input("> ")


for line in generator():
    if line[0] == ">":
        line = line[1:]
    elif line[0] == "#":
        continue
    if (result := guide.consume(line.strip())) is not None:
        print(result)
