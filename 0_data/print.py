import pandas as pd

abbreviations = pd.read_parquet('0_data/abbreviations.parquet')
print("len(abbreviations): ", len(abbreviations))
print(abbreviations)

data = pd.read_parquet('0_data/data.parquet')
print("len(data): ", len(data))
print(pd.concat([data[data['control'] == 1].sample(3), data[data['control'] == 0].sample(3)]))
