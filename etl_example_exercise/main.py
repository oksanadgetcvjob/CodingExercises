### Start solution here
import os
import pandas as pd

DATA = (('Input/data_source_1/sample_data.1.csv', ',', 'csv'),
        ('Input/data_source_1/sample_data.2.dat', '|', 'dat'),
        ('Input/data_source_2/sample_data.3.dat', ',', 'dat'))

import_function = {'csv': pd.read_csv, 'dat': pd.read_table}

result = pd.DataFrame()
for i, source in enumerate(DATA):
    df = import_function[source[2]](source[0], sep=source[1])
    df['source'] = i
    result = pd.concat([result, df])
if not os.path.isdir('Output'):
    os.mkdir('Output')
result.to_csv(r'Output/consolidated_output.1.csv', header=True)
