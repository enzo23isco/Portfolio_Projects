#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 20:09:06 2022

@author: enzovillafuerte
"""

####################################################### Data Gathering & Cleaning ##############################################################

# Get the data from April 16, 2022 to May 16, 2022 (accounting for 6 games in most cases)
# import libraries 

import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np

# import the dataset of the stats last 5 games, overall, home and away.
df_overall = pd.read_csv("xG_Test_dataset.csv")
df_home = pd.read_csv("xG_Test_dataset_Home.csv")
df_away = pd.read_csv("xG_Test_dataset_Away.csv")

###### 2. Data Cleaning & Manipulation
# xG, xGA, xPTS metrics have extra values. We need to get rid of them.
df_overall.dtypes # if we pay attention, the type of such columns are "object", we also need to change them to float after manipulation.

# Manipulate Overall Data
df_overall["xG"] = df_overall["xG"].str[:5]
df_overall["xGA"] = df_overall["xGA"].str[:5]
df_overall["xPTS"] = df_overall["xPTS"].str[:5]

df_overall["xG"] = df_overall.xG.astype(float)
df_overall["xGA"] = df_overall.xGA.astype(float)
df_overall["xPTS"] = df_overall.xPTS.astype(float)

# Home Data
df_home["xG"] = df_home["xG"].str[:5]
df_home["xGA"] = df_home["xGA"].str[:5]
df_home["xPTS"] = df_home["xPTS"].str[:5]

df_home["xG"] = df_home.xG.astype(float)
df_home["xGA"] = df_home.xGA.astype(float)
df_home["xPTS"] = df_home.xPTS.astype(float)

# Away Data
df_away["xG"] = df_away["xG"].str[:5]
df_away["xGA"] = df_away["xGA"].str[:5]
df_away["xPTS"] = df_away["xPTS"].str[:5]

df_away["xG"] = df_away.xG.astype(float)
df_away["xGA"] = df_away.xGA.astype(float)
df_away["xPTS"] = df_away.xPTS.astype(float)

########## Later on, we will use a Loop for the Data Type conversion as it would make it more efficient. For now, we will focus on
# finishing the model first


list_metric = ["xG", "xGA", "xPTS"]
list_naming = ["xG per Game", "xGA per Game", "xPTS per Game"]

df_overall["xG per Game"] = df_overall["xG"] / df_overall["M"]

# Get the ratios per game

# Loop for Overall
counter = 0
while counter < len(list_metric):
    df_overall[list_naming[counter]] = df_overall[list_metric[counter]] / df_overall["M"]
    counter += 1

df_overall.head()

# Loop for Home    
counter = 0
while counter < len(list_metric):
    df_home[list_naming[counter]] = df_home[list_metric[counter]] / df_home["M"]
    counter += 1
    
# Loop for Away 
counter = 0
while counter < len(list_metric):
    df_away[list_naming[counter]] = df_away[list_metric[counter]] / df_away["M"]
    counter += 1
    
    


# check that the dataset are OK
df_overall.head()
df_home.head()
df_away.head()

######################################################### Model Development #################################################################

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# create list for home and away teams
list_home = ["Real Madrid", "Rayo Vallecano", "Valencia", "Elche", "Alaves", "Granada", "Osasuna", "Barcelona", "Real Sociedad", "Sevilla"]
list_away = ["Real Betis", "Levante", "Celta Vigo", "Getafe", "Cadiz", "Espanyol", "Mallorca", "Villarreal", "Atletico Madrid", "Athletic Club"]
# ---------------------------------------------------------------------------------------------------------------------------------------------------


##### APPROACH 1 - Create two different dataframes for Home and Away specifically

# OVERALL DATASET

# Filter and get a subset of the dataset only showing the Home Teams, and then the Away teams
home_teams_df = df_overall.loc[df_overall["Team"].isin(list_home)] # Method 2: Select Rows where Column Value is in List of Values
away_teams_df = df_overall.loc[df_overall["Team"].isin(list_away)]
# set index so we can filter data based on Team and then re-index so we have them in order (THIS MAY NOT BE NEEDED)
home_teams_df = home_teams_df.set_index("Team")
away_teams_df = away_teams_df.set_index("Team")

home_teams_df = home_teams_df.reindex(list_home)
away_teams_df = away_teams_df.reindex(list_away)
#reset the index again so we can leverage the loop using counter
home_teams_df = home_teams_df.reset_index()
away_teams_df = away_teams_df.reset_index()

# HOME DATASET - ONE DATASET

one_home_teams_df = df_home.loc[df_home["Team"].isin(list_home)] # Method 2: Select Rows where Column Value is in List of Values
one_away_teams_df = df_home.loc[df_home["Team"].isin(list_away)]
# set index so we can filter data based on Team and then re-index so we have them in order (THIS MAY NOT BE NEEDED)
one_home_teams_df = one_home_teams_df.set_index("Team")
one_away_teams_df = one_away_teams_df.set_index("Team")

one_home_teams_df = one_home_teams_df.reindex(list_home)
one_away_teams_df = one_away_teams_df.reindex(list_away)
#reset the index again so we can leverage the loop using counter
one_home_teams_df = one_home_teams_df.reset_index()
one_away_teams_df = one_away_teams_df.reset_index()


# AWAY DATASET - TWO DATASET

two_home_teams_df = df_away.loc[df_away["Team"].isin(list_home)] # Method 2: Select Rows where Column Value is in List of Values
two_away_teams_df = df_away.loc[df_away["Team"].isin(list_away)]

# set index so we can filter data based on Team and then re-index so we have them in order (THIS MAY NOT BE NEEDED)
two_home_teams_df = two_home_teams_df.set_index("Team")
two_away_teams_df = two_away_teams_df.set_index("Team")

two_home_teams_df = two_home_teams_df.reindex(list_home)
two_away_teams_df = two_away_teams_df.reindex(list_away)

#reset the index again so we can leverage the loop using counter
two_home_teams_df = two_home_teams_df.reset_index()
two_away_teams_df = two_away_teams_df.reset_index()

#
# use list_naming previously created (xG per Game, xGA per game, xPTS per Game | will focus only in xG and xGA per game)

'''
THIS MAY NOT BE NECESSARY

home_teams_df[list_naming[0]][list_home[0]] # will retrieve Real Madrid xG per Game metric
# the previous is the equivalent as saying home_teams_df["xG per Game"]["Real Madrid"], but we will leverage a loop with counters
home_teams_df[list_naming[1]][list_home[0]] # will retrieve Real Madrid's xGA per game metric

away_teams_df[list_naming[0]][list_away[0]] # will retrieve Real Madrid xG per Game metric
away_teams_df[list_naming[1]][list_away[0]] # will retrieve Real Madrid's xGA per game metric

'''


""""
TOTAL GOALS BASED ON xG PREDICTION

