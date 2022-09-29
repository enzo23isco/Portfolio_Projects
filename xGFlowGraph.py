#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 23:37:42 2022

@author: enzovillafuerte
"""
"""
Web Scrapping Section
"""

# import libraries
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


#scrape a single game shots. We will allow users to enter a base url
base_url = 'https://understat.com/match/'
match = str(input('Please enter the match id: '))
url = base_url+match

#Use requests to get the webpage and BeautifulSoup to parse the page
res = requests.get(url)  # <- see tutorial video on this
soup = BeautifulSoup(res.content, 'lxml')    # <- see tutorial video on this
scripts = soup.find_all('script')

#get only the shotsData
strings = scripts[1].string


# strip unnecessary symbols and get only JSON data 
ind_start = strings.index("('")+2 
ind_end = strings.index("')") 
json_data = strings[ind_start:ind_end] 
json_data = json_data.encode('utf8').decode('unicode_escape')

#convert string to json format
data = json.loads(json_data)

""" we are going to create lists for the different variables we want to store. In this case we want to get the coordinates x and y out, the xG values,
the result of the shot and the minute of the shot.

After we created both data_away and data_home variables, we can manually use indexing to see a specific record (example: data_home[1] and see the 
                                                                                                                columns available.
                                                                                                                
Then we will use a loop to iterate through all the records and assign values to the variable lists just created"""                                                                                                                


x = []
y = []
xG = []
result = []
minute = []
player = []
team = []

data_away = data['a']
data_home = data['h']

data_home[1]

for index in range(len(data_home)):
    for key in data_home[index]:
        if key == 'X':
            x.append(data_home[index][key])
        if key == 'Y':
            y.append(data_home[index][key])
        if key == 'h_team':
            team.append(data_home[index][key])
        if key == 'xG':
            xG.append(data_home[index][key])
        if key == 'result':
            result.append(data_home[index][key])   
        if key == 'minute':
            minute.append(data_home[index][key])
        if key == 'player':
            player.append(data_home[index][key])    

for index in range(len(data_away)):
    for key in data_away[index]:
        if key == 'X':
            x.append(data_away[index][key])
        if key == 'Y':
            y.append(data_away[index][key])
        if key == 'a_team':
            team.append(data_away[index][key])
        if key == 'xG':
            xG.append(data_away[index][key])
        if key == 'result':
            result.append(data_away[index][key])
        if key == 'minute':
            minute.append(data_away[index][key])   
        if key == 'player':
            player.append(data_away[index][key])      
 
            
# create the pandas dataframe with the lists previously created with the loops
            
col_names = ['x','y','xG','result','team', 'minute', 'player']
df = pd.DataFrame([x,y,xG,result,team, minute, player],index=col_names)
df = df.T      
    


# export the dataframe into a csv file
df.to_csv("MadridvsBarcaxGDataset.csv")

# when trying to use the groupby function for the xG value, it add each record as if they were integers (non numbers)
#So we gotta get the columns which we want to change the type of the column

df.dtypes  # if we look at the dtypes, we'll see that all the columns are set as objects. We gotta change those that are numeric to float

list_columns = ["x", "y", "xG", "minute"]
for value in list_columns:
    df[value] = df[value].astype(float)
    
df.dtypes # now if we re-run this line we'll see the changes made    

df.groupby(by=["team"])[["xG"]].sum()



"""
xG Flowchart Development Section
"""


#import packages
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# import the dataset
df = pd.read_csv("MadridvsBarcaxGDataset.csv")

#now that we have our dataframe set up, we are going to create some lists to plot the different xG values
#4 lists - home and away xg and minutes
#We start these with zero so our charts will start at 0
a_xG = [0]
h_xG= [0]
a_min = [0]
h_min = [0]

#this finds our team names from the dataframe. This will only work as long as both teams took a shot
hteam = df['team'].iloc[0]  # will get the first record (usually the home team)
ateam = df['team'].iloc[-1]# will get the last record (the away team)

'''
# iterate to the loop to populate the lists a_xG and h_xG previously created
# what the loop is doing here is checking if the record df[team][index] is equal to ateam(away), if true it will append the xG values into a_xG list
'''

for x in range(len(df['xG'])):
    if df['team'][x]==ateam:
        a_xG.append(df['xG'][x])
        a_min.append(df['minute'][x])
    if df['team'][x]==hteam:
        h_xG.append(df['xG'][x])
        h_min.append(df['minute'][x])
        
#this is the function we use to make our xG values be CUMULATIVE rather than single shot values
#it goes through the list and adds the numbers together
def nums_cumulative_sum(nums_list):
    return [sum(nums_list[:i+1]) for i in range(len(nums_list))]        

a_cumulative = nums_cumulative_sum(a_xG)
h_cumulative = nums_cumulative_sum(h_xG)

#this is used to find the total xG. It just creates a new variable from the last item in the cumulative list
alast = round(a_cumulative[-1],2)
hlast = round(h_cumulative[-1],2)


# the graph part

fig, ax = plt.subplots(figsize = (10,5))
fig.set_facecolor('#3d4849')
ax.patch.set_facecolor('#3d4849')

#set up our base layer
mpl.rcParams['xtick.color'] = 'white'
mpl.rcParams['ytick.color'] = 'white'

ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
spines = ['top','bottom','left','right']
for x in spines:
    if x in spines:
        ax.spines[x].set_visible(False)
        
plt.xticks([0,15,30,45,60,75,90])
plt.xlabel('Minute',fontname='Andale Mono',color='white',fontsize=16)
plt.ylabel('xG',fontname='Andale Mono',color='white',fontsize=16)
# plt.suptitle("tuvieja", y=1.05, fontsize=18)
plt.title("Real Madrid vs FC Barcelona xG Flow Chart", color = 'white', fontsize=20)

#plot the step graphs
ax.step(x=a_min,y=a_cumulative,color='#900C3F',label=ateam,linewidth=5,where='post')
ax.step(x=h_min,y=h_cumulative,color='#94C7BF',label=ateam,linewidth=5,where='post')

# FOR HTML COLOR CODES : https://htmlcolorcodes.com/
