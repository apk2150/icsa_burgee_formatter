import difflib
import pandas as pd

mapping=pd.read_csv('file_name_mappings.csv')

df=pd.read_csv('test.csv')
print(mapping.head())

# df1 = DataFrame([[1,'one'],[2,'two'],[3,'three'],[4,'four'],[5,'five']], columns=['number', 'name'])
# df2 = DataFrame([['a','one'],['b','too'],['c','three'],['d','fours'],['e','five']], columns=['letter', 'name'])

# df2['name'] = df2['name'].apply(lambda x: difflib.get_close_matches(x, df1['name'])[0])
# df1.mer
# ge(df2)
df['png_name'] = df['school'].apply(lambda x: difflib.get_close_matches(x, mapping['school'],n=1,cutoff=0.1)[0])
joined=df.merge(mapping, left_on='png_name', right_on='school')
print(joined)

# joined=df.merge(mapping,left_on="school",)
# print(joined)