"""
# BEFORE IF STATEMENTS AND LOOP: MANUALLY TYPE THE COMPARISON

counter_team = 0
counter_stats = 0
confidence_metric = 0

# CREATE DATAFRAME FOR CONFIDENCE LEVELS
list_of_loops = ["L1" , "L2", "L3", "L4", "L5", "L6"]
data = [1,2,3,4,5,6,7,8,9,10]
df_confidence_level = pd.DataFrame(data, columns=["Game Code"])

# for loop to create the columns into the dataframe
for var in list_of_loops:
    df_confidence_level[var] = 0


''' THIS IS IMPORTANT: EXPLAINS THE LOOP IN A STEP - STEP PROCESS
# first we are going to compare 2 xG values, Madrid vs Betis
home_teams_df["Team"][0] # displays Real Madrid
home_teams_df["xG per Game"][0] # displays xG per Game

away_teams_df["Team"][0] # displays Real Betis
away_teams_df["xG per Game"][0]

#NOW COMPARE - TOTAL GOALS SCORED


if (home_teams_df["xG per Game"][0] + away_teams_df["xG per Game"][0]) > 3.0:  # PARAMETER HERE IS MORE THAN 3 IN XG TERMS
    print("Bet +2.5 on " + home_teams_df["Team"][0] + " vs " + away_teams_df["Team"][0])
else:
    print("Do not place a Bet +2.5 on " + home_teams_df["Team"][0] + " vs " + away_teams_df["Team"][0])
''' 
# now we need to get that through a loop

# LOOP FOR GENERAL xG - PARAMETER > 3
while counter_team < len(list_home):
    if (home_teams_df["xG per Game"][counter_team] + away_teams_df["xG per Game"][counter_team]) > 3.0:  # PARAMETER HERE IS MORE THAN 3 IN XG TERMS
        print("Bet +2.5 on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
        df_confidence_level["L1"][counter_team] = 1
        # confidence_metric += 1
    else:
        print("Do not place a Bet +2.5 on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
    counter_team += 1    
counter_team = 0   

# LOOP FOR GENERAL xGA - PARAMETER > 2
while counter_team < len(list_home):
    if (home_teams_df["xGA per Game"][counter_team] + away_teams_df["xGA per Game"][counter_team]) > 2.5:  # PARAMETER HERE IS MORE THAN 3 IN XG TERMS
        print("Bet +2.5 on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
        # confidence_metric += 1
        df_confidence_level["L2"][counter_team] = 1
    else:
        print("Do not place a Bet +2.5 on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
    counter_team += 1    
counter_team = 0   

# LOOP FOR xG for LOCAL TEAMS vs xG away teams # DONE
while counter_team < len(list_home):
    if (one_home_teams_df["xG per Game"][counter_team] + two_away_teams_df["xG per Game"][counter_team]) > 3.0:
        print("Bet +2.5 on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
        df_confidence_level["L3"][counter_team] = 1
    else:    
        print("Do not place a bet +2.5 on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
    counter_team += 1
counter_team = 0   

# LOOP FOR xG for LOCAL TEAMS vs xGA for AWAY teams
while counter_team < len(list_home):
    if (one_home_teams_df["xG per Game"][counter_team] + two_away_teams_df["xGA per Game"][counter_team]) > 3.0:
        print("Bet +2.5 on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
        df_confidence_level["L4"][counter_team] = 1
    else:    
        print("Do not place a bet +2.5 on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
    counter_team += 1
counter_team = 0   

# LOOP FOR xGA for LOCAL TEAMS vs xGA for AWAY Teams
while counter_team < len(list_home):
    if (one_home_teams_df["xGA per Game"][counter_team] + two_away_teams_df["xGA per Game"][counter_team]) > 3.0:
        print("Bet +2.5 on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
        df_confidence_level["L5"][counter_team] = 1
    else:    
        print("Do not place a bet +2.5 on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
    counter_team += 1
counter_team = 0  

# LOOP FOR xGA for LOCAL vs xG for AWAY Teams 
while counter_team < len(list_home):
    if (one_home_teams_df["xGA per Game"][counter_team] + two_away_teams_df["xG per Game"][counter_team]) > 3.0:
        print("Bet +2.5 on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
        df_confidence_level["L6"][counter_team] = 1
    else:    
        print("Do not place a bet +2.5 on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
    counter_team += 1
counter_team = 0  

df_confidence_level

# add 2 columns for a sum of row and the "stake"

df_confidence_level["Sum L"] = df_confidence_level.sum(axis=1) - df_confidence_level["Game Code"]
df_confidence_level["Relative Stake"] = df_confidence_level["Sum L"] / 6
df_confidence_level

# print BET Messages
# ---------------------------------------------------------------------------------------------------------------------------------

for var in df_confidence_level["Game Code"] - 1:
    if df_confidence_level["Relative Stake"][var] >= 0.5:
        print(f"POTENTIAL +2.5 BET: {list_home[var]} vs {list_away[var]}, STAKE: {df_confidence_level['Relative Stake'][var]}")
    else:
        print(f"Do not bet: {list_home[var]} vs {list_away[var]}")

# ---------------------------------------------------------------------------------------------------------------------------------     

""""

