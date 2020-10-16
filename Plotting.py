# -*- coding: utf-8 -*-
#%%

"""

Load the cleaned data from file
    Data cleaned using Data_cleaning.py

"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import numpy as np


wd=os.path.abspath('C://Users//Mariko//Documents//GitHub//military-gdp')
os.chdir(wd)


data_gdp=pd.read_csv(wd+'\\cleaned_data_GDP.csv', index_col=0)
data_pop=pd.read_csv(wd+'\\cleaned_data_POP.csv', index_col=0)
data_mil=pd.read_csv(wd+'\\cleaned_data_MIL.csv', index_col=0)



#Rename the countries to their more common names

data_gdp.replace({'Russian Federation':'Russia','Iran, Islamic Rep.':'Iran', 'Korea, Rep.': 'South Korea'}, inplace=True)
data_pop.replace({'Russian Federation':'Russia','Iran, Islamic Rep.':'Iran', 'Korea, Rep.': 'South Korea'}, inplace=True)
data_mil.replace({'Russian Federation':'Russia','Iran, Islamic Rep.':'Iran', 'Korea, Rep.': 'South Korea'}, inplace=True)


#%%


def basic_plot_1_cat(df, data_type):

    str_dict={'GDP':['Gross Domestic Product', 'GDP in Billions (USD)'], 
              'POP':['Population', 'Population in Millions (Total Estimated)'], 
              'MIL':['Military Expenditure', 'Expenditure in Billions (USD)']}
    
    
    
    plt.figure(figsize=(11,4))
    for i in range(10):
        plt.plot(df.columns[2:], df.iloc[i,2:])
    
    plt.title(str_dict[data_type][0])
    plt.ylabel(str_dict[data_type][1])
    plt.legend(df.iloc[:,0], bbox_to_anchor=(1.0, .9))



basic_plot_1_cat(data_gdp, 'GDP')
basic_plot_1_cat(data_mil, 'MIL')
basic_plot_1_cat(data_pop, 'POP')



#%%

def global_line_dollars(df_dollars, df_pop, dollar_type, mode='abs'):
    """
    Plots the GDP or Military Expenditure for all countries, as both absolute values and per capita

    """
    
    
    if mode=='abs':
            str_dict={'GDP':['GDP', 'GDP in Billions (USD)'], 
              'MIL':['Military Expenditure', 'Expenditure in Billions (USD)']}
            
            df_val=df_dollars.iloc[:,2:]
    else:
        str_dict={'GDP':['GDP per Capita', 'GDP per Capita in Billions (USD)'], 
                  'MIL':['Military Expenditure per Capita', 'Expenditure per Capita in Billions (USD)']}
        
        df_val=df_dollars.iloc[:,2:]/df_pop.iloc[:,2:]
    
    
    dollar_type=dollar_type.upper()
    
    
    plt.figure(figsize=(11,4))
    for i in range(10):
        plt.plot(df_val.columns[:], df_val.iloc[i,:])
    
    plt.title(str_dict[dollar_type][0])
    plt.ylabel(str_dict[dollar_type][1])
    plt.legend(df_dollars.iloc[:,0], bbox_to_anchor=(1.0, .9))
    



global_line_dollars(data_gdp, data_pop, 'GDP', 'abs')
global_line_dollars(data_gdp, data_pop, 'GDP', 'cap')

global_line_dollars(data_mil, data_pop, 'MIL', 'abs')
global_line_dollars(data_mil, data_pop, 'MIL', 'cap')

#%%


def mil_as_percent_gdp(df_mil, df_gdp):
    """
    Plot the Military expenditure as a percentage of GDP for all countries
    """
    
    str_dict=['Military Expenditure as a Fraction of GDP', '% GDP']
    
    
    df_percent=df_mil.iloc[:,2:]/df_gdp.iloc[:,2:]*100
    
    
    
    plt.figure(figsize=(11,4))
    for i in range(10):
        plt.plot(df_percent.columns[:], df_percent.iloc[i,:])
    
    plt.title(str_dict[0])
    plt.ylabel(str_dict[1])
    plt.legend(df_mil.iloc[:,0], bbox_to_anchor=(1.0, .9))
    

mil_as_percent_gdp(data_mil, data_gdp)


#%%


def single_country_metrics_plot(df_mil, df_gdp, df_pop, country_str, mode='abs'):
    """
    Make a lineplot with two axes to comapre GDP and Mil expenditure for one country at a time
    """

    try:
        df_mil=df_mil[df_mil['Country Name']==country_str]
        df_gdp=df_gdp[df_gdp['Country Name']==country_str]
        df_pop=df_pop[df_pop['Country Name']==country_str]
        
    except:
        raise ValueError('Country not found, please check spelling.')
        
    if mode=='abs':
        str_add='' 

    else:
        str_add=' per Capita'
        df_gdp.iloc[:,2:]=df_gdp.iloc[:,2:]/df_pop.iloc[:,2:]    
        df_mil.iloc[:,2:]=df_mil.iloc[:,2:]/df_pop.iloc[:,2:]    
        
        
    
    colours=('Gray', '#0165fc' )
    
    fig, ax1 = plt.subplots(figsize=(11,4))
    
    ax1.plot(df_gdp.columns[2:], df_gdp.iloc[0,2:], color=colours[0])
    ax1.set_ylabel(f'GDP{str_add} in Billions (USD)', color=colours[0])
    ax1.tick_params(axis='y', labelcolor=colours[0])
    
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel(f'Military Expenditure{str_add} in Billions (USD)', color=colours[1])  # we already handled the x-label with ax1
    ax2.plot(df_mil.columns[2:], df_mil.iloc[0,2:], color=colours[1])
    ax2.tick_params(axis='y', labelcolor=colours[1])
    
   

    plt.title(f'Comparison of GDP{str_add} and Military Expenditure{str_add}: {country_str}', fontsize=16)

    plt.show()


single_country_metrics_plot(data_mil, data_gdp, data_pop, 'Germany')
single_country_metrics_plot(data_mil, data_gdp, data_pop, 'China', 'cap')




#%%

def global_stack_dollars(df_dollars, df_pop, dollar_type, mode='abs'):
    """
    Plot the Military expenditure as a stacked plot, to get a feel of proportional spending
    """
    
    if mode=='abs':
            str_dict={'GDP':['GDP', 'GDP in Billions (USD)'], 
              'MIL':['Military Expenditure', 'Expenditure in Billions (USD)']}
            
            df_val=df_dollars.iloc[:,2:]
    else:
        str_dict={'GDP':['GDP per Capita', 'GDP per Capita in Billions (USD)'], 
                  'MIL':['Military Expenditure per Capita', 'Expenditure per Capita in Billions (USD)']}
        
        df_val=df_dollars.iloc[:,2:]/df_pop.iloc[:,2:]
    
    
    dollar_type=dollar_type.upper()
    
    bottom=df_val.iloc[0,:]*0
    plt.figure(figsize=(11,4))
    for i in range(10):
        plt.bar(df_val.columns[:], df_val.iloc[i,:], bottom=bottom)
        bottom=df_val.iloc[i,:]+bottom

    
    plt.title(str_dict[dollar_type][0])
    plt.ylabel(str_dict[dollar_type][1])
    plt.legend(df_dollars.iloc[:,0], bbox_to_anchor=(1.0, .9))
    



global_stack_dollars(data_gdp, data_pop, 'GDP', 'abs')
global_stack_dollars(data_gdp, data_pop, 'GDP', 'cap')

global_stack_dollars(data_mil, data_pop, 'MIL', 'abs')
global_stack_dollars(data_mil, data_pop, 'MIL', 'cap')

#%%


"""

