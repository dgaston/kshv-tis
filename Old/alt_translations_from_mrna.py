import sys
import Bio
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--annotations', help="Input GFF file of annotations")
    parser.add_argument('-d', '--db', help="Input GFF file of annotations", default='annotations.db')
    args = parser.parse_args()

    alt_start_codons = ["CTG", "GTG"]
