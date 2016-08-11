#!/usr/bin/env python

import sys
import csv
import argparse
import plotly
import plotly.graph_objs as go

from collections import defaultdict
from collections import OrderedDict


def parse_expression_data(file):
    temp_values = dict()
    with open(file, 'r') as transscriptfile:
        reader = csv.reader(transscriptfile, dialect='excel-tab')
        header = reader.next()
        i = 0
        for row in reader:
            i += 1
            temp_values[row[5]] = float(row[11])

    sys.stdout.write("Parsed {} values\n".format(i))
    values = OrderedDict(sorted(temp_values.items(), key=lambda t: t[0]))

    return values


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file name.')

    args = parser.parse_args()

    data = defaultdict(lambda: defaultdict(OrderedDict))

    with open(args.input, 'r') as infile:
        reader = csv.reader(infile, dialect='excel-tab')
        header = reader.next()
        for row in reader:

            sys.stdout.write("Parsing data from file {}\n".format(row[1]))
            data[row[0]]['sample1'] = row[1]
            data[row[0]]['expression1'] = parse_expression_data(row[3])

            sys.stdout.write("Parsing data from file {}\n".format(row[2]))
            data[row[0]]['sample2'] = row[2]
            data[row[0]]['expression2'] = parse_expression_data(row[4])

        for comparison in data.keys():
            values1 = list()
            values2 = list()

            for transcript in data[comparison]['expression1']:
                values1.append(data[comparison]['expression1'][transcript])

            for transcript in data[comparison]['expression2']:
                values2.append(data[comparison]['expression2'][transcript])

            trace = go.Scatter(
                x=values1,
                y=values2,
                mode='markers'
            )

            layout = go.Layout(title="Correlation between samples for: {}".format(comparison),
                               xaxis=dict(
                                   title="{}".format(header[0])
                               ),
                               yaxis=dict(
                                   title="{}".format(header[1])
                               ))

            figure = go.Figure(data=[trace], layout=layout)

            plotly.offline.plot(figure, filename="{}_correlations.html".format(comparison))