Deltas in mil

"""


def changes_in_mil_spending(df_mil, year_start=2000, year_end=2017, country='all', mode='abs', span='annual', plot=True):
    """
    mode: Changes presented as change in absolute value, or as percent change, 'abs' or 'per'
    span: Timeframe to compare, can be annual or ends
    """

    #Input checking
    if year_start<=2000:
        year_start=2000
        
    if year_end>=2017:
        year_end=2017
        
    if mode=='abs':
        str_add='in Billions (USD)' 
    elif mode=='per':
        str_add='in Percent Change'
        
    #Year Filter
    if span == 'annual':
        years_keep=[str(i) for i in range(year_start-1, year_end+1)]
        years_keep=['Country Name', 'Country Code']+years_keep
        df_mil=df_mil.filter(years_keep, axis=1)
    elif span == 'ends':        
        years_keep=['Country Name', 'Country Code', str(year_start), str(year_end)]
        df_mil=df_mil.filter(years_keep, axis=1)
    else:
        raise ValueError('Please select span="annual" or "ends".')
        
    
    #Country filter
    if country !='all':
        if type(country)==list:
            df_mil=df_mil[df_mil['Country Name'].isin(country)]
        else:
            df_mil=df_mil[df_mil['Country Name'] == country ]

    #Dataframe for delta Spending set-up
    deltas=df_mil.copy()
    deltas.iloc[:,2:]=0
    
    #Calculate change in spending
    for year in range(3, df_mil.shape[1]):
        if mode.lower()=='abs':
            deltas.iloc[:, year]=df_mil.iloc[:, year]-df_mil.iloc[:, year-1]
        elif mode.lower()=='per':
            deltas.iloc[:, year]=(df_mil.iloc[:, year]-df_mil.iloc[:, year-1])/df_mil.iloc[:, year-1]*100
        else:
            raise ValueError('Please select mode="abs" or "per".')
    
    #Transform dataframe from wide to tall        
    deltas.drop(deltas.columns[2], axis=1, inplace=True) #Drop the first year (base before deltas start)
    melt_deltas=pd.melt(deltas, id_vars=['Country Name', 'Country Code'])
    
    if plot==False:
        return melt_deltas
    
    #Plot the data
    fig, ax= plt.subplots(figsize=(11,4))  
    sns.barplot(ax=ax, data=melt_deltas, hue='Country Name', x='variable', y='value',)
    ax.axhline(y=0, color='k')
    plt.legend(bbox_to_anchor=(1.0, .9))
    plt.ylabel(f'Change in Military Expenditure{str_add}')
    plt.xlabel('')
    plt.title(f'Changes in Military Spending from {year_start} to {year_end} {str_add}')
    
    if span=='ends':
        ax.set_xticks([])
        

    plt.show()
    
    
changes_in_mil_spending(data_mil, year_start=2012, country='all')
changes_in_mil_spending(data_mil, year_start=2012, country=['Russia', 'China'])
changes_in_mil_spending(data_mil, year_start=2001, country='Iran')

changes_in_mil_spending(data_mil, year_start=2015, country=['Russia', 'France'], span='ends')
changes_in_mil_spending(data_mil, year_start=2001, country='Iran', span='ends')
changes_in_mil_spending(data_mil, year_start=2015, country='all', span='ends')

changes_in_mil_spending(data_mil, year_start=2001,year_end=2004, country='all', mode='per', span='ends')
changes_in_mil_spending(data_mil, year_start=2001,year_end=2004, country='all', mode='abs', span='ends')
#%%





#%%
"""

