import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from datetime import datetime

def patient_traffic(data, subcategory1):
    if subcategory1 == "All":
        data = data
    else:
        data = data[data['District'] == subcategory1]

    data = data.sort_values(['Time'], ascending=[1])
    data = data['Time'].value_counts()
    data = data.sort_index()

    x = data.index
    x = pd.DataFrame(x)

    y = data.values
    y = pd.DataFrame(y)

    df = pd.concat([x,y], axis=1)
    df.columns = ['time', 'freq']
    df.head()

    df['time'] = df['time'].apply(lambda x: '20'+str(x))
    df['time'] = df['time'].apply(lambda x: x[:4]+' '+x[4:6]+' '+x[6:])
    df['time'] = df['time'].apply(lambda x: datetime.strptime(x, '%Y %m %d'))

    df['month'] = df['time'].dt.month
    df['day'] = df['time'].dt.weekday
    df['week'] = df['time'].dt.week
    df['year'] = df['time'].dt.year

    month = df.groupby(['year','month'], as_index=False)['freq'].sum()
    month['month'] = month['month'].replace([1,2,3,4,5,6,7,8,9,10,11,12], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27, forward=True)
    ax = sns.barplot(x="month", y="freq", data=month)
    ax.set(xlabel='month', ylabel='freq')
    return fig