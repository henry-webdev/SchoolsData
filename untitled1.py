#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 14:46:17 2019

@author: test
"""
import csv
import statistics
import plotly.offline as off
import plotly.graph_objects as go
import plotly.express as px
from plotly import subplots
#('Robert Morris University Illinois', '19')
#('Roosevelt University', '17')
def filtered_cols(Row):
    saved_row={}
    for col in Keep_Cols:
        saved_row[col]=Row[col]
    return saved_row
def intify(n):
    try:
        return int(n)
    except:
        return 0
    
Carnige_Codes=['17','19']
Keep_Cols=['LATITUDE', 'LONGITUDE', 'CCBASIC', 'INEXPFTE','SAT_AVG','NPT45_PRIV','NPT45_PUB','RELAFFIL','DEBT_MDN']
Data_File="/Users/test/Downloads/Most-Recent-Cohorts-All-Data-Elements.csv"
saved_schools={}
def read_school_data(path):
    with open(path, 'rU') as data:
        reader = csv.DictReader(data)
        for row in reader:
            yield row
def filter_file(file_name):
    for row in read_school_data(file_name):
        if row["CCBASIC"] in Carnige_Codes  and intify(row["RELAFFIL"])<1:
            saved_schools[row["INSTNM"]]=filtered_cols(row)    
filter_file(Data_File)

RU_like=filter(lambda school:school[1]['CCBASIC']=='17'and \
   school[1]['SAT_AVG'] != 'NULL' ,saved_schools.items()) 
"""
vs.
RU_like=list(filter(lambda school:school[1]['CCBASIC']=='17'and \
   school[1]['SAT_AVG'] != 'NULL' ,saved_schools.items()) )
NOTE *** That unless we store the tuples in a list they dissapears as soon as we use them so after 
we use RU_like in the function below it becomes empty if it is a filter (generator??)  and not a filter wrapped
in list !!!!
Try printing RU_like before and after using it both way to see what happens.  Without the list() we only get 
to use it (consume it) once
"""
    
AVG_SAT =statistics.mean(map( lambda f: int(f[1]['SAT_AVG']),RU_like))
                    
    
SORTED_BY_EXPENSE=sorted(filter(lambda school:school[1]['CCBASIC']=='17',\
    saved_schools.items()),key = lambda k: float(k[1]['INEXPFTE']),reverse=True) 
 
names, expenses, tuition, sats,debt= zip \
(*list( map (lambda school: (school[0],school[1]['INEXPFTE'],\
            intify(school[1]['NPT45_PRIV'])+ intify(school[1]['NPT45_PUB']),school[1]['SAT_AVG'],school[1]['DEBT_MDN']),SORTED_BY_EXPENSE)))

#names, expenses= zip (*list(sorted(map (lambda school: (school[0],school[1]['INEXPFTE']),\
#                                       saved_schools.items()),key = lambda pare: pare[1] )))
#A simple graph with a scatter and a second scatter
MyFirstFigure=go.Figure(
   data=[go.Scatter(y=expenses, x=names, mode='lines+markers')],
   layout=go.Layout(
       title=go.layout.Title(text="School Chart"),orientation=90)     
     )
MyFirstFigure.add_scatter(y=tuition,x=names,mode='lines+markers')    
off.plot(MyFirstFigure)

#using subplots to have 2 yaxis with different scales
gfig=subplots.make_subplots(specs=[[{"secondary_y": True}]])
gfig.add_trace(go.Scatter(y=expenses, x=names, mode='lines+markers', name="Expenses"),
    secondary_y=False)
gfig.add_trace(go.Scatter(y=tuition,x=names,mode='lines+markers',name="Tuition"),
    secondary_y=False)
gfig.add_trace(go.Scatter(y=debt, x=names, mode='lines+markers', name="Debt"),
    secondary_y=False)
gfig.add_trace(go.Scatter(y=sats,x=names,mode='lines+markers',name="SAT"),
    secondary_y=True)
gfig.update_layout(title="Comparative Scool Facts",orientation=90)
gfig.update_yaxes(title_text="Valuein dollars", secondary_y=False)
gfig.update_yaxes(title_text="Scorein points", secondary_y=True)
off.plot(gfig)
