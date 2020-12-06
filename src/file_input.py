#!/usr/bin/python3
import sys
import os
import warnings

import pandas
from output_excel import OverviewDataExcel

from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


input_file = sys.argv[1]
output_file = sys.argv[2]
sheets = ['MATHCES', 'MAPS']

with open(input_file) as f:
    content = f.readlines()

urls = [line.strip() for line in content]

OverviewDataExcel(urls, output_file, sheets)
