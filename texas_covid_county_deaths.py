import pandas as pd
import random as rd
from datetime import datetime, timedelta
import time
import urllib.request
from dateutil.parser import parse
from matplotlib import pyplot as plt
import matplotlib.dates as mdates


#download deaths file from Texas health dept.
dls = "https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx"
urllib.request.urlretrieve(dls, "test.xlsx")

#import xl file from local folder
data_xls = pd.read_excel('test.xlsx')
data_xls.to_csv('new_covid_test.csv', encoding='utf-8')
c_cov = pd.read_csv('new_covid_test.csv')

#shorten the publishing date info in c_cov
c_cov.rename(columns=lambda x: x.replace('COVID-19 Total Fatalities by County, 3/7/2020 - ', ''), inplace=True)

# change the 1 to a str
c_cov.iloc[1,0] = str(c_cov.iloc[1,0])

#make the columns the right ones:
new_header = c_cov.iloc[1] #grab the first row for the header
c_cov = c_cov[2:] #take the data less the header row
c_cov.columns = new_header #set the header row as the df header

#set index
c_cov = c_cov.iloc[:, 1:] #take the data less the first two columns or so

c_cov = c_cov.set_index('County Name')
# then transpose
c_cov = c_cov.T
# reset index
c_cov = c_cov.reset_index()



# After pivot & datetime clenup, change the cell above the dates from 'county name' to 'dates:

# # parse into datetime and shortent to date()
c_cov.iloc[:,0] = c_cov.iloc[:,0].apply(lambda x: parse(x).date())

#make all the column names aka headers strings (cause the first one wasnt for like NO REASON)
c_cov.columns = [str(i) for i in c_cov.columns.values.tolist()]
c_cov.rename(columns=lambda x: x.replace('1', 'dates'), inplace=True)  

#clean county names and everything else that will be column headers
c_cov.rename(columns=lambda x: x.strip()\
                                .lower().replace(' ', '_').replace('(', '').replace(')', '')\
                                , inplace=True)

# # # filter out everything but tarrant county
tarrant_df = c_cov[[ 'dates', 'tarrant']].reset_index()


# #make data integers:
# tarrant_df.iloc[1:,2] = pd.to_numeric(tarrant_df.iloc[1:,2], downcast='integer')
tarrant_df.tarrant = pd.to_numeric(tarrant_df.tarrant, downcast='integer')

# #variable for today's deaths
# today_deaths = tarrant_df.iloc[-1,2]

# #to get deaths each day you must subtract today from 8 days ago.  making 8 days the zero
# week_ago_deaths = tarrant_df.iloc[-8,2] 

# two_week_ago_deaths = tarrant_df.iloc[-15,2]

# deaths_last_seven_days = today_deaths - week_ago_deaths
# deaths_week_before = week_ago_deaths - two_week_ago_deaths

# # #make most recent column name and 1 week ago column name as variables to print out

# most_recent_date = tarrant_df.dates.iloc[-1]
# two_week_ago_date = tarrant_df.iloc[-8,1]
# county = (tarrant_df.iloc[0,2])

# # #create average deaths per day for each week:
# ave_deaths_last_seven_days = deaths_last_seven_days / 7
# ave_deaths_week_before = deaths_week_before / 7

# #### stuff befor graffing
# # # print total deaths
# # print('\n' + county +' county' + '\n''\n' + '  Total Deaths:' + '\n')
# # print('Last 7 days' +'\n' '(ending ' + str(most_recent_date) + '): ' + str(deaths_last_seven_days))
# # print('week before' +'\n'+ '(ending ' + str(two_week_ago_date) + '): ' + str(deaths_week_before))

# # #print ave deaths per day
# # print('\n' + '  Ave Deaths/day:' + '\n')
# # print('Last 7 days' +'\n' '(ending ' + str(most_recent_date) + '): ' + str(ave_deaths_last_seven_days))
# # print('week before' +'\n'+ '(ending ' + str(two_week_ago_date) + '): ' + str(ave_deaths_week_before))

# # # create a function that finds the last day a death was reported:
# # recent_repeated_data = tarrant_df[tarrant_df.tarrant == today_deaths]
# # # one_day = datetime.timedelta(days=1)
# # date_most_recent_update = recent_repeated_data.dates.iloc[0]
# # days_since_update = date_most_recent_update - most_recent_date - timedelta(days=1)

# # #print date of last reported death:
# # print('last day there was a change in deaths reported: ' + str(date_most_recent_update))
# # print('number of days since last update:   ' + str(days_since_update))


# # print(tarrant_df.iloc[-15:,1:])

# # #find the last day deaths actually changed. then save the last day to a variable.
# # most_recent_updated_death_total_df = tarrant_df.loc[(tarrant_df.dates == date_most_recent_update), ['tarrant']]
# # most_recent_updated_death_total = most_recent_updated_death_total_df.iloc[0,0]
# # print(most_recent_updated_death_total)

# # week_before_mrud_total_df = tarrant_df.loc[(tarrant_df.dates == date_most_recent_update - timedelta(days=8)), ['tarrant']]
# # week_before_mrud_total = week_before_mrud_total_df.iloc[0,0]
# # print(week_before_mrud_total)


# # updated_last_seven_ave = (most_recent_updated_death_total - week_before_mrud_total) / 7
# # print(updated_last_seven_ave)

# #print bar graph of Tarrant County Deaths
fig, ax = plt.subplots(figsize=(10, 6))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax.bar(tarrant_df.dates, tarrant_df.tarrant, width=0.8, align='center')
plt.xlabel('Dates')
plt.ylabel('Deaths')
plt.title('Tarrant County Total Covid Deaths over Time')
plt.show()

# ###

##figure out daily deaths to watch rate:
#set y_values to equal last 7 days
    #create list of the last 7 days from the df you've created.
        #try using today's deaths variable
        # daily_deaths_lsd = [i for i in tarrant_df.iloc[-1,2]
# y_values = [range(700)]

# plt.plot(x_values, y_values)




##things I thought to do before I started graphing:
##now make it so it's got he average for the recent update and the week before that...


# #create function to find highest ave during peak

# ##create function here:

# #filter dates:

## so figure out the earliest unchanged day.  and track how much they change over time.  