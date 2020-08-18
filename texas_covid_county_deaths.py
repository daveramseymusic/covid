import pandas as pd
import random as rd
from datetime import datetime, timedelta
import time
import urllib.request
from dateutil.parser import parse
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

# # download deaths file from Texas health dept.
# dls = "https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx"
# urllib.request.urlretrieve(dls, "texas_covid_data.xlsx")

# #import xl file from local folder and convert to csv
# data_xls = pd.read_excel('texas_covid_data.xlsx')
# data_xls.to_csv('texas_covid_data.csv', encoding='utf-8')
texas = pd.read_csv('texas_covid_data.csv')

# # NYT
# # download deaths files from NYT's github.
# dls = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
# urllib.request.urlretrieve(dls, "nyt_county_covid_data.csv")
nyt = pd.read_csv('nyt_county_covid_data.csv')

#run filters on all county and state columns to snake it all for easy search
nyt.state = nyt.state.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
nyt.county = nyt.county.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

#filter out all states and counties I want to use
# df.query('col1 <= 1 & 1 <= col1')
nyt_filtered = nyt.query('state == "texas" or state == "pennsylvania" or state == "colorado" or state == "california"')
nyt_filtered = nyt_filtered.query('county == "tarrant" or county == "philadelphia" or county == "san_diego" or county == "douglas"')

nyt_filtered = nyt_filtered.reset_index()


# nyt_filtered.rename(columns=lambda x: x.replace('county', 'nyt_county'), inplace=True)
nyt_pivot = nyt_filtered.pivot(columns='county',
         index='date',
         values='deaths').reset_index()


#make nyt_death data integer
for col in ['tarrant','philadelphia','san_diego','douglas']:
    nyt_pivot[col] = pd.to_numeric(nyt_pivot[col],errors='coerce').fillna(0)

#turn the parse the nyt dates so they match with the Texas dates
# parse dates into datetime and shortent to date()
nyt_pivot.date = nyt_pivot.date.apply(lambda x: parse(x).date())
print(nyt_pivot.head())

##Pivot and Clean Texas DHS dataframe
#shorten the publishing date info in texas 
texas.rename(columns=lambda x: x.replace('COVID-19 Total Fatalities by County, 3/7/2020 - ', ''), inplace=True)

#make the columns the right ones:
new_header = texas.iloc[1] #grab the first row for the header
texas = texas[2:] #take the data less the header row
texas.columns = new_header #set the header row as the df header

#set index
texas = texas.iloc[:, 1:] #take the data less the first two columns or so

texas = texas.set_index('County Name')
# then transpose
texas = texas.T
# reset index
texas = texas.reset_index()

# After pivot & datetime clenup, change the cell above the date from 'county name' to 'date:

# parse into datetime and shortent to date()
texas.iloc[:,0] = texas.iloc[:,0].apply(lambda x: parse(x).date())

#make all the column names aka headers strings (cause the first one wasnt for like NO REASON)
texas.columns = [str(i) for i in texas.columns.values.tolist()]
texas.rename(columns=lambda x: x.replace('1', 'date'), inplace=True)  

#clean county names and everything else that will be column headers
texas.rename(columns=lambda x: x.strip()\
                                .lower().replace(' ', '_').replace('(', '').replace(')', '')\
                                , inplace=True)

# filter out everything but tarrant county
tarrant_df = texas[[ 'date', 'tarrant']]

# #make tarrant death data integers:
tarrant_df.tarrant = pd.to_numeric(tarrant_df.tarrant, downcast='integer')

##
# 
#  Merge Texas and NYT on tarrant date column
death_merge = pd.merge(
    tarrant_df,
    nyt_pivot,
    how='left',
    left_on='date',
    right_on='date',
    suffixes=['_tx_deaths', '_nyt_deaths']
)

#turn Nan or in the float format into 0's 
#  df['DataFrame Column'] = df['DataFrame Column'].fillna(0)
# death_merge.tarrant_nyt_deaths = death_merge.tarrant_nyt_deaths.fillna(0)


# death_merge.tarrant_nyt_deaths = death_merge.tarrant_nyt_deaths.apply(lambda x: int(x))


for col in ['tarrant_nyt_deaths','philadelphia','san_diego','douglas']:
    # nyt_pivot[col] = pd.to_numeric(nyt_pivot[col],errors='coerce').fillna(0)
    death_merge[col] = death_merge[col].apply(lambda x: int(x))

print(death_merge.head())


#print bar graph of Tarrant County Deaths
#DO a plot figure then the ax later just as in the codecademy:

# # create your figure here
# plt.figure(figsize=(12, 8))

# ax1 = plt.subplot(1, 2, 1)
# x_values = range(len(months))
# plt.plot(x_values, visits_per_month, marker='s')
# plt.xlabel('months')
# plt.ylabel('visits')
# ax1.set_xticks(x_values) 
# ax1.set_xticklabels(months)
# plt.title('visits per month')

# ax2 = plt.subplot(1, 2, 2)
# plt.plot(x_values, key_limes_per_month, color='green', marker='s')
# plt.plot(x_values, persian_limes_per_month, marker='o', color='blue')
# plt.plot(x_values, blood_limes_per_month, marker='*', color='orange')
# ax2.set_xticks(x_values) 
# ax2.set_xticklabels(months)
# plt.legend(['Key Lime', 'Persian', 'Blood'], loc=1)
# plt.title('Limes per month')
# plt.subplots_adjust()
# plt.show()