GAME WINNER BASED ON xG PREDICTION

(The idea is to find teams that produce higher xG values than the opposition within different context to predict a winner)

#L1: Team 1 with a higher xG total value of ___parameter____ than Team 2
#L1.2: Team 2 with a higher xG total value of ____parameter____ than team 2
#L2: Team 1 xG + Team 2 xGA > ____parameter_____
#L3: Team 2 xGA 

"""   
# We have already created the teams list

# Figure out how to include the output of each into a dataset 
# thinking of creating a dataset with a R column with results of Null, L, V,
# CREATE DATAFRAME FOR CONFIDENCE LEVELS

list_of_loops_1 = ["L1" , "L2", "L3", "L4"]
data_1 = [1,2,3,4,5,6,7,8,9,10]
df_confidence_level_1 = pd.DataFrame(data_1, columns=["Game Code"])

# for loop to create the columns into the dataframe
for var in list_of_loops_1:
    df_confidence_level_1[var] = 0


# LOOP 1: xG Home vs xG Away (OVERALL)
while counter_team < len(list_home):
    # we want to see if it's positive, meaning that local team has higher xG values
    if home_teams_df["xG per Game"][counter_team] - away_teams_df["xG per Game"][counter_team] > 0.0: 
        # now we will see if it meet the parameter (let's use >0.7 first)
        if home_teams_df["xG per Game"][counter_team] - away_teams_df["xG per Game"][counter_team] > 0.7:
            print("Bet L on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
            df_confidence_level_1["L1"][counter_team] = "L"
        else:
            print("Do not place a Result Bet on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
            df_confidence_level_1["L1"][counter_team] = "None"
    # we want to see if it's negative, meaning that away team has higher xG values
    elif home_teams_df["xG per Game"][counter_team] - away_teams_df["xG per Game"][counter_team] < 0.0: 
        # now we will see if it meet the parameter (let's use < -0.7 first)
        if home_teams_df["xG per Game"][counter_team] - away_teams_df["xG per Game"][counter_team] < -0.7:
            print("Bet V on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
            df_confidence_level_1["L1"][counter_team] = "V"
        else:
            print("Do not place a Result Bet on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team]) 
            df_confidence_level_1["L1"][counter_team] = "None"
    else:
        print("Do not place a Result Bet on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
        df_confidence_level_1["L1"][counter_team] = "None"
    counter_team += 1
counter_team = 0    
        
            
# LOOP 2: xG Home vs xG Away (last 5 games home and away)        
while counter_team < len(list_home):
    if (one_home_teams_df["xG per Game"][counter_team] - two_away_teams_df["xG per Game"][counter_team]) > 0.0:
        if one_home_teams_df["xG per Game"][counter_team] - two_away_teams_df["xG per Game"][counter_team] > 0.7:
            print("Bet L on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
            df_confidence_level_1["L2"][counter_team] = "L"
        else:
            print("Do not place a Result Bet on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
            df_confidence_level_1["L2"][counter_team] = "None"
    elif (one_home_teams_df["xG per Game"][counter_team] - two_away_teams_df["xG per Game"][counter_team]) < 0.0:
        if one_home_teams_df["xG per Game"][counter_team] - two_away_teams_df["xG per Game"][counter_team] < -0.7:
            print("Bet V on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
            df_confidence_level_1["L2"][counter_team] = "V"
        else:
            print("Do not place a Result Bet on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
            df_confidence_level_1["L2"][counter_team] = "None"
    else:
        print("Do not place a Result Bet on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])   
        df_confidence_level_1["L2"][counter_team] = "None"
    counter_team += 1
counter_team = 0    
        
            

# LOOP 3: (xG Home + xGA Visit) - (xGA Home + xG Visit) (Overall first) # Parameter: difference of 0.7
while counter_team < len(list_home):
    if (home_teams_df["xG per Game"][counter_team] + away_teams_df["xGA per Game"][counter_team]) - (home_teams_df["xGA per Game"][counter_team] + away_teams_df["xG per Game"][counter_team]) > 0.0:
        if (home_teams_df["xG per Game"][counter_team] + away_teams_df["xGA per Game"][counter_team]) - (home_teams_df["xGA per Game"][counter_team] + away_teams_df["xG per Game"][counter_team]) > 0.7:
            print(" Bet L on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
            df_confidence_level_1["L3"][counter_team] = "L"
        else: 
            print("Do not place a Result Bet on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
            df_confidence_level_1["L3"][counter_team] = "None"
    elif (home_teams_df["xG per Game"][counter_team] + away_teams_df["xGA per Game"][counter_team]) - (home_teams_df["xGA per Game"][counter_team] + away_teams_df["xG per Game"][counter_team]) < 0.0:  
        if (home_teams_df["xG per Game"][counter_team] + away_teams_df["xGA per Game"][counter_team]) - (home_teams_df["xGA per Game"][counter_team] + away_teams_df["xG per Game"][counter_team]) < -0.7:
            print("Bet V on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
            df_confidence_level_1["L3"][counter_team] = "V"
        else:
            print("Do not place a Result Bet on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team]) 
            df_confidence_level_1["L3"][counter_team] = "None"
    else:
        print("Do not place a Result Bet on " + home_teams_df["Team"][counter_team] + " vs " + away_teams_df["Team"][counter_team])
        df_confidence_level_1["L3"][counter_team] = "None"
    counter_team += 1
counter_team = 0            
            

# LOOP 4: (xG Home + xGA Visit) - (xGA Home + xG Visit) (Home and away games)
while counter_team < len(list_home):
    if (one_home_teams_df["xG per Game"][counter_team] + two_away_teams_df["xGA per Game"][counter_team]) - (one_home_teams_df["xGA per Game"][counter_team] + two_away_teams_df["xG per Game"][counter_team]) > 0.0:
        if (one_home_teams_df["xG per Game"][counter_team] + two_away_teams_df["xGA per Game"][counter_team]) - (one_home_teams_df["xGA per Game"][counter_team] + two_away_teams_df["xG per Game"][counter_team]) > 0.7:
            print(" Bet L on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
            df_confidence_level_1["L4"][counter_team] = "L"
        else: 
            print("Do not place a Result Bet on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
            df_confidence_level_1["L4"][counter_team] = "None"
    elif (one_home_teams_df["xG per Game"][counter_team] + two_away_teams_df["xGA per Game"][counter_team]) - (one_home_teams_df["xGA per Game"][counter_team] + two_away_teams_df["xG per Game"][counter_team]) < 0.0:  
        if (one_home_teams_df["xG per Game"][counter_team] + two_away_teams_df["xGA per Game"][counter_team]) - (one_home_teams_df["xGA per Game"][counter_team] + two_away_teams_df["xG per Game"][counter_team]) < -0.7:
            print("Bet V on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
            df_confidence_level_1["L4"][counter_team] = "V"
        else:
            print("Do not place a Result Bet on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])  
            df_confidence_level_1["L4"][counter_team] = "None"
    else:
        print("Do not place a Result Bet on " + one_home_teams_df["Team"][counter_team] + " vs " + two_away_teams_df["Team"][counter_team])
        df_confidence_level_1["L4"][counter_team] = "None"
    counter_team += 1
counter_team = 0    


df_confidence_level_1


# ------------------------------------------------------------------|
# ------------------------------------------------------------------|
print(df_confidence_level)
print(df_confidence_level_1)
# ------------------------------------------------------------------|
# ------------------------------------------------------------------|

# Still need to determine the parameters statistically










