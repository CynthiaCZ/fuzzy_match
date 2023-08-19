# fuzzy_match
This program uses FuzzyWuzzy, a fuzzy string-matching program in Python, to compare E-commerce products and brand names. It aims to identify matches and discrepancies between a renowned Singaporean online shopping site and its competing platform. For each entry in the competitor's dataset, the program outputs the top matches along with their similarity scores and prices. On average, the top five matches exhibit an accuracy rate exceeding 90%, proving it highly effective in identifying assortment and pricing gaps between the two companies.

## Packages and Versions
python 3.11.0\
numpy 1.15.1\
pandas 3.6.6\
tqdm 4.64.1 \
fuzzywuzzy 0.18.0

## Files and Contents
├── data: internal data, not published\
├──── shopee.xlsx \
├──── lazada.xlsx \
├──── fuzzy_match.xlsx: output from fuzzy_match.py \
├──── fuzzy_match_w_price.xlsx: output from add_price.py \
├── fuzzy_match.py: perform fuzzy string matching and outputs a xlsx file with top 5 matches \
├── add_price.py: calculate and compare prices from both companies \
└── README.md
