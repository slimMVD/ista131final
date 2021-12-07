import pandas as pd, numpy as np, matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import datetime as dt



# this funtion takes a csv file and cleans it into a dataframe
def get_df():
    fname = "C:\\Users\\bbiel\\Documents\\Mu Code ISTA\\Final\\data_table_for_daily_death_trends__california zejun graph.csv"
    df = pd.read_csv(fname,sep=',', skiprows = 2, engine='python')
    del df["State"]
    df["Dates"] = np.nan
    def date_convert(date_to_convert):
        return datetime.datetime.strptime(date_to_convert, '%b %d %Y').strftime('%m/%d/%Y')
    df['Dates'] = df['Date'].apply(date_convert)
    del df["Date"]
    return df

# This gets and returns a list of the dates
def get_date_lst():
    df = get_df()
    lst_dates = []
    for i in df['Dates']:
        lst_dates.append(i)
    return lst_dates


# this creates the first graph
def fig1():
    df = get_df()
    lst_dates = get_date_lst()
    x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in lst_dates]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))
    plt.plot(x,df['Current Hospitalized COVID-19 Patients'])
    plt.gcf().autofmt_xdate()
    plt.xlabel("Dates")
    plt.ylabel("Current Hospitalized COVID-19 Patients in California")


#this creates the second graph
def fig2():
    df = get_df()
    lst_dates = get_date_lst()
    plt.figure(figsize=(10,10))
    plt.style.use('ggplot')
    lst_dates = []
    for i in df['Dates']:
        lst_dates.append(i)
    x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in lst_dates]
    lst = []
    for i in df['New Deaths']:
        lst.append(i)
    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x,lst,width=0.8, color='black')


    fig=df.plot.bar(capsize=8, legend=None,
    rot=0,fontsize=10,color=['blue','green'],edgecolor='black',
    linewidth=3, figsize=(12,8))

    plt.xlabel("Dates")
    plt.ylabel("New COVID-19 Hospitalizations in California")
    fig.invert_xaxis()
    #plt.ylabel("New COVID-19 Deaths in California")


#this creates the third graph
def fig3():
    df = get_df()
    plt.figure(figsize=(16,10), dpi= 80)
    lst_dates = get_date_lst()
    lst = []
    for i in df["7-Day Moving Avg"]:
        lst.append(i)
    x = np.array(lst_dates)
    y = np.array(lst)
    plt.rcParams['axes.facecolor']='LavenderBlush'
    plt.rcParams['figure.facecolor']='black'
    plt.scatter(x, y)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))
    plt.xlabel("Dates")
    plt.ylabel("7-Day Moving Avg in California")

# this is the first main, I have two because I had issues managing the plt object.
# The other graphs will be displayed when the first graphs are closed.
def main():
    fig1()
    fig2()
    fig3()
    plt.show()


main()

# this converts 2 different CSVs with one of the csv file paths being provided as a paramenter. The CSVs are converted
# to dataframes.
def csv(file):
    df = pd.read_csv(file, sep = ",", skiprows = 2)
    df2 = pd.read_csv("C:\\Users\\bbiel\\Documents\\Mu Code ISTA\\Final\\data_table_for_daily_death_trends__california.csv", sep = "," , skiprows = 2)
    df["New Deaths"] = df2["New Deaths"]
    df["Doses Per Day"] = 0
    df["Dates"] = df["Date"].replace({"Jan":"01", "Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}, regex = True)
    df["Total Doses Administered"] = df["Total Doses Administered"].fillna(0)
    for i in range(1, len(df["Total Doses Administered"])-1):
        a = pd.to_numeric(df["Total Doses Administered"])
        df.loc[i-1,"Doses Per Day"] = abs((int(a.iloc[i-1]) - int(a.iloc[i])))
        a.append(df["Doses Per Day"])
    #for j in
    df.drop(labels = [0], axis = 0)
    df.drop([0, 1, 2], axis = 0,inplace = True)
   #for j in range
    #df.drop(df.iloc[634], axis = 0,inplace = True)
    del df["7-Day Moving Avg"]
    del df["State"]
    return df


# this function cleans a csv to make it more workable for the project.
def clean_dose():
    df = csv("C:\\Users\\bbiel\\Documents\\Mu Code ISTA\\Final\\data_table_for_daily_cases_trends__california.csv")
    lst_dates = []
    for i in range(349,674):
        #print(i)
        df = df.drop(index=i)
    return df


# This creates the fourth graph
def figure1():
    df = csv("C:\\Users\\bbiel\\Documents\\Mu Code ISTA\\Final\\data_table_for_daily_cases_trends__california.csv")
    x = [dt.datetime.strptime(d,'%m %d %Y').date() for d in df["Dates"]]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m %d %Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))
    plt.plot(x,df['New Cases'])
    plt.gcf().autofmt_xdate()
    plt.xlabel("Dates")
    plt.ylabel("New Cases")



# this creates the fifth graph
def figure2():
    df = csv("C:\\Users\\bbiel\\Documents\\Mu Code ISTA\\Final\\data_table_for_daily_cases_trends__california.csv")
    plt.figure(figsize=(10,10))
    plt.style.use('ggplot')
    lst_dates = []
    for i in df['Dates']:
        lst_dates.append(i)
    x = [dt.datetime.strptime(d,'%m %d %Y').date() for d in df["Dates"]]
    lst = []
    for i in df['New Deaths']:
        lst.append(i)
    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x,lst,width=0.8, color='black')
    plt.xlabel("Dates")
    plt.ylabel("New Deaths")


# this creates the sixth graph
def figure3():
    df = clean_dose()
    plt.figure(figsize=(16,10), dpi= 80)
    lst = []
   #df_1 = df.iloc[3:634,:]
    for i in df["Doses Per Day"]:
        lst.append(i)
    x = np.array(df["Dates"])
    y = np.array(lst)
    plt.scatter(x, y)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))
    plt.bar(x,lst,width=0.8, color='navy')
    plt.xlabel("Dates")
    plt.ylabel("Doses Per Day")
    x2=[]
    y2=[]
    for i in range(349):
        x2.append(int(i))
    for b in x2:
        y2.append(-716*b+251000)
    plt.plot(x2, y2)
    plt.gca().invert_xaxis()




# this is the first main, I have two because I had issues managing the plt object.
# The other graphs will be displayed when the first graphs are closed.
def main2():
    clean_dose()
    figure1()
    figure2()
    figure3()
    plt.show()


main2()