"""
Script to generate one-hot-encoding for given table

Ex. given table:
A France 20000
B England 30000
C India 40000
D France 30000
E India 60000


Convert it to: 
A 1 0 0 20000
B 0 1 0 30000
C 0 0 1 40000
D 1 0 0 30000
E 0 0 1 60000

One-hot encoding eliminates ordinality (meaning that Male and Female have equal preference but model can misunderstand it if male is labeled as 0 and female as 1), 
converts input to numbers that model can understand
"""
import pandas as pd 

def ohe(df, col_name):
    ohe_df = list()
    categories = set()
    for ct in df[col_name]:
        categories.add(ct)
    col_index = df.columns.get_loc(col_name)
    enc_cts = encode_categories(categories)
    for _, row in df.iterrows():
        row_list = row.tolist()
        updated_row = row_list[:col_index] + enc_cts[row_list[col_index]] + row_list[col_index+1:]
        ohe_df.append(updated_row)
    return ohe_df


def encode_categories(categories):
    n = len(categories)
    if n > 10:
        print(f"This is a bad choice for one-hot encoding")
    encoded_cts = dict()
    for _id, ct in enumerate(categories):
        enc_ct = list()
        for i in range(n):
            if i == _id:
                enc_ct.append(1)
            else:
                enc_ct.append(0)
        encoded_cts[ct] = enc_ct
    print(encoded_cts)
    return encoded_cts


df = pd.read_csv('titanic.csv')
op = ohe(df, 'Sex')
for i in range(10):
  print(op[i])