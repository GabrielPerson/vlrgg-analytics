#!/usr/bin/python3
import sys
import warnings

import pandas
from output_excel import PerformanceDataExcel
from output_csv import PerformanceDataCSV 

from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


input_file = sys.argv[1]
output_file = sys.argv[2]
output_type = sys.argv[3]

with open(input_file) as f:
    content = f.readlines()

urls = [line.strip() for line in content]

#urls = ['https://www.vlr.gg/stats/?event_id=all&region=all&country=br&min_rounds=100&agent=viper&map_id=all&timespan=60d/']


if output_type.lower() == 'csv':
    output_file = '../data/csv/' + output_file
    PerformanceDataCSV(urls, output_file)
elif output_type.lower() == 'xls':
    output_file = '../data/excel/' + output_file
    PerformanceDataExcel(urls, output_file, ['MATCHES', 'MAPS'])
else:
    print("** TIPO ERRADO DE ARQUIVO -- USE 'CSV' OU 'XLS' **")