Cartopy imports

"""


import cartopy
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.patheffects as PathEffects
from matplotlib.colors import Normalize
import matplotlib
from matplotlib import cm


#%%


def global_map_military_spending_delta(df_mil, year_start=2000, year_end=2017, mode='per'):
    """
    
    
    """
    
    #First, calculate the changes in spending using the previously defined changes_in_mil_spending() function.
    gradient_df=changes_in_mil_spending(df_mil, year_start=year_start,year_end=year_end, mode=mode,
                                          span='ends', country='all', plot=False)
    
    #Calculate the RBGA Values for each country's returned values
    
    #Find the max distance from 0 
    max_gradient=np.array([abs(gradient_df.value.min()), abs(gradient_df.value.max())]).max()
    #Create the normalized gradient centered on the zero between the max and negative max
    #Then output a color for each value
    norm = Normalize(vmin=-max_gradient, vmax=max_gradient)
    color_vals=[cm.coolwarm(norm(val),) for val in gradient_df.value ]
    
    #Filter the gradient data to remove unneded columns, and replace the values with the RGBA from above
    gradient_df=gradient_df.filter(['Country Name','value'])
    gradient_df['value']=color_vals
    
    #Make a list of countries for ease of reference
    country_list=gradient_df.iloc[:,0].tolist()
    
    #Load the appropriate global shapefiles
    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()
    country = next(countries)
    
    
    #Initialize the figure
    fig=plt.figure(figsize=(14, 10))
    
    
    
    #Load the map
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([180, -22, 0, 80],  crs=ccrs.PlateCarree())
    ax.add_feature(cartopy.feature.OCEAN,edgecolor='black')
    

    
    #Loop through the countries in the reader, and add to map if relevant
    for country in countries:
        if country.attributes['NAME'] in country_list :
            #Set the facecolour to our calculated value
            colour_calc=gradient_df[gradient_df['Country Name']==country.attributes['NAME']].iloc[0,1]
            ax.add_geometries(country.geometry, ccrs.PlateCarree(), facecolor=colour_calc, edgecolor='black')
            #Add text near the center of each country (offset for legibility)
            x = country.geometry.centroid.x        
            y = country.geometry.centroid.y
            ax.text(x, y+2, country.attributes['NAME'], color='White', size=10, ha='center', va='center', transform=ccrs.PlateCarree(), 
                    path_effects=[PathEffects.withStroke(linewidth=3, foreground="k", alpha=.8)])
       
   
    #Add an axis for Israel - It needs a zoomed-in window or you can't see it.
    ax2 = fig.add_axes([0.725, 0.3, 0.16, 0.16], projection=ccrs.PlateCarree(central_longitude=34), autoscale_on=False)
    ax2.set_extent([29, 40, 27, 35],  crs=ccrs.PlateCarree())
    ax2.add_feature(cartopy.feature.OCEAN,edgecolor='black')
    
    #Need to reload the reader, as it does not loop around
    countries = reader.records()
    country = next(countries)
    
    #Loop to israel, and repeat the above process, but in the zoomed window
    for country in countries:
        if country.attributes['NAME'] == "Israel":
            colour_calc=gradient_df[gradient_df['Country Name']=='Israel'].iloc[0,1]
            ax2.add_geometries(country.geometry, ccrs.PlateCarree(), facecolor=colour_calc, edgecolor='black')
            x = country.geometry.centroid.x        
            y = country.geometry.centroid.y
            ax2.text(x+2.4, y, country.attributes['NAME'], color='White', size=11, ha='center', va='center', transform=ccrs.PlateCarree(), 
                    path_effects=[PathEffects.withStroke(linewidth=3, foreground="k", alpha=.8)])
       
    
    #Add stand-alone colourbar to show the direction of the gradient
    c_map_ax = fig.add_axes([0.91, 0.33, 0.01, 0.36])
    c_map_ax.axes.get_xaxis().set_visible(False)
    c_map_ax.axes.get_yaxis().set_visible(False)
    matplotlib.colorbar.ColorbarBase(c_map_ax, cmap='coolwarm', orientation = 'vertical')
    
    
    #Set the title
    if mode=='per':
        str_add='Percent'
    else:
        str_add='Absolute'
    
    ax.set_title(f'{str_add} Change in Military Expenditure from {year_start} to {year_end}', fontsize=16)
    
    plt.show()

#%%

global_map_military_spending_delta(data_mil, year_start=2000, year_end=2017, mode='per')


global_map_military_spending_delta(data_mil, year_start=2000, year_end=2017, mode='abs')


global_map_military_spending_delta(data_mil, year_start=2015, year_end=2017, mode='abs')




#%%

'France' in data_mil['Country Name'].to_list()
data_mil[data_mil['Country Name']=='zim']














































































