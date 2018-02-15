import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from datetime import datetime
import statsmodels.api as sm
import itertools
from sklearn import linear_model
plt.style.use('fivethirtyeight')

def analyser(data, maincate, subcategory1, subcategory3, subcategory4, subcategory5, subcategory6):
    if maincate == 'maincate1':
        return Daily_visit_count(data, subcategory1, subcategory3)
    elif maincate == 'maincate2':
        return cases_frequency(data, subcategory1, subcategory3)
    elif maincate == 'maincate3':
        return Average_time(data, subcategory1, subcategory3)
    elif maincate == 'maincate4':
        return Hour_of_day(data, subcategory1, subcategory3)
    elif maincate == 'maincate5':
        return top_package_sold_and_prediction(data, subcategory1, subcategory3)
    # elif maincate == 'maincate6':
    #     return special_hospital(data, maincate, subcategory1, subcategory3)
    # elif maincate == 'maincate7':
    #     return special_hospital(data, maincate, subcategory1, subcategory3)
    # elif maincate == 'maincate8':
    #     return special_hospital(data, maincate, subcategory1, subcategory3)
    # elif maincate == 'maincate9':
    #     return top_package_sold(data, subcategory1, subcategory3)    
    elif maincate == 'maincate10':
        return pkg_approval_and_rejection(data, subcategory4, subcategory5)
    elif maincate == 'maincate11':
        return pkg_uptake(data, subcategory4, subcategory5)
    elif maincate == 'maincate12':
        return top_packages(data, subcategory4, subcategory5)
    elif maincate == 'maincate13':
    	return visit_and_average_time(data, subcategory6)
    elif maincate == 'maincate14':
    	return visit_and_package_value(data, subcategory6)


def visit_and_package_value(data, ID):
    df_n = data.copy()
    df_n = df_n[df_n['Identity No']==ID]

    H_data = pd.DataFrame(df_n['Pkg Rate'])
    H_data.reset_index(drop=True, inplace=True)

    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27, forward=True)
    ax = sns.barplot(x=H_data['Pkg Rate'], y=H_data.index+1, orient="h")
    ax.set(xlabel='Rupee by packages', ylabel='No. of visit')
    return fig

