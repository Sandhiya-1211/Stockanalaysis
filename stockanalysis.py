import pandas as pd
import requests

git_url="https://api.github.com/repos/squareshift/stock_analysis/contents/"
response=requests.get(git_url)
# print(response.status_code)
data=response.json()
csv_files=[url['download_url'] for url in data if url['name'].endswith('.csv')]
csv_file=csv_files.pop()
metadata_df=pd.read_csv(csv_file)

new_list=[]
for url in csv_files:
    sym=url.split('/')[-1].replace(".csv","")
    df=pd.read_csv(url)
    df['Symbol']=sym
    new_list.append(df)

# print(new_list)
concat=pd.concat(new_list,ignore_index=True)
merge_df=pd.merge(concat,metadata_df, on='Symbol', how='left').reset_index(drop=True)
merge_df['timestamp']=pd.to_datetime(merge_df['timestamp'])
# print(merge_df)
filter_df=merge_df[(merge_df['timestamp']>="2021-01-01") & (merge_df['timestamp']<="2021-05-26")]
group=filter_df.groupby('Sector').agg({"open":"mean","high":"max","low":"min","close":"mean","volume":"mean"}).reset_index()
# print(group)
lst=["ENERGY & TRANSPORTATION","FINANCE"]
new_grp=group[group['Sector'].isin(lst)].reset_index(drop=True)
# print(new_grp)
new_grp.to_csv("SA.csv",index=False)
print("Completed successfully")