import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from datetime import datetime


def analyser(data, maincate, subcategory1, subcategory3, subcategory4, subcategory5):
    if maincate == 'maincate1':
        return Daily_visit_count(data, subcategory1, subcategory3)
    elif maincate == 'maincate2':
        return cases_frequency(data, subcategory1, subcategory3)
    elif maincate == 'maincate3':
        return Average_time(data, subcategory1, subcategory3)
    elif maincate == 'maincate4':
        return Hour_of_day(data, subcategory1, subcategory3)
    elif maincate == 'maincate5':
        return special_hospital(data, maincate, subcategory1, subcategory3)
    elif maincate == 'maincate6':
        return special_hospital(data, maincate, subcategory1, subcategory3)
    elif maincate == 'maincate7':
        return special_hospital(data, maincate, subcategory1, subcategory3)
    elif maincate == 'maincate8':
        return special_hospital(data, maincate, subcategory1, subcategory3)
    elif maincate == 'maincate9':
        return top_package_sold(data, subcategory1, subcategory3)    
    elif maincate == 'maincate10':
        return pkg_code(data, subcategory4, subcategory5)
    elif maincate == 'maincate11':
        return pkg_uptake(data, subcategory4, subcategory5)
    elif maincate == 'maincate12':
        return top_packages(data, subcategory4, subcategory5)


def Daily_visit_count(data, subcategory1="All", subcategory3="Not"):
    if subcategory1 == "All":
        data = data
    else:
        data = data[data['District'] == subcategory1]
        
    if (subcategory3 == "Government Hospital") or (subcategory3 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory3]
    else:
        data = data
        
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

def cases_frequency(data, subcategory1="All", subcategory3="Not"):
    if subcategory1 == "All":
        data = data.copy()
    else:
        data = data[data['District'] == subcategory1].copy()
        
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
        data = data[data['District'] == subcategory1]
        
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

def Average_time(data, subcategory1="All", subcategory3="Not"):
    if subcategory1 == "All":
        data = data
    else:
        data = data[data['District'] == subcategory1]
        
    if (subcategory3 == "Government Hospital") or (subcategory3 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory3]
    else:
        data = data
        
    df_n = data.copy()
    df_n['Adm Date'] = df_n['Adm Date'].astype(str)
    new = df_n[df_n['Adm Date'] != '-']
    new.reset_index(inplace=True)
    new['Adm Date'] = new['Adm Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

    new = new[new['Disch Date'] != '-']
    new.reset_index(inplace=True)
    new['Disch Date'] = new['Disch Date'].astype(str)
    new['Disch Date'] = new['Disch Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

    new['time_difference'] = abs((new['Disch Date']-new['Adm Date']).dt.days)
    H_data = new[['Hosp Name','time_difference']]
    H_data = H_data.groupby('Hosp Name', as_index=False)['time_difference'].mean()
    H_data = H_data.sort_values(['time_difference'], ascending=False).reset_index(drop=True)


    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27, forward=True)
    ax = sns.barplot(x="time_difference", y="Hosp Name", orient="h", data=H_data)
    ax.set(xlabel='Average time(in days)', ylabel='Hospital Name')
    return fig

def special_hospital(data, maincate, subcategory1="All", subcategory3="Not"):
    if subcategory1 == "All":
        data = data
    else:
        data = data[data['District'] == subcategory1]
        
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

def top_package_sold(data, subcategory1="All", subcategory3="Not"):
    if subcategory1 == "All":
        data = data
    else:
        data = data[data['District'] == subcategory1]
        
    if (subcategory3 == "Government Hospital") or (subcategory3 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory3]
    else:
        data = data
        
    n_data = data.groupby(['year','month'], as_index=False)['Pkg Rate'].sum()
    
    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)
    ax = sns.barplot(x="month", y="Pkg Rate", hue='year', data=n_data)
    ax.set(xlabel='month', ylabel='Rupee value of package sold')
    
    return fig

def pkg_code(data, subcategory4, subcategory5):
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

    ct = pd.crosstab(data["month"], data["Present Pkg Status"]).apply(lambda r: r/r.sum(), axis=1)
    stacked = ct.stack().reset_index().rename(columns={0:'value'})
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

    ct = data.groupby(['month', 'Pkg Code']).size().reset_index(name='counts')
    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27)
    ax = sns.barplot(x=ct['month'], y=ct['counts'])
    ax.set(xlabel='month', ylabel='uptake')
    return fig

def top_packages(data, subcategory4, subcategory5):
    data = data[data['month'] == 6].copy()

    if (subcategory5 == "Government Hospital") or (subcategory5 == "Private Hospital"):
        data = data[data['Hospital Type'] == subcategory5]
    else:
        data = data
        
    unique, counts = np.unique(data['Pkg Code'], return_counts=True)
    unique_packages = pd.DataFrame(np.asarray((unique, counts)).T)
    ndata = unique_packages[unique_packages[1] > 0].sort_values(by=1, ascending=False)
    ndata.columns = ['package_name', 'counts']
    fig, ax = plt.subplots()
    fig.set_size_inches(11.7, 8.27, forward=True)
    ax = sns.barplot(x="counts", y="package_name", orient="h", data=ndata[:10])
    ax.set(xlabel='counts', ylabel='package_name')
    return fig
