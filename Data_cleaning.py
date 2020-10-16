# -*- coding: utf-8 -*-

"""

All three databases (Military Pop and GDP) should be cleanable with similar functions,
All three from same source, and share the same formatting

"""

#%%

"""

Import Section

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


wd=os.path.abspath('C://Users//Mariko//Documents//GitHub//military-gdp')
os.chdir(wd)

#%%%%

"""
Utility Functions

"""

def double_check():
    response=input("Confirm? (Y/N)\n")
    if response.lower()=='y' or response.lower()=='yes':
        return 1
    else:
        return 0



#%%%%

"""

Load Raw data and inspect

"""



raw_gdp = 'API_NY.GDP.MKTP.CD_DS2_en_excel_v2_1345121.xls'
raw_pop = 'API_SP.POP.TOTL_DS2_en_excel_v2_1345100.xls'
raw_mil = 'API_MS.MIL.XPND.CD_DS2_en_excel_v2_1346213.xls'
raw_data=[raw_gdp, raw_pop, raw_mil]
data_order=['GDP', 'POP', 'MIL']


def init_df(file_name):
    """
    Load the df, check and drop unneeded columns
    """
    
    df=pd.read_excel(file_name, sheet_name='Data', header=3)
    #print(df.head(10))
    
    #Make sure there's nothing needed in the indicator cols
    for col in ['Indicator Name', 'Indicator Code']:
        if len(df[col].unique()) >1:
            print(f'Multiple distinct entries found in {col}. Delete?' )
            print(df[col].unique())
            double_check()
            if double_check==1:
                del df[col]
        else: 
            del df[col]
     
    print('Import complete' )    
    return df


def filter_for_country(df):
    """
    
    Filter only for countries of interest:
        China, Russia, Germany, UK, France, Italy, Iran, Saudi Arabia, Israel, S. Korea
    
    """
    
    #These are the exact names used by worldbank
    countries= ['China', 'Russian Federation', 'Germany', 'United Kingdom', 'France', 
                'Italy', 'Iran, Islamic Rep.', 'Saudi Arabia', 'Israel','Korea, Rep.']
    
    
    
    df_interest=df[df['Country Name'].isin(countries)]

    if len(countries)!=df_interest.shape[0]:
        raise ValueError("There is a mismatch between filtered countris and input list.")
    
    df_interest.reset_index(drop=True, inplace=True)
    
    return df_interest

        
#%%

"""

Run the functions to load and clean data

"""

data=[]

for i in raw_data:
    df= init_df(i)
    df=filter_for_country(df)
    data.append(df)   


#%%

"""
Need to find a span of years that has data in all dataframes for all countries.

"""
na_frame=[i.isna().sum(axis=0)[2:] for i in data]
na_frame2=pd.DataFrame(na_frame)

plt.figure(figsize=(11,2))
plt.bar(na_frame2.columns,na_frame2.sum(axis=0))
plt.title('Count of Missing Datapoints by Year')
plt.xticks(na_frame2.columns, na_frame2.columns, rotation='vertical')
plt.show()

# Result: From 1960-1992 there are at least 1 NaN in one of the datasets,
#         followed by a full dataset 1993-2017, then more NaNs 2018-2019.
#
#        Drop years<1993 and years>2017


#%%%


def df_extract_years(df, start_year, end_year):
    """
    Extract the years while keeping the label columns
    """
    if start_year >= end_year:
        raise ValueError('Please ensure start year is less than end year.')
    
    years= [str(i) for i in range(start_year, end_year+1)]
    years=['Country Name', 'Country Code']+years
    df=df.filter(years)
    
    return df


    
data=[df_extract_years(datum,2000, 2017) for datum in data]
    
#%%

#Put data in terms of billions

data[0].iloc[:,2:]=data[0].iloc[:,2:]/10**9
data[1].iloc[:,2:]=data[1].iloc[:,2:]/10**6
data[2].iloc[:,2:]=data[2].iloc[:,2:]/10**9




#%%
for i in range(3):
    data[i].to_csv(wd+'\\cleaned_data_'+data_order[i]+'.csv')



    
    
    
