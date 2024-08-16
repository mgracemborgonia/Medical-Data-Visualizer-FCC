import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("medical_examination.csv")
#print(df)

df['overweight'] = df['weight'] / np.square(df['height'] / 100)
df['overweight'] = df['overweight'].apply(lambda a: 1 if a > 25 else 0)
#print(df['overweight'])

#df['cholesterol'] = df['cholesterol'].apply(lambda a: 1 if a > 1 else 0)
#df['gluc'] = df['gluc'].apply(lambda a: 1 if a > 1 else 0)
df['cholesterol'] = df['cholesterol'].apply(lambda a: 0 if a == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda a: 0 if a == 1 else 1)
#print(df['gluc'])
#print(df['cholesterol'])

def draw_cat_plot():
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    df_cat = df_cat.groupby(['cardio','variable','value'])
    df_cat = df_cat.size()
    df_cat = df_cat.reset_index(name="total")
    
    #print(df_cat)

    fig = sns.catplot(data=df_cat, x='variable', y='total', kind='bar', hue='value', col='cardio')
    fig = fig.figure

    fig.savefig('catplot.png')
    return fig

def draw_heat_map():
    height_lo = df['height'] >= df['height'].quantile(0.025)
    height_hi = df['height'] <= df['height'].quantile(0.975)
    weight_lo = df['weight'] >= df['weight'].quantile(0.025)
    weight_hi = df['weight'] <= df['weight'].quantile(0.975)
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi']) & (height_lo)& (height_hi) & (weight_lo) & (weight_hi)]
    #print(df_heat['height'])
    #print(df_heat['weight'])

    corr = df_heat.corr()
    #print(corr)

    mask = np.triu(np.ones_like(corr, subok=True))
    #print(mask)

    fig, ax = plt.subplots(figsize=(13,13))

    ax = sns.heatmap(corr, mask=mask, linewidths=0.3, vmin=-0.2, vmax=0.3, center=0, annot=True, square=True, fmt='.1f', cbar_kws={'shrink': 0.6})

    fig.savefig('heatmap.png')
    return fig
