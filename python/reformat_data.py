import pandas as pd

df = pd.read_csv('../data/historical_emissions.csv')
df.drop(['ISO', 'Data source', 'Gas', 'Unit'], axis=1, inplace=True)

df_melted = pd.melt(df, id_vars=['Country', 'Sector'], var_name='Year', value_name='Value')
df_melted['Year'] = df_melted['Year'].astype(int)
df_pivoted = df_melted.pivot_table(index=['Country', 'Year'], columns='Sector', values='Value', aggfunc='sum')
df_pivoted.reset_index(inplace=True)
df_pivoted.columns.name = None
df_pivoted['Total'] = df_pivoted['Total excluding LUCF']

df_pivoted.fillna(0, inplace=True)

df_pivoted = df_pivoted[df_pivoted['Country'] != 'European Union (27)']

total_2021 = df_pivoted[df_pivoted['Year'] == 2021][['Country', 'Total']]
top_5_countries = total_2021.nlargest(5, 'Total')['Country']
df_filtered = df_pivoted[df_pivoted['Country'].isin(top_5_countries)]

df_filtered.drop(['Land-Use Change and Forestry', 'Total excluding LUCF', 'Total including LUCF', 'Energy', 'Fugitive Emissions'], axis=1, inplace=True)

df_filtered.to_csv("../data/formatted.csv", index=False)