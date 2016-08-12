#!/usr/bin/env python

import sys
import csv
import HTSeq
import argparse

from collections import defaultdict


def parse_transcripts_reference(infile):
    transcripts = dict()

    with open(infile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        header = reader.next()
        for row in reader:
            transcripts[row[0]] = row[1]

    return transcripts


def parse_gtf(infile):
    gene_dict = defaultdict(lambda: defaultdict())
    gtf_file = HTSeq.GFF_Reader(infile, end_included=True)
    for feature in gtf_file:
        if feature.type == "transcript":
            gene_dict[feature.attr['transcript_id']]['gene_id'] = feature.attr['gene_id']
            if 'ref_gene_name' in feature.attr:
                gene_dict[feature.attr['transcript_id']]['gene_name'] = feature.attr['ref_gene_name']
            else:
                gene_dict[feature.attr['transcript_id']]['gene_name'] = feature.attr['gene_id']

    return gene_dict


def parse_ballgown_results(infile, transcript_dict, fold_changes, gene_dict):
    stats = defaultdict(dict)
    with open(infile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='"')
        header = reader.next()
        for row in reader:
            stats[transcript_dict[row[1]]]['pval'] = row[2]
            stats[transcript_dict[row[1]]]['qval'] = row[3]
            stats[transcript_dict[row[1]]]['fc'] = fold_changes[transcript_dict[row[1]]]
            stats[transcript_dict[row[1]]]['gene_id'] = gene_dict[transcript_dict[row[1]]]['gene_id']
            stats[transcript_dict[row[1]]]['gene_name'] = gene_dict[transcript_dict[row[1]]]['gene_name']

    return stats


def parse_fold_changes(infile, transcript_dict):
    fold_changes = dict()

    with open(infile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='"')
        header = reader.next()
        for row in reader:
            fold_changes[transcript_dict[row[2]]] = row[3]

    return fold_changes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file with differential expression results from ballgown '
                                              'stattest', required=True)
    parser.add_argument('-g', '--gtf', help="GTF file", required=True)
    parser.add_argument('-o', '--output', help='Output file name', required=True)
    parser.add_argument('-t', '--transcripts', help="File that links ballgown internal transcript IDs to transcript "
                                                    "names", required=True)
    parser.add_argument('-f', '--fold_change', help="Optional file with fold change information to draw from. "
                                                    "Required when fold change information is not in the stattest "
                                                    "results due to custom models used in Ballgown")

    args = parser.parse_args()

    sys.stdout.write("Parsing Transcripts file to create transcripts dictionary\n")
    transcript_dict = parse_transcripts_reference(args.transcripts)

    sys.stdout.write("Reading file with fold change data\n")
    fold_changes = parse_fold_changes(args.fold_change, transcript_dict)

    sys.stdout.write("Parsing GTF file to construct transcript gene dictionary\n")
    gene_dict = parse_gtf(args.gtf)

    sys.stdout.write("Parsing main ballgown result set\n")
    stats = parse_ballgown_results(args.input, transcript_dict, fold_changes, gene_dict)

    sys.stdout.write("Filtering based on FDR QValue and outputting to {}\n".format(args.output))
    with open(args.output, 'w') as outfile:
        outfile.write("Transcript\tGeneID\tGene Name\tFC\tPValue\tQValue (FDR Adjusted P-value)\n")
        for transcript in stats:
            if stats[transcript]['qval'] <= 0.05:
                outfile.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(transcript, stats[transcript]['gene_id'],
                                                                stats[transcript]['gene_name'],
                                                                stats[transcript]['fc'], stats[transcript]['pval'],
                                                                stats[transcript]['qval']))

