# Builds Bat/dashboard/data.js from the study CSVs (run from D:\My Research\ANimal)
import pandas as pd, json
Y = list(range(1992, 2023))
ntl = pd.read_csv('nighttime_light_USA_1992_2022_All.csv').pivot_table(index='FIPS', columns='year', values='mean')
z = pd.read_csv('Bat/US_Counties_All_Bat_NTL_Bivariate_Table_Corrected.csv').pivot_table(index='FIPS_Num', columns='year', values='z_score')
bat = pd.read_csv('Bat/US_Bat_with_pattern.csv', encoding='utf-8-sig').set_index('FIPS'); bat['PATTERN'] = bat.PATTERN.fillna('No Pattern Detected')
meta = pd.read_csv('Bat/BigBrownBat_Table_GWR.csv', usecols=['FIPS_Num','SQMI','POPULATION','year'], nrows=3200)
meta = meta[meta.year == 1992].drop_duplicates('FIPS_Num').set_index('FIPS_Num')
land = pd.read_csv('Bat/US_Counties_All_Bat_NTL_Bivariate_Table.csv', usecols=['GEOID','ALAND','Year'], nrows=3400)
land = land[land.Year == land.Year.iloc[0]].drop_duplicates('GEOID').set_index('GEOID').ALAND / 4046.8564224
pats = sorted(bat.PATTERN.unique())
r = lambda v, d: None if pd.isna(v) else round(float(v), d)
C = {}
for f, b in bat.iterrows():
    acres = land.get(f, meta.SQMI.get(f, float('nan')) * 640)
    C[f'{f:05d}'] = dict(
        n=b.NAME, s=b.STATE_ABBR, p=pats.index(b.PATTERN),
        a=[round(b.BigBrownBat), round(b.SilverHaired), round(b.LittleBrownMyot)],
        ar=None if pd.isna(acres) else round(acres),
        pop=None if f not in meta.index else int(meta.POPULATION[f]),
        l=[r(ntl.at[f, y], 3) if f in ntl.index else None for y in Y],
        z=[r(z.at[f, y], 3) if f in z.index else None for y in Y])
hh = pd.read_csv('Bat/High_High_Cluster_Counts.csv').values.tolist()
pp = pd.read_csv('Bat/bat_habitat_percentage_by_pattern.csv').round(3).values.tolist()
out = dict(years=Y, patterns=pats, counties=C, highHigh=hh, habitatByPattern=pp)
open('Bat/dashboard/data.js', 'w').write('const DATA=' + json.dumps(out, separators=(',', ':')) + ';')
print(len(C), sum(v['ar'] is None for v in C.values()), 'no area')
