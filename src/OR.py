'''
Author: <Ngan Pham>
Date: <10/14/2021>
Class: ISTA 131
Section Leader: <Grace>
'''
'''
ISTA 131 Final Project
GROUP MEMBERS:
    Bryan Bielawa
    Zejun Li
    Alexander Esparza
    Luis Flores Lozano
    Ngan Pham

Each of the team members will choose a different state and will gather and extract specific columns that they choose to visualize Covid trends related data regard their respective states.
Dataset link: 
https://covid.cdc.gov/covid-data-tracker/#trends_dailydeaths
Columns: State (Oregon), Date, New Deaths, Total Death Rate per 100k, 7-Day % Positivity
'''

import pandas as pd, numpy as np, matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import datetime as dt

'''
This function reads the csv file of daily death trends in Oregon, converts the dates to m/d/y format and return its dataframe
'''
def get_df():
    fname = "data_table_for_daily_death_trends__oregon.csv"
    df = pd.read_csv(fname, sep=',', skiprows = 2, engine='python')
    del df["State"]
    df["Dates"] = np.nan
    def date_convert(date_to_convert):
        return datetime.datetime.strptime(date_to_convert, '%b %d %Y').strftime('%m/%d/%Y')
    df['Dates'] = df['Date'].apply(date_convert)
    del df["Date"]
    return df

'''
This function gets the dates from the dataframe and return a date list
'''
def get_date_lst():
    df = get_df()
    lst_dates = []
    for i in df['Dates']:
        lst_dates.append(i)
    return lst_dates
'''
This function groups the months from the dataframe and create a month list
'''
def get_month_lst():
    dates = get_date_lst()
    s = pd.to_datetime(pd.Series(dates), format='%m/%d/%Y')
    s.index = s.dt.to_period('m')
    s = s.groupby(level=0).size()
    s = s.reindex(pd.period_range(s.index.min(), s.index.max(), freq='m'), fill_value=0)
    return list(s.index.strftime('%Y-%m'))
'''
This function plots a line chart representing the percent of NAAT tests reported in the last 7 days that were positive for COVID-19
'''
def fig1():
    df = get_df()   
    lst_dates = get_date_lst()
    x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in lst_dates]
    plt.figure(figsize=(16,10))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=90))
    ax = plt.gca()
    ax.set_facecolor('aliceblue')
    plt.grid()
    plt.plot(x,df['7-Day % Positivity'], color = 'g')
    plt.xlabel("Months", fontsize = 14)
    plt.ylabel("7-Day % Positivity", fontsize = 14)
    plt.title("NAATs 7-Day Percent Positivity in Oregon Reported to CDC", fontsize = 18)
'''
This function plots a bar graph representing monthly trends in total number of COVID-19 deaths
'''
def fig2():
    df = get_df()
    df['Dates'] = pd.to_datetime(df.Dates, format='%m/%d/%Y')
    lst_dates = get_month_lst()
    plt.figure(figsize=(16,10))
    plt.gcf().subplots_adjust(bottom = 0.2)
    ax = plt.gca()
    ax.set_facecolor('honeydew')
    plt.grid()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    df.groupby([df['Dates'].dt.year, df['Dates'].dt.month])['New Deaths'].sum().plot(kind = 'bar', color = 'teal')
    plt.xlabel("Months", fontsize = 14)
    ticks = pd.date_range(pd.Timestamp("2020-01"), periods = 23, freq = 'm').strftime('%m-%Y')
    plt.xticks(range(0,len(ticks)), ticks)
    plt.ylabel("New Deaths", fontsize = 14)
    plt.title("Monthly Trends in Number of COVID-19 Deaths in Oregon Reported to CDC", fontsize = 18)
'''
This funcion extracts the data of new COVID cases from the dataframe
'''
def get_df_fig_3_newcase():
    fname = "data_table_for_daily_case_trends__oregon.csv"
    df = pd.read_csv(fname, sep=',', skiprows = 2, engine='python')
    del df["State"]
    df["Dates"] = np.nan
    def date_convert(date_to_convert):
        return datetime.datetime.strptime(date_to_convert, '%b %d %Y').strftime('%m/%d/%Y')
    df['Dates'] = df['Date'].apply(date_convert)
    del df["Date"]
    return df
'''
This funcion extracts the data of new COVID deaths from the dataframe
'''
def get_df_fig_3_newdeath():
    fname = "data_table_for_daily_death_trends__oregon.csv"
    df = pd.read_csv(fname, sep=',', skiprows = 2, engine='python')
    del df["State"]
    df["Dates"] = np.nan
    def date_convert(date_to_convert):
        return datetime.datetime.strptime(date_to_convert, '%b %d %Y').strftime('%m/%d/%Y')
    df['Dates'] = df['Date'].apply(date_convert)
    del df["Date"]
    return df
'''
This function creates a scatter plot displaying the daily COVID cases and daily COVID deaths from two dataset
'''
def fig3():
    df_newcase = get_df_fig_3_newcase()
    df_newdeath = get_df_fig_3_newdeath()
    plt.figure(figsize=(16,10), dpi= 80)
    lst_new_cases = []
    for i in df_newcase['New Cases']:
        lst_new_cases.append(i)
    lst_new_death = []
    for i in df_newdeath['New Deaths']:
        lst_new_death.append(i)
    x = np.array(lst_new_cases)
    y = np.array(lst_new_death)
    plt.grid()
    ax = plt.gca()
    ax.set_facecolor('seashell')
    x_pos = [i for i, _ in enumerate(x)]
    plt.scatter(x, y, color='maroon')
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b, color = 'navy')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=230))
    plt.xlabel("New Cases", fontsize = 18)
    plt.ylabel("New Deaths", fontsize = 18)
    plt.title("Daily Deaths vs Daily Cases in Oregon Reported to CDC", fontsize = 23)
    plt.gca()

#Call previous funtions to plot figures
def main():
    fig1()
    fig2()
    fig3()
    plt.show()

if __name__ == "__main__":
    main()
