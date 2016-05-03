#!/usr/bin/env python

import sys
import argparse
import gffutils


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', help="Annotations database", default='annotations.db')
    parser.add_argument('-g', '--genome', help="Reference Genome to retrieve sequence data from")
    args = parser.parse_args()

    sys.stdout.write("Loading database {}\n".format(args.db))
    db = gffutils.FeatureDB(args.db, keep_order=True)

    sys.stdout.write("Processing UTRs\n")
    i = 0
    for utr in db.features_of_type('UTR', order_by='start'):
        i += 1
        print i
        print utr
