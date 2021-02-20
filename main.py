import pandas as pd
import datetime

chunksize = 100000
filename = 'small_sample.csv'

chunks = pd.read_csv(filename, chunksize=chunksize)
summary = pd.DataFrame(columns=['ID', 'Report Date', 'Last Available', 'In Stock', 'Out of Stock', 'Not Listed', 'RPC',
                                'Description', 'Sub Category', 'Market', 'Store', 'Dimension7', 'Dimension8'])

for chunk in chunks:
    for index, row in chunk.iterrows():
        ID = str(row['TRUSTED_RPC']) + '-' + row['ONLINE_STORE'] + '-' + row['MARKET']

        if ID in summary['ID'].values:
            r = summary.loc[summary['ID'] == ID]
            dates = r['Report Date'].values[0]
            dates.append({
                'date': row['REPORT_DATE'],
                'availability': row['AVAILABILITY']
            })
            row['Report Date'] = dates

            if row['AVAILABILITY'] == "In Stock":
                if (r['Last Available'].values[0] == "") or (datetime.datetime.strptime(r['Last Available'].values[0], '%Y-%m-%d') < datetime.datetime.strptime(row['REPORT_DATE'], '%Y-%m-%d')):
                    r['Last Available'].values[0] = row['REPORT_DATE']

            summary.loc[summary['ID'] == ID] = r

        else:
            la = ""
            if row['AVAILABILITY'] == "In Stock":
                la = row['REPORT_DATE']
            summary = summary.append({
            'ID': ID,
            'Report Date': [
                {
                    'date': row['REPORT_DATE'],
                    'availability': row['AVAILABILITY']
                }
            ],
            'Last Available': la,
            'In Stock': 0,
            'Out of Stock': 0,
            'Not Listed': 0,
            'RPC': row['TRUSTED_RPC'],
            'Description': row['TRUSTED_PRODUCT_DESCRIPTION'],
            'Sub Category': row['SUB_CATEGORY'],
            'Market': row['MARKET'],
            'Store': row['ONLINE_STORE'],
            'Dimension7': row['DIMENSION7'],
            'Dimension8': row['DIMENSION8']
        }, ignore_index=True)

for index, row in summary.iterrows():
    for dic in row['Report Date']:
        for k, v in dic.items():
            if v == "In Stock":
                row['In Stock'] += 1
            elif v == "Out of Stock":
                row['Out of Stock'] += 1
            else:
                row['Not Listed'] += 1

del summary['Report Date']
summary.to_csv('adv2.csv')
