import pandas as pd

filename = ""
chnksize = 5000
necessary_attr = ['TRUSTED_PRODUCT_DESCRIPTION',
                  'SUB_CATEGORY',
                  'ONLINE_STORE',
                  'DIMENSION7',
                  'DIMENSION8']
extra_attr = [
                  'TRUSTED_RPC',
                  'MARKET',
                  'AVAILABILITY',
                  'REPORT_DATE'
]

dframe = pd.read_csv(filename, chunksize=chnksize)
summary_table = pd.DataFrame(columns=[necessary_attr, extra_attr])

for chunk in dframe:
    summary_table.concat(dframe.filter([necessary_attr, extra_attr]), ignore_index=True)

summary_table['NEW_ID'] = summary_table['TRUSTED_RPC'].str.cat(summary_table[['ONLINE_STORE', 'MARKET']].values, sep='-')
summary_table['REPORT_DATE'] = pd.to_datetime(summary_table['REPORT_DATE'])
summary_table = summary_table.sort_values(['NEW_ID', 'REPORT_DATE'])
new_ids = list(summary_table['NEW_ID'].unique())

for ids in new_ids:
#    not_listed = dict(summary_table['AVAILABILITY'].value_counts())
    summary_table.drop_duplicates(subset= ['NEW_ID'], keep='last')

summary_table.reset_index(inplace =True)
del summary_table['index']


