import csv
import os

import matplotlib.pyplot as plt

class HistogramifierFileNotFoundError(Exception):
    pass

class HistogramifierUnprocessableFileError(Exception):
    pass

class Histogramifier(object):
    """Turn data from a column of a source file into a simple histogram.

    """

    def __init__(self, file_path, column=0):
        self.acceptable_file_types = ('csv', 'xls')
        self.column = column
        self.data = None
        self.file_path = file_path
        self.file_type = None

    def detect_file_type(self):
        self.file_type = self.file_path.split(".")[-1]
        if self.file_type not in self.acceptable_file_types:
            raise HistogramifierUnprocessableFileError()

    def load_data_as_list(self):
        if self.file_type == 'csv':
            self.load_data_from_csv()
        elif self.file_type == 'xls':
            self.load_data_from_xls()

    def load_data_from_csv(self):
        with open(self.file_path, 'rbU') as f:
            reader = csv.reader(f)
            data = [float(fields[self.column]) for fields in reader]
        self.data = data

    def load_data_from_xls(self):
        try:
            from xlrd import open_workbook
        except ImportError:
            raise HistogramifierUnprocessableFileError(
                'Cannot process Excel file without xlrd module.')
        data = list()
        wb = open_workbook(self.file_path)
        s = wb.sheets()[0]
        for row in range(s.nrows):
            data.append(float(str(s.cell(row, self.column)).split(':')[-1]))
        self.data = data

    def histogramify(self):
        self.verify_file_exists()
        self.detect_file_type()
        self.load_data_as_list()
        self.set_output_file_path()
        self.plot()

    def plot(self):
        plt.hist(self.data)
        plt.savefig(self.output_file_path)
        plt.clf()

    def set_output_file_path(self):
        self.output_file_path = self.file_path.replace('.'+self.file_type,
                                                       '.png')

    def verify_file_exists(self):
        if not os.path.exists(self.file_path):
            raise HistogramifierFileNotFoundError()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('--column', type=int, default=0)
    args = parser.parse_args()

    h = Histogramifier(args.input_file, args.column)
    h.histogramify()

if __name__ == '__main__':
    import sys
    sys.exit(main())

    
