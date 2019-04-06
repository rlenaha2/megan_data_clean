# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:27:46 2017

@author: Ryan
"""

import pandas as pd
import numpy as np

df = pd.read_csv('Combined Export File.csv')

df = df[['subject_id', 'interval_type', 'interval_number','onset_latency', 
         'efficiency', 'waso', 'sleep_time', 'start_date', 'end_date']]

df_time = df[df['interval_type'] == 'ACTIVE']
df['start_date'] = pd.to_datetime(df_time['start_date'])
df['end_date'] = pd.to_datetime(df_time['end_date'])

start_date = df.groupby('subject_id')['start_date'].min().reset_index()
end_date = df.groupby('subject_id')['end_date'].max().reset_index()

df = df[df['interval_type'] == 'Sleep Summary']

df = df[(df['interval_number']== 'Average(n)') | (df['interval_number']== 'Std Dev(n-1)')]

df_ave = df[df['interval_number'] == 'Average(n)']
df_std = df[df['interval_number'] == 'Std Dev(n-1)']


df_merged = pd.merge(df_ave, df_std, on='subject_id')

df_merged.rename(columns={'onset_latency_x':'Average Sleep Onset Latency',
                          'onset_latency_y':'SD Sleep Onset latency',
                          'efficiency_x': 'Average Efficiency',
                          'efficiency_y': 'SD Efficiency',
                          'waso_x': 'Average WASO',
                          'waso_y': 'SD WASO',
                          'sleep_time_x': 'Average Total Sleep Time',
                          'sleep_time_y': 'SD Total Sleep Time'}, inplace=True)

df_final = df_merged[['subject_id', 'Average Sleep Onset Latency', 'SD Sleep Onset latency', 'Average Efficiency',
         'SD Efficiency', 'Average WASO', 'SD WASO', 'Average Total Sleep Time',
         'SD Total Sleep Time']]

df_final = pd.merge(df_final, start_date)
df_final = pd.merge(df_final, end_date)

df_final['Number of Days'] = (df_final['end_date'] - df_final['start_date']).dt.days

df_final.to_csv('output_file.csv')
