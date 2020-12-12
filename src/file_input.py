#!/usr/bin/python3
import sys
import os
import warnings

import pandas
from output_excel import OverviewDataExcel
from output_csv import OverviewDataCSV, PerformanceDataCSV, EconomyDataCSV

from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


input_file = sys.argv[1]
output_file = sys.argv[2]
sheets = ['MATHCES', 'MAPS']

with open(input_file) as f:
    content = f.readlines()

urls = [line.strip() for line in content]

#url = ['https://www.vlr.gg/6797/gamelanders-vs-imperial-esports-copa-brmalls-tournament-grand-final/']

OverviewDataCSV(urls, output_file)
PerformanceDataCSV(urls, output_file)
EconomyDataCSV(urls, output_file)
