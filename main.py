import pandas as pd
import datetime

chunksize = 100000
availability_status = "In Stock" # or "Out of Stock", or "Not Listed", etc.
filename = 'small_sample.csv'

chunks = pd.read_csv(filename, chunksize=chunksize)
summary = pd.DataFrame(columns=['ID', 'Report Date', 'Last Available', 'Availability', 'Title', 'RPC', 'Market', 'Store'])

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
                if (r['Last Available'].values[0] == "") or (datetime.datetime.strptime(r['Last Available'].values[0], '%Y-%m-%d') < \
                        datetime.datetime.strptime(row['REPORT_DATE'], '%Y-%m-%d')):
                    r['Last Available'].values[0] = row['REPORT_DATE']
            #elif row['AVAILABILITY'] == "Out of Stock":

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
            'Availability': 0,
            'Title': row['TRUSTED_PRODUCT_DESCRIPTION'],
            'RPC': row['TRUSTED_RPC'],
            'Market': row['MARKET'],
            'Store': row['ONLINE_STORE']
        }, ignore_index=True)

for index, row in summary.iterrows():
    total = 0
    for dic in row['Report Date']:
        for k, v in dic.items():
            if v == availability_status:
                total += 1
    row['Availability'] = total

summary.to_csv('adv2.csv')
