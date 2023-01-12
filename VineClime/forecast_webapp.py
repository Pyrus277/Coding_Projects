import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from prophet import Prophet 
import shelve
import streamlit as st
# To make this file work, open up gitbash, nav to this dir, and run 
# $ streamlit run forecast_webapp.py
   
def visualize_wine_trend(county, climate_feat, dep_var):
    '''
    Input:
        county: One of the wine producing counties in the cwp dataset
        climate_feature: One of the climate featue column headers in the acc dataset
        dep_var: either "production" for tons of winegrapes produced in a given year
            or "price" for price value per ton of wine grapes for a given year
    
    Output: 
        a Prophet chart showing the relevant known datapoints in black, known test-set
        datapoints in red, and a prediction line running through to 2025, surrounded by
        a 80% error margin. 
    '''
   
    with shelve.open('capstone_dataframes') as shelfFile:
        cwp_acc = shelfFile['cwp_acc']
    
    # String formatting for the chart title
    if dep_var == 'production':
        title_str = 'production in tons'
    elif dep_var == 'price':
        title_str = 'value per ton (usd)'
    
    ## Isolate the production and climate data for the selected county
    county_df = cwp_acc.loc[cwp_acc['county'] == county]

    # Format for Prophet
    county_df = county_df[["year", dep_var, climate_feat]]
    county_df["year"] = pd.to_datetime(county_df['year'], format='%Y')
    county_df.rename(columns={"year":"ds", dep_var:"y"}, inplace=True)

    # Test train split
    train = county_df.loc[county_df.ds < '2014']
    test = county_df.loc[county_df.ds >= '2014']

    # Train Prophet model
    model = Prophet() 
    model.add_regressor(climate_feat, standardize=True) 
    model.fit(train)

    # Construct the train_test_period_df
    # Set up a dataframe for the testing time segment so it includes 2014 onwards
    train_test_period = model.make_future_dataframe(periods=7, freq='Y')
    # update future df with column for the regressor amount-- annual_temperature
    train_test_period = train_test_period.merge(county_df[['ds', climate_feat]], on = ['ds'], how = 'right')

    ## Extend the dataframe to predict out to 2025
    # Set up a new dataframe to in a linear model prediction on the chosen 
    # climate feature
    county_df = cwp_acc.loc[cwp_acc['county'] == county]
    X_withconstant = sm.add_constant(county_df['year'])
    y = county_df[climate_feat]

    # Setup linreg
    myregression = sm.OLS(y, X_withconstant)
    # Fit the model
    myregression_results = myregression.fit()
    # predict the next five years onwards from 2020
    years = np.array([2021, 2022, 2023, 2024, 2025])
    future_years = sm.add_constant(years)
    future_years = myregression_results.predict(future_years)

    #package this into a dataframe to append on to the Prophet forcast df
    future_df = pd.DataFrame({'ds': years, 
                  climate_feat: future_years})
    future_df['ds'] = pd.to_datetime(future_df['ds'], format='%Y')

    # sort the dataframe just in case to the concat stacks in order
    train_test_period = train_test_period.sort_values('ds')

    # Concat the new forcast df segment onto the train_test_period df
    forecast_df = pd.concat([train_test_period, future_df])


    # Fire up the trained Prophet model
    forecast = model.predict(forecast_df)

    # Plot the output
    fig2 = model.plot(forecast, xlabel='YEAR', ylabel = dep_var.upper())
    fig1 = plt.scatter(test['ds'], test['y'], c = 'red', label="Observed Test Points")
    plt.legend(loc='upper left')
    plt.title(f'Winegrape {title_str} as a function of time and {climate_feat.replace("_"," ")} for {county} County, Ca \n', fontdict={'fontsize': 15})
    
    return plt

# set up dropdown items
county = st.sidebar.selectbox(
    'Select a California County',
    (['Alameda', 'Amador', 'Calaveras', 'Colusa', 'ContraCosta',
       'ElDorado', 'Fresno', 'Kern', 'Kings', 'Lake', 'Madera', 'Marin',
       'Mendocino', 'Merced', 'Monterey', 'Napa', 'Nevada', 'Placer',
       'Riverside', 'Sacramento', 'SanBenito', 'SanBernardino',
       'SanDiego', 'SanJoaquin', 'SanLuisObispo', 'SanMateo',
       'SantaBarbara', 'SantaClara', 'SantaCruz', 'Shasta', 'Solano',
       'Sonoma', 'Stanislaus', 'Tehama', 'Tulare', 'Yolo', 'Mariposa',
       'Trinity', 'Mono', 'Yuba', 'Glenn']))
climate_feat = st.sidebar.selectbox(
    'Select a Climate Feature',
    (['annual_profile_moisture', 'annual_root_moisture',
       'annual_surface_moisture', 'annual_precipitation', 'annual_humidity',
       'annual_temperature', 'annual_wind_speed', 'summer_profile_moisture',
       'summer_root_moisture', 'summer_surface_moisture',
       'summer_precipitation', 'summer_humidity', 'summer_temperature',
       'summer_wind_speed', 'winter_profile_moisture', 'winter_root_moisture',
       'winter_surface_moisture', 'winter_precipitation', 'winter_humidity',
       'winter_temperature', 'winter_wind_speed']))

dep_var = st.sidebar.selectbox(
    'Select a Production Metric',
    ('price', 'production'))
   
if len(county) != 0 and len(climate_feat) != 0 and len(dep_var) != 0:

    st.pyplot(visualize_wine_trend(county, climate_feat, dep_var))



# county = st.sidebar.text_input("County:")
# climate_feat = st.sidebar.text_input("Climate Feature:")
# dep_var = st.sidebar.text_input("Production Variable:")
              