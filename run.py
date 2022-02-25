import argparse
import os, sys
from data_parse.parse import parse_flatfile


def parse_opt():

    parser = argparse.ArgumentParser()
    parser.add_argument('-ff', '--formatfile', type=str, help='path to formatfile')
    parser.add_argument('-df', '--datafile', type=str, help='path to datafile')

    try:
        opt = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    return opt


def run(opt):
    datafilename = opt.datafile
    formatfilename = opt.formatfile

    # relative path

    if not os.path.isfile(datafilename):
        print(f"{datafilename} not found.")
        sys.exit(0)

    if not os.path.isfile(formatfilename):
        print(f"{formatfilename} not found.")
        sys.exit(0)

    if not datafilename.endswith(".txt"):
        print(f"{datafilename} is not a txt file.")
        sys.exit(0)

    if not formatfilename.endswith(".csv"):
        print(f"{formatfilename} is not a csv file.")
        sys.exit(0)

    output = parse_flatfile(datafilename, formatfilename)
    print(output)




if __name__ == "__main__":

    opt = parse_opt()
    run(opt)