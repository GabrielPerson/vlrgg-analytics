#!/usr/bin/python3
import sys
import warnings
import time


import pandas
from output_excel import OverviewDataExcel
from output_csv import OverviewDataCSV 

from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

## exec format: python3 file_input_overview.py ../urls/gamelanders.txt gamelanders_overview csv
start = time.time()

input_file = sys.argv[1]
output_file = sys.argv[2]
output_type = sys.argv[3]

with open(input_file) as f:
    content = f.readlines()

urls = [line.strip() for line in content]

#urls = ['https://www.vlr.gg/8298/team-vikings-vs-imperial-esports-ultimaster-aoc-main-event-grand-final/']


if output_type.lower() == 'csv':
    output_file = '../data/csv/' + output_file
    OverviewDataCSV(urls, output_file)
elif output_type.lower() == 'xls':
    output_file = '../data/excel/' + output_file
    OverviewDataExcel(urls, output_file, ['MATCHES', 'MAPS'])
else:
    print("** TIPO ERRADO DE ARQUIVO -- USE 'CSV' OU 'XLS' **")

print('It took {0:0.1f} seconds'.format(time.time() - start))