def visit_and_average_time(data, ID):
    df_n = data.copy()
    df_n = df_n[df_n['Identity No']==ID]
    df_n['Adm Date'] = df_n['Adm Date'].astype(str)
    new = df_n[df_n['Adm Date'] != '-']
    new.reset_index(inplace=True)
    new['Adm Date'] = new['Adm Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

    new = new[new['Disch Date'] != '-']
    new.reset_index(inplace=True)
    new['Disch Date'] = new['Disch Date'].astype(str)
    new['Disch Date'] = new['Disch Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

    new['time_difference'] = abs((new['Disch Date']-new['Adm Date']).dt.days)
    H_data = pd.DataFrame(new['time_difference'])

    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27, forward=True)
    ax = sns.barplot(x=H_data.time_difference, y=H_data.index+1, orient="h")
    ax.set(xlabel='Average time(in days)', ylabel='No. of visit')
    return fig

def Daily_visit_count(data, subcategory1="All", subcategory3="Not"):
    if subcategory1 == "All":
        data = data
    else:
        data = data[data['Dist Name'] == subcategory1]
        
    if (subcategory3 == "Government Hospital") or (subcategory3 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory3]
    else:
        data = data
        
    data.loc[:,'year'] = data['TID No'].apply(lambda x: '20'+x[5:7])
    data.loc[:,'month'] = data['TID No'].apply(lambda x: x[3:5])
    data.loc[:,'day'] = data['TID No'].apply(lambda x: x[1:3])
    data.loc[:,'Time'] = data[['year', 'month', 'day']].apply(lambda x: '-'.join(x), axis=1)
    data.loc[:,'Time'] = data['Time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    data = data.sort_values(['Time'], ascending=[1])
    data = data['Time'].value_counts()
    data = data.sort_index()
    data = pd.DataFrame(data)

    y = data
    y = y['Time'].resample('MS').mean()
    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=(1, 1, 0),
                                    seasonal_order=(1, 0, 0, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

    results = mod.fit()

    # Get forecast 5 steps ahead in future
    pred_uc = results.get_forecast(steps=5)
    # Get confidence intervals of forecasts
    pred_ci = pred_uc.conf_int()
    fig, ax = plt.subplots()
    ax = y.plot(label='observed', figsize=(11.7, 8.27))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Patient count')

    plt.legend()
    return fig

def cases_frequency(data, subcategory1="All", subcategory3="Not"):
    if subcategory1 == "All":
        data = data.copy()
    else:
        data = data[data['Dist Name'] == subcategory1].copy()
        
    if (subcategory3 == "Government Hospital") or (subcategory3 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory3].copy()
    else:
        data = data.copy()
    
    data['Time'] = data['Time'].astype(str)
    data1 = data.sort_values(['Time'], ascending=[1])
    data1 = data1['Time'].value_counts()
    data1 = data1.sort_index()
    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27, forward=True)
    ax = data1.plot()
    return fig

def Hour_of_day(data, subcategory1="All", subcategory3="Not"):
    if subcategory1 == "All":
        data = data
    else:
        data = data[data['Dist Name'] == subcategory1]
        
    if (subcategory3 == "Government Hospital") or (subcategory3 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory3]
    else:
        data = data
        
    df_n = data.copy()
    df_n['Admission Time'] = df_n['Admission Time'].astype(str)
    new = df_n[df_n['Admission Time'] != '-'].copy()
    new.reset_index(inplace=True)

    new['Admission Time'] = new['Admission Time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    new['hour'] = new['Admission Time'].dt.hour
    new['minute'] = new['Admission Time'].dt.minute
    time = new['hour'].value_counts()

    x = pd.DataFrame(time.index)
    y = pd.DataFrame(time.values)
    df = pd.concat([x,y], axis=1)
    df.columns = ['hour', 'freq']
    df['hour'][23] = 24
    df.sort_values('hour')

    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27, forward=True)
    ax = sns.barplot(x="hour", y="freq", data=df)
    ax.set(xlabel='hour of the day', ylabel='freq')
    return fig

def Average_time(data, subcategory1, subcategory3):
    if subcategory1 == "All":
        data = data
    else:
        data = data[data['Dist Name'] == subcategory1]
        
    if (subcategory3 == "Government Hospital") or (subcategory3 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory3]
    else:
        data = data    

    #data["Adm Date"] = data["Adm Date"].values[::-1]
    data = data[data['Disch Date'] != '-']
    data['Disch Date'] = pd.to_datetime(data['Disch Date'], format = '%Y-%m-%d %H:%M:%S')
    data = data[data['Adm Date'] != '-']
    data['Adm Date'] = pd.to_datetime(data['Adm Date'], format = '%Y-%m-%d %H:%M:%S')

    data['time_difference'] = abs((data['Disch Date']-data['Adm Date']).dt.days)
    H_data = data[['year','month','time_difference']]
    H_data = H_data.groupby(['year','month'], as_index=False)['time_difference'].mean()

    if H_data.loc[H_data.shape[0]-1,'month'] == 12:
        year = (H_data.loc[H_data.shape[0]-1,'year']) + 1
    else:
        year = H_data.loc[H_data.shape[0]-1,'year']

    nextmonth = (H_data.loc[H_data.shape[0]-1,'month']%12) + 1


    # model
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(H_data[['year','month']], H_data['time_difference'])

    H_data.loc[H_data.shape[0],['year','month','time_difference']] = [year,nextmonth,0]
    pred = regr.predict(H_data.loc[H_data.shape[0]-1,['year','month']].values.reshape(1,-1) )
    H_data.loc[H_data.shape[0]-1,'time_difference'] = pred
    H_data['year'] = H_data['year'].astype(int)
    H_data.loc[H_data.shape[0]-1,'year'] = 'prediction'


    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)
    ax = sns.barplot(x="month", y="time_difference", hue='year', data=H_data)
    ax.set(xlabel='month', ylabel='Mean time spent')
    ax.text(0.5, 1, subcategory3, ha='center', va='center', transform=ax.transAxes, fontsize=20)
    return fig
    
def special_hospital(data, maincate, subcategory1="All", subcategory3="Not"):
    if subcategory1 == "All":
        data = data
    else:
        data = data[data['Dist Name'] == subcategory1]
        
    if (subcategory3 == "Government Hospital") or (subcategory3 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory3]
    else:
        data = data
        
    general_disease = ['General Ward(per day):Unspecified -  Description of ailment to be written.',
    'General Ward (Two Days):Unspecified -  Description of ailment to be written.',
    'General Ward (Three Days):Unspecified -  Description of ailment to be written.',
    'General Ward (Ten Days):Unspecified -  Description of ailment to be written.',
    'General Ward (Six Days):Unspecified -  Description of ailment to be written.',
    'General Ward (Seven Days):Unspecified -  Description of ailment to be written.',
    'General Ward (One Day):Unspecified -  Description of ailment to be written.',
    'General Ward (Nine Days):Unspecified -  Description of ailment to be written.',
    'General Ward (Four Days):Unspecified -  Description of ailment to be written.',
    'General Ward (Five Days):Unspecified -  Description of ailment to be written.',
    'General Ward (Eight Days):Unspecified -  Description of ailment to be written.',
              ]
    renal_dialysis_disease = ['Nephroureterectomy for Transitional Cell Carcinoma of renal pelvis (one side)',
    'Laproscopic surgery for kidney & supra renal any type',
    'Splenorenal Anastomosis', 'Splenectomy - For -  Trauma',
    'Maintenance Hemodialysis (Mhd) (With Inj. Erythropoetine With Inj. Iron) –Per Dialysis.',
    'Brachiocephalic Av Fistula For Hemodialysis',
    'AV Shunt for dialysis', 'Aural polypectomy'
                             ]

    cardiac_disease = ['Reimplanation  of Urethra', 'Refractory Cardiac Failure']

    natal_disease = ['Special Pkg for Neo Natal Care (Babies admitted with mild-moderate respiratory distress, Infections/sepsis with no major complications, Prolonged/persistent jaundice, Assisted feeding for low birth weight - babies (<1800 gms), Neonatal seizures)',
    'Nephrectomy', 'neonatal jaundice #',
    'Basic Package for Neo -  Natal Care (Package for Babies admitted for short term care for conditions like: Transient tachypnoea of newborn, Mild birth asphyxia, Jaundice requiring phototherapy, Hemorrhagic disease of newborn, Large for date',
    'Advanced Pkg for - Neo Natal Care (Low birth weight babies <1500 gm and all babies admitted with complications like Meningitis, Severe respiratory distress - Shock, Coma, Convulsions or Encephalopathy, Jaundice requiring exchange transfusion, NEC)'
    ]

    if maincate == "maincate5":
        disease_type = general_disease
    elif maincate == "maincate6":
        disease_type = renal_dialysis_disease
    elif maincate == "maincate7":
        disease_type = cardiac_disease    
    elif maincate == "maincate8":
        disease_type = natal_disease

    data = data.copy()
    data = data.loc[data['Pkg Name'].isin(disease_type)]  # change disease list name to get results for other diseases
    data = data[['Hosp Name','Pkg Name']]
    data['freq'] = np.ones((data.shape[0],), dtype=np.int)
    data = data.groupby(['Hosp Name'], as_index=False)['freq'].sum()
    data = data.sort_values(['freq'], ascending=False).reset_index(drop=True)
    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27, forward=True)
    ax = sns.barplot(x="freq", y="Hosp Name", orient="h", data=data)
    ax.set(xlabel='cases frequency', ylabel='Hospital Name')
    return fig

