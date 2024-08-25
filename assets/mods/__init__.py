#!/usr/bin/python3
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="The purpose of this script")
    parser.add_argument("p1", metavar="alias", nargs="+", type=str, help="Description of the argument")
    return parser.parse_args()

def main():
    args = parse_arguments()
    print(args.p1)

if __name__ == "__main__":
    parse_arguments()
    main()
