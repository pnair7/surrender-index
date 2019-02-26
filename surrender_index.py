#!/usr/bin/env python
# coding: utf-8
# In[1]:

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
# get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# In[2]:


punts = pd.read_csv('2018punts.csv')
punts.head(100)
punts = punts.drop(columns = ["Detail"])


# In[3]:


punts["Team Code"] = "XXX"
new_array = []
for i in range(len(punts["Tm"])):
    n = punts["Tm"][i]
    if n == "Falcons":
        new_array.append("ATL")
    if n == "Vikings":
        new_array.append("MIN")
    if n == "Texans":
        new_array.append("HTX")
    if n == "Jaguars":
        new_array.append("JAX")
    if n == "Bills":
        new_array.append("BUF")
    if n == "Chiefs":
        new_array.append("KAN")
    if n == "Eagles":
        new_array.append("PHI")
    if n == "Cowboys":
        new_array.append("DAL")
    if n == "Panthers":
        new_array.append("CAR")
    if n == "Steelers":
        new_array.append("PIT")
        #10 down
    if n == "Browns":
        new_array.append("CLE")
    if n == "Bengals":
        new_array.append("CIN")
    if n == "Colts":
        new_array.append("CLT")
    if n == "Cardinals":
        new_array.append("CRD")
    if n == "Redskins":
        new_array.append("WAS")
    if n == "Broncos":
        new_array.append("DEN")
    if n == "Seahawks":
        new_array.append("SEA")
    if n == "Packers":
        new_array.append("GNB")
    if n == "Bears":
        new_array.append("CHI")
    if n == "Dolphins":
        new_array.append("MIA")
        #20 down
    if n == "Titans":
        new_array.append("OTI")
    if n == "49ers":
        new_array.append("SFO")
    if n == "Saints":
        new_array.append("NOR")
    if n == "Buccaneers":
        new_array.append("TAM")
    if n == "Patriots":
        new_array.append("NWE")
    if n == "Giants":
        new_array.append("NYG")
    if n == "Ravens":
        new_array.append("RAV")
    if n == "Chargers":
        new_array.append("SDG")
    if n == "Lions":
        new_array.append("DET")
    if n == "Jets":
        new_array.append("NYJ")
        #30 down
    if n == "Raiders":
        new_array.append("RAI")
    if n == "Rams":
        new_array.append("RAM")
punts["Team Code"] = new_array
punts.head()


# In[4]:


territory_team = [i[0:3] for i in punts.Location]
in_own_territory = punts["Team Code"] == territory_team
punts["In Own Territory"] = in_own_territory
on_50 = punts["Location"] == "50"
punts["On 50?"] = on_50
punts.head()


# In[5]:


def distance_multiplier(togo):
    if togo <= 1:
        return 1
    elif togo <= 3:
        return 0.8
    elif togo <= 6:
        return 0.6
    elif togo <= 9:
        return 0.4
    else:
        return 0.2
d_factor = [distance_multiplier(i) for i in punts["ToGo"]]
punts["Distance Multiplier"] = d_factor
punts.head()



# In[6]:


score_difference = [int(i.split(sep="-")[0]) - int(i.split(sep="-")[1]) for i in punts["Score"]]

def score_multiplier(diff):
    if diff >= 1:
        return 1
    elif diff == 0:
        return 2
    elif diff >= -8:
        return 4
    else:
        return 3
score_factor = [score_multiplier(d) for d in score_difference]
punts["Score Multiplier"] = score_factor
punts.head()


# In[7]:


def clock_multiplier(time, quarter):
    if quarter == 5:
        min = int(time.split(sep=":")[0])
        sec = int(time.split(sep=":")[1])
        seconds_left = (60 * min) + sec
        seconds_since_half = 2700 - seconds_left
    elif quarter == 4:
        min = int(time.split(sep=":")[0])
        sec = int(time.split(sep=":")[1])
        seconds_left = (60 * min) + sec
        seconds_since_half = 1800 - seconds_left
    elif quarter == 3:
        min = int(time.split(sep=":")[0])
        sec = int(time.split(sep=":")[1])
        seconds_left = (60 * min) + sec
        seconds_since_half = 900 - seconds_left
    else:
        return 1
    return ((seconds_since_half * 0.001) ** 3) + 1
clock_factor = [clock_multiplier(punts["Time"][i], punts["Quarter"][i]) for i in range(len(punts["Tm"]))]
punts["Clock Multiplier"] = clock_factor
punts.head()


# In[8]:


def multiplier_before_50(position):
    if position <= 40:
        return 1
    else:
        return multiplier_before_50(position - 1) * 1.1

def multiplier_after_50(position):
    if position == 50:
        return 2.5937424601
    else:
        return multiplier_after_50(position + 1) * 1.2

position = []
for i in range(punts.shape[0]):
    if punts["On 50?"][i]:
        position.append(50)
        continue
    position.append(int(punts["Location"][i].split()[1]))

position_multiplier = [multiplier_after_50(position[i]) if (punts["On 50?"][i] or not punts["In Own Territory"][i]) else multiplier_before_50(position[i]) for i in range(punts.shape[0])]
punts["Position Multiplier"] = position_multiplier
punts.head(40)


# In[9]:


surrender_index = [punts["Distance Multiplier"][i] * punts["Score Multiplier"][i] * punts["Clock Multiplier"][i] * punts["Position Multiplier"][i] for i in range(punts.shape[0])]
punts["Surrender Index"] = surrender_index
punts.head(100)

# In[11]:
print(punts.sort_values(by=["Surrender Index"], ascending=False))