def top_package_sold_and_prediction(dataframe, subcategory1, subcategory3):
    # get next month
    table = dataframe[dataframe['year'] == np.max(dataframe['year'])]
    nextmonth = (np.max(table['month']) % 12) + 1
    
    # slice by month
    dataframe['year'] = dataframe['year'].astype(int)
    lessdata = dataframe[dataframe['year'] < max(dataframe['year'])]
    currentdata = dataframe[dataframe['year'] == max(dataframe['year'])]
    currentdata = currentdata[currentdata['month'].astype(int) <= int(subcategory1)]
    data = pd.concat([currentdata, lessdata], axis=0)

    # slice by hospital
    if (subcategory3 == "Government Hospital") or (subcategory3 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory3]
    else:
        data = data

    data['Pkg Rate'] = data['Pkg Rate'].astype(int)
    newdata = data[data['month'].astype(int) == int(subcategory1)].copy()
    unique, counts = np.unique(newdata['Pkg Code'], return_counts=True)
    unique_packages = pd.DataFrame(np.asarray((unique, counts)).T)
    ndata = unique_packages[unique_packages[1] > 0].sort_values(by=1, ascending=False)
    ndata.reset_index(drop=True, inplace=True)
    package = ndata[0][0]

    data = data[data['Pkg Code'] == package].copy()
    table = data.groupby(['year','month'], as_index=False)['Pkg Rate'].sum()
    table['year'] = table['year'].astype(int)
    table['month'] = table['month'].astype(int)

    if int(subcategory1) == table.loc[table.shape[0]-1,'month'] == 12:
        year = (table.loc[table.shape[0]-1,'year']) + 1
    else:
        year = table.loc[table.shape[0]-1,'year']


    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(table[['year','month']], table['Pkg Rate'])

    table.loc[table.shape[0],['year','month','Pkg Rate']] = [year,nextmonth,0]
    pred = regr.predict(table.loc[table.shape[0]-1,['year','month']].values.reshape(1,-1) )
    table.loc[table.shape[0]-1,'Pkg Rate'] = pred
    table.loc[table.shape[0]-1,'year'] = 'prediction'


    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)
    ax = sns.barplot(x="month", y="Pkg Rate", hue='year', data=table)
    ax.set(xlabel='month', ylabel='Rupee value of package sold')
    ax.text(0.5, 1, package, ha='center', va='center', transform=ax.transAxes, fontsize=20)
    return fig

