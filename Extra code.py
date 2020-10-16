# -*- coding: utf-8 -*-

"""

Basic experimentation with the cartopy package
Identify that we need to change some of the country names

"""

country_list= ['China', 'Russian Federation', 'Germany', 'United Kingdom', 'France', 
            'Italy', 'Iran, Islamic Rep.', 'Saudi Arabia', 'Israel','Korea, Rep.']



shpfilename = shpreader.natural_earth(resolution='110m',
                                      category='cultural',
                                      name='admin_0_countries')



reader = shpreader.Reader(shpfilename)
countries = reader.records()
country = next(countries)



reader = shpreader.Reader(shpfilename)
countries = reader.records()



plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())


ax.add_feature(cartopy.feature.OCEAN,edgecolor='black')

for country in countries:
    if country.attributes['NAME'] in country_list:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(), facecolor=(0, 1, 0), edgecolor='black')
   
plt.rcParams["figure.figsize"] = (20,20)
plt.show()



#%%
"""

This section was used to identify the countries that needed adjustment 
from the countrys identifiers in the world bank names

"""


country_list= ['China', 'Russian Federation', 'Germany', 'United Kingdom', 'France', 
            'Italy', 'Iran, Islamic Rep.', 'Saudi Arabia', 'Israel','Korea, Rep.']

in_list=[]

reader = shpreader.Reader(shpfilename)
countries = reader.records()
country = next(countries)
for country in countries:
    in_list.append(country.attributes['NAME'])
    
need_fix=[left_out for left_out in country_list if left_out not in in_list ]    


country_list= ['China', 'Russia', 'Germany', 'United Kingdom', 'France', 
            'Italy', 'Iran', 'Saudi Arabia', 'Israel','South Korea']

#need_fix=[left_out for left_out in country_list if left_out not in in_list ]    



#%%

#%%

"""
Scatter plot that doesn't look great, plots mil vs gdp per capita

"""
def mil_as_percent_gdp_per_cap(df_mil, df_gdp, df_pop):

       
    
    df_percent_mil=df_mil.iloc[:,2:]/df_pop.iloc[:,2:]*100
    df_percent_gop=df_gdp.iloc[:,2:]/df_pop.iloc[:,2:]*100
    
    
    plt.figure(figsize=(11,4))
    for i in range(10):
        plt.scatter(df_percent_gop.iloc[i,:], df_percent_mil.iloc[i,:],)
    
    plt.title('Military Expenditure per Capita as a Fraction of GDP per Capita')
    plt.ylabel('Military Expenditure per Capita')
    plt.xlabel('GDP per Capita')
    plt.legend(df_mil.iloc[:,0], bbox_to_anchor=(1.0, .9))
    

mil_as_percent_gdp_per_cap(data_mil, data_gdp, data_pop)


#%%


def single_country_metrics_plot(df_mil, df_gdp, df_pop, country_str, mode='abs'):
    """
    Make a paired barplot with two axes to comapre GDP and MIl expenditure for one country at a time
    """

    
    df_mil['Type']="Military"
    df_gdp['Type']="GDP"

    df_combo=pd.concat([df_mil, df_gdp], ignore_index=True)
    
    try:
        df_combo=df_combo[df_combo['Country Name']==country_str].reset_index(drop=True)
        df_pop=df_pop[df_pop['Country Name']==country_str]
        df_pop=pd.concat([df_pop]*2, ignore_index=True) #Duplicate the population row for use on combo

    except:
        raise ValueError('Country not found, please check spelling.')
        
    if mode=='abs':
        str_add='' 

    else:
        str_add=' per Capita'
        df_combo.iloc[:,2:-1]=df_combo.iloc[:,2:-1]/df_pop.iloc[:,2:] 
        
    melt_combo=pd.melt(df_combo, id_vars=['Country Name', 'Country Code', 'Type'])   
    
    
    fig, ax= plt.subplots(figsize=(11,4))  
    sns.barplot(ax=ax, data=melt_combo, hue='Type', x='variable', y='value',)
    plt.legend(bbox_to_anchor=(1.0, .9))
    plt.ylabel(f'Change in Military Expenditure')
    plt.xlabel('')
  

    #plt.title(f'Comparison of GDP and Military Expenditure{str_add}: {country_str}', fontsize=16)

    plt.show()


single_country_metrics_plot(data_mil, data_gdp, data_pop, 'France')
single_country_metrics_plot(data_mil, data_gdp, data_pop, 'France', 'cap')


#%%

"""

Plots the gdp per capita and mil per capita, nothing more

"""
def dollars_per_capita(df_dollars, df_pop, dollar_type):
    


    str_dict={'GDP':['GDP per Capita', 'GDP per Capita in Billions (USD)'], 
              'MIL':['Military Expenditure per Capita', 'Expenditure per Capita in Billions (USD)']}
    dollar_type=dollar_type.upper()
    
    df_percapia=df_dollars.iloc[:,2:]/df_pop.iloc[:,2:]
    
    
    
    plt.figure(figsize=(11,4))
    for i in range(10):
        plt.plot(df_percapia.columns[:], df_percapia.iloc[i,:])
    
    plt.title(str_dict[dollar_type][0])
    plt.ylabel(str_dict[dollar_type][1])
    plt.legend(df_dollars.iloc[:,0], bbox_to_anchor=(1.0, .9))
    




dollars_per_capita(data_gdp, data_pop, 'GDP')
dollars_per_capita(data_mil, data_pop, 'MIL')