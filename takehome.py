#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 17:25:47 2021

@author: Lin
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

Survey_Data = pd.read_excel("Analyst_Dataset.xlsx", sheet_name = 'Purchase Exit Survey Data')
#data = pd.read_excel("Analyst_Dataset_test.xlsx")
Airings_Data = pd.read_excel("Analyst_Dataset.xlsx", sheet_name = 'Airings')
Lookup_Data = pd.read_excel("Analyst_Dataset.xlsx", sheet_name = 'Lookup',skiprows=[0])

##### remove unrelated information and convert that into organized dataframe
def survey_preprocess (Survey_Data):
    
    #get the position of survey_data table from excel
    row_ind = Survey_Data.iloc[:, 0].first_valid_index()
    col_ind = Survey_Data.iloc[:, 1].first_valid_index()
    # remove the quarter
    Survey_Data = Survey_Data.drop(row_ind-2)
    # fill na with left value (row)
    for n in range(row_ind-1):
        Survey_Data.iloc[n] = Survey_Data.iloc[n].ffill()
        Survey_Data.iloc[n].astype(str)
    
    Survey_Data.iloc[row_ind-2,] = Survey_Data.iloc[row_ind-2,].replace("January","01").replace("February","02").replace("March","03").replace("April","04").replace("May","05").replace("June","06").replace("July","07").replace("August","08").replace("September","09").replace("October","10").replace("November","11").replace("December","12")
    Survey_Data.iloc[row_ind-1:row_ind,col_ind-1:] = Survey_Data.iloc[row_ind-1:row_ind,col_ind-1:].astype(int).astype(str)
    Survey_Data.iloc[:1,] = list(Survey_Data[0:row_ind].apply(lambda x: '-'.join(x.dropna()), axis=0))
    # create new column name
    Survey_Data.iloc[0,2:]= [datetime.strptime(x,'%Y-%m-%d').strftime("%Y-%m-%d") for x in Survey_Data.iloc[0,2:]]
    Survey_Data.columns = Survey_Data.iloc[0]
    
    Survey_Data.iloc[:,row_ind-1:] = Survey_Data.iloc[:,row_ind-1:].fillna(0)
    Survey_Data = Survey_Data.fillna(method='ffill')    
    Survey_Data = Survey_Data[row_ind:]
    return Survey_Data


Survey_Data = survey_preprocess(Survey_Data)


#### Lookup_Data data : filling NA airlings with original source name
k = len(Lookup_Data)
for n in range(k):
    Lookup_Data.iloc[n] = Lookup_Data.iloc[n].ffill()



#### Merge 3 sheets/dataframe into 1
#DATE = [datetime.strptime(x,'%m/%d/%Y %H:%M') for x in dates]


Survey_Data1 = pd.merge(left = Lookup_Data[['Airings','Exit Survey']] , right = Survey_Data, how = 'right', left_on = 'Exit Survey', right_on = 'Source')

del Survey_Data1['Exit Survey']


############### Cost Per Visitor Driven by the TV Campaign ###############

#resample and tranpose dataframe
Survey_Data2 = Survey_Data1.iloc[:,3:].T
new_header = Survey_Data1['Airings'] 
Survey_Data2.columns = new_header

# get the total visits by the source per month
Survey_Data2.index = pd.to_datetime(Survey_Data2.index)
visits_monthly= Survey_Data2.groupby(pd.Grouper(freq="M")) 
visits_by_month = visits_monthly.sum()

# get the total spend by the sourcce per month
airings_data1 = Airings_Data[['Date/Time ET','Network','Spend']]
airings_data1 = airings_data1.set_index('Date/Time ET')
airings_monthly = airings_data1.groupby([pd.Grouper(freq="M"),'Network'])['Spend']
spend_by_month = airings_monthly.sum()