def pkg_approval_and_rejection(data, subcategory4, subcategory5):    
    # get next month
    table = data[data['year'] == np.max(data['year'])]
    next_month = (np.max(table['month']) % 12) + 1

    data = data[data['Pkg Name'] == subcategory4].copy()

    if (subcategory5 == "Government Hospital") or (subcategory5 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory5]
    else:
        data = data
        
    # see most common used Packages
    data['Present Pkg Status'].replace(['claimPackageApprovedandPaid', 'claimPackageApproved',
       'claimPackageRejected', 'claimRejectedByAnalyser',
       'claimQueryByAnalyser', 'claimApprovalPendingAtAnalyser',
       'claimapprovalpending', 'revertBackToAnalyserByClaim',
       'fundEnhancementPackageQuery', 'preAuthApproved',
       'preAuthPackageRejected', 'fundEnhancementPackageRejected',
       'fundEnhancementApprovalPending', 'preAuthApprovalPending',
       'preAuthPackageQuery', 'queryreplytodecesion'],["Accept","Accept","Reject","Reject","Reject","Reject","Reject","Reject","Reject","Accept","Reject","Reject","Reject","Reject","Reject","Reject"], inplace=True)

    ct = pd.crosstab(data["month"], data["Present Pkg Status"])#.apply(lambda r: r/r.sum(), axis=1)
    ct = ct.stack().reset_index().rename(columns={0:'value'})
    ct1 = ct[ct['Present Pkg Status'] == 'Accept'].reset_index(drop=True)
    # model
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(ct1['month'].values.reshape(-1,1), ct1['value'])

    ct1.loc[ct1.shape[0],['month','Present Pkg Status','value']] = [next_month,'Accept',0]
    pred = regr.predict(ct1.loc[ct1.shape[0]-1,['month']].values.reshape(1,-1) )
    ct1.loc[ct1.shape[0]-1,'value'] = np.abs(pred)
    ct1.loc[ct1.shape[0]-1,'month'] = str(next_month)+' month prediction'


    ct2 = ct[ct['Present Pkg Status'] == 'Reject'].reset_index(drop=True)
    # model
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(ct2['month'].values.reshape(-1,1), ct2['value'])

    ct2.loc[ct2.shape[0],['month','Present Pkg Status','value']] = [next_month,'Reject',0]
    pred = regr.predict(ct2.loc[ct2.shape[0]-1,['month']].values.reshape(1,-1) )
    ct2.loc[ct2.shape[0]-1,'value'] = np.abs(pred)
    ct2.loc[ct2.shape[0]-1,'month'] = str(next_month)+' month prediction'

    ct3 = pd.concat([ct1,ct2], axis=0).reset_index(drop=True)
    stacked = ct3.groupby(['month', 'Present Pkg Status']).value.sum().unstack(fill_value=0).apply(lambda r: r/r.sum(), axis=1)
    stacked = stacked.stack().reset_index().rename(columns={0:'value'})

    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)
    ax = sns.barplot(x=stacked['Present Pkg Status'], y=stacked['value'], hue=stacked['month'])
    ax.set(xlabel='Package Status', ylabel='Percentage')
    return fig

