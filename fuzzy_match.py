import pandas as pd
import numpy as np
from tqdm import tqdm
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

pd.set_option('display.max_columns', None)

lazada_excel = pd.read_excel('./data/lazada.xlsx', engine='openpyxl',)
lazada = pd.DataFrame(lazada_excel, columns=['skuId', 'Keyin Shopee skuid', 'Name','Brand Name', 'pdpUrl'])
lazada.columns = ['lazada_id', 'l_sku_id', 'l_name', 'l_brand', 'l_url']

shopee_excel = pd.read_excel('./data/shopee.xlsx', engine='openpyxl',)
shopee_excel = shopee_excel.rename(columns={'Unnamed: 29': 'url_1', 'Unnamed: 30': 'url'})
shopee = pd.DataFrame(shopee_excel, columns=['sku_id', 'Item_Name', 'global_brand', 'url'])
shopee.columns = ['s_sku_id', 's_name', 's_brand', 's_url']

# calculated fuzzywuzzy score on manually matched 123 rows
matched = lazada.merge(shopee, on = 'sku_id')
matched['fuzz_WRatio'] = matched.apply(lambda row: fuzz.token_set_ratio(row['l_name'], row['s_name']), axis=1)
matched['fuzz_WRatio'].mean()
# mean weighted ratio of manually matched rows is 88.18

### function to get top n matches, default 5
def get_top_matches(row, choices, selected_columns, num_matches=5):
    brand_choices = choices[choices['s_brand'].apply(lambda x: fuzz.token_set_ratio(row['l_brand'], x) >= 80)]
    matches = process.extract(row['l_name'], brand_choices['s_name'], scorer=fuzz.token_sort_ratio, limit=num_matches)
    top_info = []
    
    for match in matches:
        matched_row = choices.iloc[match[2]]
        top_info.append(matched_row[selected_columns].tolist() + [match[1]])
    while len(top_info) < num_matches:
        top_info.append([None] * (len(selected_columns) + 1))
    top_results = [list(x) for x in zip(*top_info)]
    return pd.Series(top_results, index=selected_columns + ['similarity_score'])

selected_columns = ['s_name', 's_sku_id', 's_url']

# apply function to df
# tqdm tracks progress
tqdm.pandas()
lazada[selected_columns + ['similarity_score']] = lazada.progress_apply(
    lambda row: pd.Series(get_top_matches(row, shopee, selected_columns)),
    axis=1
)

# calculate accuracy
accuracy_top1 = lazada.apply(lambda row: row['l_sku_id'] == row['s_sku_id'][0], axis=1).sum()/len(lazada)
accuracy_top3 = lazada.apply(lambda row: row['l_sku_id'] in row['s_sku_id'][:3], axis=1).sum()/len(lazada)
accuracy_top5 = lazada.apply(lambda row: row['l_sku_id'] in row['s_sku_id'], axis=1).sum()/len(lazada)
print(accuracy_top1, accuracy_top3, accuracy_top5)
# top 5 accuracy is > 90%


lazada[['top1_sku', 'top2_sku', 'top3_sku', 'top4_sku', 'top5_sku']] = lazada['s_sku_id'].apply(lambda x: pd.Series(x))
lazada[['top1_name', 'top2_name', 'top3_name', 'top4_name', 'top5_name']] = lazada['s_name'].apply(lambda x: pd.Series(x))
lazada[['top1_url', 'top2_url', 'top3_url', 'top4_url', 'top5_url']] = lazada['s_url'].apply(lambda x: pd.Series(x))

lazada.to_excel('./data/manual_auto_compare.xlsx')

