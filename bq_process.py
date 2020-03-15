import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import os

from sklearn.preprocessing import MinMaxScaler

def load(path, data):
    df = pd.read_csv(path)
    if data == 'country':
        df.columns = ['Actor1', 'Actor2', 'Actor2Type1','Actor2Type2','AvgTone','MonthYear','NumSources','Url']
    if data == 'mediaop':
        df.columns = ['Actor1',	'Actor2', 'Actor2Type1', 'Actor2Type2', 'AvgTone', 'MonthYear','NumSources' ,'Url']
    
    scaler = MinMaxScaler()
    df.AvgTone = scaler.fit_transform(np.float32(df.AvgTone).reshape(len(df), -1))
    # df.AvgTone = scaler.fit_transform([df.AvgTone])[0]
    # df.AvgTone = np.array(scaler.transform([df.AvgTone]))
    return df

def heatmap(df):
    sub_df = df[['Actor1', 'Actor2', 'AvgTone']]
    heatmap1_data = pd.pivot_table(sub_df, values='AvgTone', 
                     index=['Actor1'], 
                     columns='Actor2')
    ax = sns.heatmap(heatmap1_data)
    plt.show()

def opinionmap(df):
    sns.set(font_scale = 1)
    sub_df = df[['Actor2', 'AvgTone', 'MonthYear']]
    counts = sub_df['Actor2'].value_counts()
    sub_df = sub_df[sub_df['Actor2'].isin(counts[counts > 3].index)]

    heatmap1_data = pd.pivot_table(sub_df, values='AvgTone', 
                     index=['Actor2'], 
                     columns='MonthYear')
    ax = sns.heatmap(heatmap1_data, yticklabels=True)
    plt.show()

if __name__ == "__main__":
    path = os.path.join("data", "bq_country_country.csv")
    # path = os.path.join("data", "bq_mediaop_country.csv")
    df = load(path, "mediaop")
    heatmap(df)
    # opinionmap(df)