def pkg_uptake(data, subcategory4, subcategory5):
    data = data[data['Pkg Name'] == subcategory4].copy()

    if (subcategory5 == "Government Hospital") or (subcategory5 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory5]
    else:
        data = data

    ct = data.groupby(['year','month']).size().reset_index(name='counts')

    ct['year'] = ct['year'].astype(int)
    ct['month'] = ct['month'].astype(int)


    if ct.loc[ct.shape[0]-1,'month'] == 12:
        year = (ct.loc[ct.shape[0]-1,'year']) + 1
    else:
        year = ct.loc[ct.shape[0]-1,'year']

    nextmonth = (ct.loc[ct.shape[0]-1,'month']%12) + 1


    # model
    from sklearn import linear_model
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(ct[['year','month']], ct['counts'])

    ct.loc[ct.shape[0],['year','month','counts']] = [year,nextmonth,0]
    pred = regr.predict(ct.loc[ct.shape[0]-1,['year','month']].values.reshape(1,-1) )
    ct.loc[ct.shape[0]-1,'counts'] = pred
    ct.loc[ct.shape[0]-1,'year'] = 'prediction'


    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)
    ax = sns.barplot(x="month", y="counts", hue='year', data=ct)
    ax.set(xlabel='month', ylabel='Package uptake(monthly basis)')
    return fig

def top_packages(data, subcategory4, subcategory5):
    
    data = data[data['month'] == int(subcategory4)].copy()

    if (subcategory5 == "Government Hospital") or (subcategory5 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory5]
    else:
        data = data

    ct = data.groupby(['Pkg Code']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    ct.reset_index(drop=True, inplace=True)
    some_codes = ct.loc[:5,'Pkg Code']

    df = data.groupby(['Pkg Code','year']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)

    df = df[df['Pkg Code'].isin(some_codes)]
    df.reset_index(drop=True, inplace=True)

    for i in df['Pkg Code'].unique():
        ndf = df[df['Pkg Code']==i].sort_values(by='year', ascending=True).reset_index(drop=True)
        nextyear = ndf.loc[ndf.shape[0]-1,'year']+1
        
        # model
        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(ndf[['year']], ndf['counts'])

        ndf.loc[ndf.shape[0],['Pkg Code','year','counts']] = [ndf.loc[ndf.shape[0]-1,'Pkg Code'],nextyear,0]
        pred = regr.predict(ndf.loc[ndf.shape[0]-1,['year']].values.reshape(-1,1))

        df.loc[df.shape[0],['Pkg Code', 'year','counts']] = [ndf.loc[ndf.shape[0]-1,'Pkg Code'], nextyear, pred[0]]

    df['year'] = df['year'].astype(int)

    df['year'].replace(max(df['year']), str(max(df['year']))+" Predicted", inplace=True)

    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27, forward=True)
    ax = sns.barplot(x="counts", y="Pkg Code", hue='year', orient="h", data=df)
    ax.set(xlabel='counts', ylabel='Package Code')
    return fig





# <input type="radio" name="Maincategory" value="maincate5"> Hospital for general disease<br>
# <input type="radio" name="Maincategory" value="maincate6"> Hospital for renal_dialysis_disease<br>
# <input type="radio" name="Maincategory" value="maincate7"> Hospital for cardiac_disease<br>
# <input type="radio" name="Maincategory" value="maincate8"> Hospital for natal_disease<br>
