import pandas as pd

df = pd.read_csv('../data/historical_emissions.csv')
df.drop(['ISO', 'Data source', 'Gas', 'Unit'], axis=1, inplace=True)

df_melted = pd.melt(df, id_vars=['Country', 'Sector'], var_name='Year', value_name='Value')
df_melted['Year'] = df_melted['Year'].astype(int)
df_pivoted = df_melted.pivot_table(index=['Country', 'Year'], columns='Sector', values='Value', aggfunc='sum')
df_pivoted.reset_index(inplace=True)
df_pivoted.columns.name = None

sum_df = df_pivoted.copy()
sum_df.drop(['Country', 'Year'], axis=1, inplace=True)
df_pivoted['Total'] = sum_df.sum(axis=1)

df_pivoted.fillna(0, inplace=True)

df_pivoted.to_csv("../data/formatted.csv", index=False)