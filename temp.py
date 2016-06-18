import pandas as pd
import matplotlib.pyplot as plt

file = pd.read_json('logins.json')  #read the json file 
print file.loc[1:10]                #print the first 10 rows to see the form of data
df = pd.DataFrame(file)             #change data to DataFrame form 
df['Date'] = pd.to_datetime(df['login_time']) #change the data type to datetime
print df.head                    #print the first line to see the form 


type(df.loc[1,'Date'])  
df['Count'] = 1                 #add a count column 
df = df.set_index('Date').drop('login_time', axis=1) # drop Login_time column and set 'Date' column as index
print df.head()                #print a few lines to see its changes


interval = df.resample('15min', how=sum)    #resample the data by 15 minutes interval and count the number of logins in every 15 minutes 
interval.reset_index(drop=False, inplace=True)
print interval.head()

interval.plot()                   #the plot shows the number of logins in each interval 
plt.show()

Day = df.resample('D', how=sum)     #resample the data by one day interval and count the number of logins in every 15 minutes
                                        #start from 1970-01-01 20:00:00 
Day.reset_index(drop=False, inplace=True)
Day.head()

Day.plot()                          #the plot shows the number of logins in each interval 
plt.show()                              #the plot shows there is an extreme high point, so I want to find the highest point  

print Day.loc[Day['Count'] == Day['Count'].max(), 'Date']
#93   1970-04-04
#On 1970-04-04, there are 93 logins of users 

print len(Day['Count'])            #103, so there are 103 days of data 
Jan = []                               #seperate these data by month 
Feb = []
Mar = []
Apr = []

for i in range(31):                    #put the corresponding data to each month 
    Jan.append(Day['Count'][i])
for i in range(32,60):
    Feb.append(Day['Count'][i])
for i in range(60,91):
    Mar.append(Day['Count'][i])
for i in range(91,len(Day['Count'])):
    Apr.append(Day['Count'][i])
    
print len(Jan)                          #31 there are 31 days of data which starts from 1970-01-01
print len(Feb)                          #28 there are 28 days of data 
print len(Mar)                          #30 there are 30 days of data 
print len(Apr)                          #13 there are 13 days of data which ends at 1970-04-13

pd.DataFrame(Jan, columns = ['Count']).plot(kind = 'bar')    #show bar chart of every month 
plt.show()
pd.DataFrame(Feb, columns = ['Count']).plot(kind = 'bar')
plt.show()
pd.DataFrame(Mar, columns = ['Count']).plot(kind = 'bar' )
plt.show()
pd.DataFrame(Apr, columns = ['Count']).plot(kind = 'bar')
plt.show()

hour = df.resample('H', how=sum)    #sample data by hour 
hour.reset_index(drop=False, inplace=True)
hour.head()

_get_day_of_wk = lambda x:x.weekday() + 1    #calculate the number of logins based on weekdays 
_get_hour = lambda x:x.hour + 1
# Use resamp, since that has the hourly data.
hour['DoW'] = hour['Date'].apply(_get_day_of_wk)
hour['Hour'] = hour['Date'].apply(_get_hour)
print hour.head()

dow = {
    1:'Mo',
    2:'Tu',
    3:'We',
    4:'Th',
    5:'Fr',
    6:'Sa',
    7:'Su'
}
pivoted = hour.drop('Date', axis=1).pivot_table(index='Hour', columns='DoW', aggfunc=sum)
pivoted.columns = [dow[x] for x in range(1,8)]
print pivoted.head()

pivoted.plot()
plt.show()

print pivoted.mean()   #it increases on weekends 

##Mo    367.625000
##Tu    386.166667
##We    430.791667
##Th    498.333333
##Fr    633.666667
##Sa    807.375000
##Su    756.958333

week= df.resample('7D', how=sum)     #resample the data based on weeks 
week.reset_index(drop=False, inplace=True)
week.head()

week.plot(kind = 'bar')
plt.show()


