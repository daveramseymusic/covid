import pandas as pd
import random as rd
from datetime import datetime, timedelta
import time
import urllib.request
from dateutil.parser import parse


#download deaths file from Texas health dept.
dls = "https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx"
urllib.request.urlretrieve(dls, "test.xlsx")

#import xl file from local folder
data_xls = pd.read_excel('test.xlsx')
data_xls.to_csv('new_covid_test.csv', encoding='utf-8')
c_cov = pd.read_csv('new_covid_test.csv')

# #pivot table so the column is county name 
c_cov = c_cov.set_index('Unnamed: 0').T
# c_cov.reset_index()

#change "county name" to a date so the whole column can be in datetime
c_cov.iloc[0,1] = '01/12/1981'    

# After pivot & datetime clenup, change the cell above the dates from 'county name' to 'dates:
c_cov.iloc[0,1] = 'dates'

#clean county names and everything else in the headers
c_cov.iloc[0,:] = c_cov.iloc[0,:].str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

#create the column names as I prefer them starting on the second row & reset index:
c_cov.columns = c_cov.iloc[0]
c_cov.reset_index()


# parse into datetime and shortent to date()
c_cov.iloc[1:,1] = c_cov.iloc[1:,1].apply(lambda x: parse(x).date())

# # filter out everything but tarrant county
tarrant_df = c_cov[[ 'dates', 'tarrant']].reset_index()

#make data integers:
tarrant_df.iloc[1:,2] = pd.to_numeric(tarrant_df.iloc[1:,2], downcast='integer')


#variable for today's deaths
today_deaths = tarrant_df.iloc[-1,2]

#to get deaths each day you must subtract today from 8 days ago.  making 8 days the zero
week_ago_deaths = tarrant_df.iloc[-8,2]

two_week_ago_deaths = tarrant_df.iloc[-15,2]

deaths_last_seven_days = today_deaths - week_ago_deaths
deaths_week_before = week_ago_deaths - two_week_ago_deaths

# #make most recent column name and 1 week ago column name as variables to print out

most_recent_date = tarrant_df.dates.iloc[-1]
two_week_ago_date = tarrant_df.iloc[-8,1]
county = (tarrant_df.iloc[0,2])

# #create average deaths per day for each week:
ave_deaths_last_seven_days = deaths_last_seven_days / 7
ave_deaths_week_before = deaths_week_before / 7


# print total deaths
print('\n' + county +' county' + '\n''\n' + '  Total Deaths:' + '\n')
print('Last 7 days' +'\n' '(ending ' + str(most_recent_date) + '): ' + str(deaths_last_seven_days))
print('week before' +'\n'+ '(ending ' + str(two_week_ago_date) + '): ' + str(deaths_week_before))

#print ave deaths per day
print('\n' + '  Ave Deaths/day:' + '\n')
print('Last 7 days' +'\n' '(ending ' + str(most_recent_date) + '): ' + str(ave_deaths_last_seven_days))
print('week before' +'\n'+ '(ending ' + str(two_week_ago_date) + '): ' + str(ave_deaths_week_before))

# create a function that finds the last day a death was reported:
recent_repeated_data = tarrant_df[tarrant_df.tarrant == today_deaths]
# one_day = datetime.timedelta(days=1)
date_most_recent_update = recent_repeated_data.dates.iloc[0]
days_since_update = date_most_recent_update - most_recent_date - timedelta(days=1)

#print date of last reported death:
print('last day there was a change in deaths reported: ' + str(date_most_recent_update))
print('number of days since last update:   ' + str(days_since_update))



# df2 = df.loc[(df.column1 == 'row_i_like'), ['column_i_like']]

#print
print(tarrant_df.iloc[-15:,1:])


most_recent_updated_death_total_df = tarrant_df.loc[(tarrant_df.dates == date_most_recent_update), ['tarrant']]
most_recent_updated_death_total = most_recent_updated_death_total_df.iloc[0,0]
print(most_recent_updated_death_total)

week_before_mrud_total_df = tarrant_df.loc[(tarrant_df.dates == date_most_recent_update - timedelta(days=8)), ['tarrant']]
week_before_mrud_total = week_before_mrud_total_df.iloc[0,0]
print(week_before_mrud_total)


updated_last_seven_ave = (most_recent_updated_death_total - week_before_mrud_total) / 7
print(updated_last_seven_ave)

##now make it so it's got he average for the recent update and the week before that...


# #create function to find highest ave during peak

# ##create function here:

# #filter dates:
