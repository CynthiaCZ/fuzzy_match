import pandas as pd
import numpy as np

working_excel = pd.read_excel('./data/fuzzy_match.xlsx')
working = pd.DataFrame(working_excel)

lazada_excel = pd.read_excel('./data/lazada.xlsx')
lazada = pd.DataFrame(lazada_excel, columns=['skuId', 'ADGMV (SGD)', 'ADIS', 'Is Brand on Mart', 'Is SKU on Supermarket'])
lazada.columns = ['lazada_id', 'ADGMV', 'ADIS', 'Is Brand on Mart', 'Is SKU on Supermarket']
lazada = lazada.loc[lazada['Is Brand on Mart'] == 'Y - Is on Mart']
lazada = lazada.loc[lazada['Is SKU on Supermarket'] == 'Not Matched Yet']

shopee_excel = pd.read_excel('./data/shopee_w_price.xlsx')
shopee = pd.DataFrame(shopee_excel, columns=['sku_id', 'Item_Price'])
shopee.columns = ['s_sku_id', 's_price']
shopee = shopee.drop_duplicates()

# calculate price with ADGMV/ADIS
lazada['price_estimate'] = lazada['ADGMV']/lazada['ADIS']
lazada.drop(['ADIS', 'ADGMV'], axis=1, inplace=True)

working = working.merge(lazada, left_on='lazada_id', right_on='lazada_id')

working = working.merge(shopee, left_on='top1_sku', right_on='s_sku_id', how='left')
working.drop(['s_sku_id_y'], axis=1, inplace=True)
working.rename(columns={'s_price':'top1_price'}, inplace=True)

working = working.merge(shopee, left_on='top2_sku', right_on='s_sku_id', how='left')
working.drop(['s_sku_id'], axis=1, inplace=True)
working.rename(columns={'s_price':'top2_price'}, inplace=True)

working = working.merge(shopee, left_on='top3_sku', right_on='s_sku_id', how='left')
working.drop(['s_sku_id'], axis=1, inplace=True)
working.rename(columns={'s_price':'top3_price'}, inplace=True)

working = working.merge(shopee, left_on='top4_sku', right_on='s_sku_id', how='left')
working.drop(['s_sku_id'], axis=1, inplace=True)
working.rename(columns={'s_price':'top4_price'}, inplace=True)

working = working.merge(shopee, left_on='top5_sku', right_on='s_sku_id', how='left')
working.drop(['s_sku_id'], axis=1, inplace=True)
working.rename(columns={'s_price':'top5_price'}, inplace=True)


working.columns = ['Unnamed: 0', 'lazada_id', 'shopee_sku_(todo)', 'lazada_name', \
                   'lazada_brand', 'lazada_url', 'shopee_names', 'shopee_skus', \
                    'shopee_urls', 'similarity_score', 'top1_sku', 'top2_sku', \
                    'top3_sku', 'top4_sku', 'top5_sku', 'top1_name', \
                    'top2_name', 'top3_name', 'top4_name', 'top5_name', 'top1_url',\
                    'top2_url', 'top3_url', 'top4_url', 'top5_url', 'Is Brand on Mart', \
                    'Is SKU on Supermarket', 'lazada_price_estimate',\
                    'top1_price', 'top2_price', 'top3_price', 'top4_price', 'top5_price']

working.to_excel('./data/fuzzy_match_w_price.xlsx')
