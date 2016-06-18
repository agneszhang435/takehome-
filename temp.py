import pandas as pd
import matplotlib.pyplot as plt

file = pd.read_json('logins.json')  #read the json file 
print file.loc[1:10]                #print the first 10 rows to see the form of data
 #login_time
#1  1970-01-01 20:16:10
#2  1970-01-01 20:16:37
#3  1970-01-01 20:16:36
#4  1970-01-01 20:26:21
#5  1970-01-01 20:21:41
#6  1970-01-01 20:12:16
#7  1970-01-01 20:35:47
#8  1970-01-01 20:35:38
#9  1970-01-01 20:47:52
#10 1970-01-01 20:26:05

df = pd.DataFrame(file)             #change data to DataFrame form 
df['Date'] = pd.to_datetime(df['login_time']) #change the data type to datetime
print df.head                    #print the first line to see the form 
#<bound method DataFrame.head of login_time Date
#0     1970-01-01 20:13:18 1970-01-01 20:13:18
#1     1970-01-01 20:16:10 1970-01-01 20:16:10
#2     1970-01-01 20:16:37 1970-01-01 20:16:37
#3     1970-01-01 20:16:36 1970-01-01 20:16:36
#4     1970-01-01 20:26:21 1970-01-01 20:26:21
#5     1970-01-01 20:21:41 1970-01-01 20:21:41
#6     1970-01-01 20:12:16 1970-01-01 20:12:16
#7     1970-01-01 20:35:47 1970-01-01 20:35:47
#8     1970-01-01 20:35:38 1970-01-01 20:35:38
#9     1970-01-01 20:47:52 1970-01-01 20:47:52
#10    1970-01-01 20:26:05 1970-01-01 20:26:05
#...                   ...                 ...
#93139 1970-04-13 18:54:02 1970-04-13 18:54:02
#93140 1970-04-13 18:57:38 1970-04-13 18:57:38
#93141 1970-04-13 18:54:23 1970-04-13 18:54:23
# [93142 rows x 2 columns]>

type(df.loc[1,'Date'])  
df['Count'] = 1                 #add a count column 
df = df.set_index('Date').drop('login_time', axis=1) # drop Login_time column and set 'Date' column as index
print df.head()                #print a few lines to see its changes
#   Date               Count    
#1970-01-01 20:13:18      1
#1970-01-01 20:16:10      1
#1970-01-01 20:16:37      1
#1970-01-01 20:16:36      1
#1970-01-01 20:26:21      1


interval = df.resample('15min', how=sum)    #resample the data by 15 minutes interval and count the number of logins in every 15 minutes 
interval.reset_index(drop=False, inplace=True)
print interval.head()
#                 Date  Count
#0 1970-01-01 20:00:00      2
#1 1970-01-01 20:15:00      6
#2 1970-01-01 20:30:00      9
#3 1970-01-01 20:45:00      7
#4 1970-01-01 21:00:00      1

interval.plot()                   #the plot shows the number of logins in each interval 
plt.show()

Day = df.resample('D', how=sum)     #resample the data by one day interval and count the number of logins in every 15 minutes
                                        #start from 1970-01-01 20:00:00 
Day.reset_index(drop=False, inplace=True)
print Day.head()

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
print len(Mar)                          #31 there are 30 days of data 
print len(Apr)                          #12 there are 13 days of data which ends at 1970-04-13

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

#                 Date  Count  DoW  Hour
#0 1970-01-01 20:00:00     24    4    21
#1 1970-01-01 21:00:00      9    4    22
#2 1970-01-01 22:00:00     21    4    23
#3 1970-01-01 23:00:00     58    4    24
#4 1970-01-02 00:00:00     53    5     1

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
#Mo   Tu   We   Th   Fr    Sa    Su
#Hour                                     
#1     531  607  687  816  975  1254  1123
#2     414  566  686  777  957  1562  1355
#3     312  394  482  625  771  1608  1608
#4     236  198  299  375  502  1574  1647
#5     206  149  245  255  353  1719  2107

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


