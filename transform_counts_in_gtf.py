#!/usr/bin/env python

import sys
import csv
import HTSeq
import argparse

from collections import defaultdict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input GTF name.')

    args = parser.parse_args()

    with open(args.input, 'r') as infile:
        reader = csv.reader(infile, dialect='excel-tab')
        header = reader.next()

        for row in reader:
            gtf_file1 = HTSeq.GFF_Reader(row[0], end_included=True)
            gtf_file2 = HTSeq.GFF_Reader(row[1], end_included=True)

            transcripts1 = dict()
            transcripts2 = dict()

            for feature in gtf_file1:
                if feature.type == "transcript":
                    transcripts1[feature.attr['transcript_id']] = feature.attr['FPKM']

            for feature in gtf_file2:
                if feature.type == "transcript":
                    transcripts2[feature.attr['transcript_id']] = feature.attr['FPKM']