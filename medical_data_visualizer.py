import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set()

# Import data
df = pd.read_csv(os.getcwd() + "/medical_examination.csv")

# Add 'overweight' column
df['BMI'] = df.apply(lambda row: row['weight']/pow(row['height']/100.00, 2), axis=1)
df['overweight'] = df.apply(lambda row: 1 if row['BMI'] > 25 else 0, axis = 1)
df = df.drop(columns=['BMI'])


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = df.apply(lambda row: 0 if row['cholesterol'] == 1 else row['cholesterol'], axis = 1)
df['cholesterol'] = df.apply(lambda row: 1 if row['cholesterol'] > 1 else row['cholesterol'], axis = 1)
df['gluc'] = df.apply(lambda row: 0 if row['gluc'] == 1 else row['gluc'], axis = 1)
df['gluc'] = df.apply(lambda row: 1 if row['gluc'] > 1 else row['gluc'], axis = 1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, value_vars =['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = pd.melt(df, id_vars = ['cardio'], value_vars =['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    # Draw the catplot with 'sns.catplot()'
    p = sns.catplot(x="variable", col="cardio",
                data=df_cat,
                kind="count", legend=True, hue="value")
    p.set(xlabel='variable', ylabel='total')
    fig = p.fig

    #plt.show()
    
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df
    df_heat = df_heat[(df_heat['ap_lo'] <= df_heat['ap_hi'])
      & (df_heat['height'] >= df_heat['height'].quantile(0.025)) 
      & (df_heat['height'] <= df_heat['height'].quantile(0.975))
      & (df_heat['weight'] >= df_heat['weight'].quantile(0.025)) 
      & (df_heat['weight'] <= df_heat['weight'].quantile(0.975))]
    # Calculate the correlation matrix
    corr = df_heat.corr()



    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heatmap with 'sns.heatmap()'

    sns.heatmap(corr, mask=mask, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5},
            annot=True, fmt="0.1f")

    #plt.show()

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
