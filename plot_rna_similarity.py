#!/usr/bin/env python

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
        for row in reader:
            temp_values[row[5]] = int(row[11])

    values = OrderedDict(sorted(temp_values.items(), key=lambda t: t[0]))

    return values


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file name.')

    args = parser.parse_args()

    data = defaultdict(lambda: defaultdict(dict))

    with open(args.input, 'r') as infile:
        reader = csv.reader(infile, dialect='excel-tab')
        header = reader.next()
        for row in reader:
            data[row[0]][header[0]] = parse_expression_data(row[2])
            data[row[0]][header[1]] = parse_expression_data(row[3])

        for comparison in data.keys():
            trace = go.Scatter(
                x=data[comparison][header[0]],
                y=data[comparison][header[1]],
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