# plt.savefig('lucky_stuff.png')

plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 2, 1)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax1.bar(tarrant_df.date, death_merge.tarrant_nyt_deaths, width=0.8, align='center')
plt.ylabel('Deaths')
plt.title('Tarrant County Total Covid Deaths over Time')

ax2 = plt.subplot(2, 2, 2)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax2.bar(tarrant_df.date, death_merge.philadelphia , width=0.8, align='center')
plt.ylabel('Deaths')
plt.title('Philadelphia')

ax3 = plt.subplot(2, 2, 3)
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax3.bar(tarrant_df.date, death_merge.san_diego , width=0.8, align='center')
plt.xlabel('Dates')
plt.ylabel('Deaths')
plt.title('San Diego')

ax4 = plt.subplot(2, 2, 4)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax4.bar(tarrant_df.date, death_merge.douglas , width=0.8, align='center')
plt.xlabel('Dates')
plt.ylabel('Deaths')
plt.title('Douglas County')

plt.show()

# fig, ax = plt.subplots(figsize=(10, 6))
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
# ax.bar(tarrant_df.date, death_merge.tarrant_nyt_deaths, width=0.8, align='center')
# plt.xlabel('Dates')
# plt.ylabel('Deaths')
# plt.title('Tarrant County Total Covid Deaths over Time')

# plt.show()

#print graph of Philadelphia Cty Death
#print San Diego Deaths
#print Douglas Cty Deaths


# ## double bar graph code

# # # tx data (blue bars)
# n = 1  # This is our first dataset (out of 2)
# t = 2 # Number of datasets
# d = len(death_merge.tarrant_tx_deaths)# Number of sets of bars
# w = 0.6 # Width of each bar
# tx_deaths_x = [t*element + w*n for element
#              in range(d)]
# plt.bar(tx_deaths_x, death_merge.tarrant_tx_deaths)

# # # nyt data (orange bars)
# n = 2  # This is our second dataset (out of 2)
# t = 2 # Number of datasets
# d = len(death_merge.tarrant_tx_deaths)# Number of sets of bars
# w = 0.6 # Width of each bar
# nyc_deaths_x = [t*element + w*n for element
#              in range(d)]
# plt.bar(nyc_deaths_x, death_merge.tarrant_nyt_deaths)
# plt.xlabel('Days From 3-07 to 8-17')
# plt.ylabel('Deaths')
# plt.legend(['Texas DSHS data', 'NYT data'], loc=2)
# plt.show()



###A way of doing both bars together but squishes all dates in mess
# ax = death_merge.plot.bar(color=["SkyBlue","IndianRed"], rot=0, title="Death Merge")
# ax.set_xlabel("date")
# ax.set_ylabel("deaths")
# ax.xaxis.set_major_formatter(plt.FixedFormatter(death_merge.date))
# plt.gcf().autofmt_xdate()
# plt.show()




##other version from the same Stack Overflow answer that I don't quite understand.
# ax = plt.subplot(111)
# w = 0.3
# ax.bar(x-w, y, width=w, color='b', align='center')
# ax.bar(x, z, width=w, color='g', align='center')
# ax.bar(x+w, k, width=w, color='r', align='center')
# ax.xaxis_date()
# ax.autoscale(tight=True)
# plt.show()




# #variable for today's deaths
# today_deaths = tarrant_df.iloc[-1,2]

# #to get deaths each day you must subtract today from 8 days ago.  making 8 days the zero
# week_ago_deaths = tarrant_df.iloc[-8,2] 

# two_week_ago_deaths = tarrant_df.iloc[-15,2]

# deaths_last_seven_days = today_deaths - week_ago_deaths
# deaths_week_before = week_ago_deaths - two_week_ago_deaths

# # #make most recent column name and 1 week ago column name as variables to print out

# most_recent_date = tarrant_df.date.iloc[-1]
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
# # date_most_recent_update = recent_repeated_data.date.iloc[0]
# # days_since_update = date_most_recent_update - most_recent_date - timedelta(days=1)

# # #print date of last reported death:
# # print('last day there was a change in deaths reported: ' + str(date_most_recent_update))
# # print('number of days since last update:   ' + str(days_since_update))


# # print(tarrant_df.iloc[-15:,1:])

# # #find the last day deaths actually changed. then save the last day to a variable.
# # most_recent_updated_death_total_df = tarrant_df.loc[(tarrant_df.date == date_most_recent_update), ['tarrant']]
# # most_recent_updated_death_total = most_recent_updated_death_total_df.iloc[0,0]
# # print(most_recent_updated_death_total)

# # week_before_mrud_total_df = tarrant_df.loc[(tarrant_df.date == date_most_recent_update - timedelta(days=8)), ['tarrant']]
# # week_before_mrud_total = week_before_mrud_total_df.iloc[0,0]
# # print(week_before_mrud_total)


# # updated_last_seven_ave = (most_recent_updated_death_total - week_before_mrud_total) / 7
# # print(updated_last_seven_ave)


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