#!/usr/bin/env python

import argparse
import gffutils


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--annotations', help="Input GFF file of annotations")
    parser.add_argument('-d', '--db', help="Input GFF file of annotations", default='annotations.db')
    args = parser.parse_args()

    db = gffutils.create_db(args.annotations, dbfn=args.db, force=True, keep_order=True, merge_strategy='merge',
                            sort_attribute_values=True)
