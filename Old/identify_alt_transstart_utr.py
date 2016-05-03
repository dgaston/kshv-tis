#!/usr/bin/env python

import sys
import pysam
import argparse
import gffutils


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', help="Annotations database", default='annotations.db')
    parser.add_argument('-g', '--genome', help="Reference Genome to retrieve sequence data from")
    args = parser.parse_args()

    sys.stdout.write("Loading reference genome {}\n".format(args.genome))
    genome = pysam.FastaFile(args.genome)

    sys.stdout.write("Loading database {}\n".format(args.db))
    db = gffutils.FeatureDB(args.db, keep_order=True)

    sys.stdout.write("Processing UTRs\n")
    for utr in db.features_of_type('UTR', order_by='start'):
        if len(utr.attributes['ID']) > 1:
            sys.stderr.write("WARNING: More than one ID listed for feature\n")
            sys.stderr.write("{}\n".format(utr))
            sys.exit()
        id = utr.attributes['ID'][0]
        temp = id.split(':')
        if temp[0] == 'UTR5':
            sequence = genome.fetch()
            sys.stdout.write("{}\t{}\t{}\t{}\n".format(id, utr[0], utr[3], utr[4]))
