#!/usr/bin/python3
import sys
import warnings

import pandas
from output_excel import PlayerDataExcel
from output_csv import PlayerDataCSV 

from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


input_file = sys.argv[1]
output_file = sys.argv[2]
output_type = sys.argv[3]

with open(input_file) as f:
    content = f.readlines()

urls = [line.strip() for line in content]

#url = ['https://www.vlr.gg/6797/gamelanders-vs-imperial-esports-copa-brmalls-tournament-grand-final/']


if output_type.lower() == 'csv':
    output_file = '../data/csv/' + sys.argv[2]
    PlayerDataCSV(urls, output_file)
elif output_file.lower() == 'excel':
    output_file =  = '../data/excel/' + sys.argv[2]
    PlayerDataExcel(urls, output_file, ['PLAYER DATA'])
else:
    print("** TIPO ERRADO DE ARQUIVO -- USE 'CSV' OU 'EXCEL' **")
    

'''OverviewDataCSV(url, output_file)
PerformanceDataCSV(url, output_file)
EconomyDataCSV(url, output_file)'''