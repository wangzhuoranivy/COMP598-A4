import pandas as pd
from bokeh.plotting import figure,curdoc
from bokeh.models import ColumnDataSource,Dropdown
from bokeh.models.tools import HoverTool
from bokeh.layouts import column

from preprocess import *

df = get_df()

# prepare list for dropdown
zip_lst = df['zip_code'].unique().tolist()
zip_lst = list(map(round,zip_lst))
zip_lst = list(map(str,zip_lst))

# create dropdown
d1 = Dropdown(label="Zipcode 1", button_type="warning", menu=zip_lst)
d2 = Dropdown(label="Zipcode 2", button_type="warning", menu=zip_lst)

# callback function for dropdown button 1
def draw_line_zip1(new):
    # new is the variable which saves the new zipcode
    zc = int(new.item)
    df_sub = df[df['zip_code']==zc]
    #source_sub1 = get_graph_df(df_sub)
    
    x,y=get_graph_df(df_sub)
    source_sub1.data = {'month': x, 'duration': y}
    #p.line(x='month',y='duration', line_width=2,color='blue',source=source_sub,legend_label='2020 data in zipcode 1')

# callback function for dropdown button 1
def draw_line_zip2(new):
    zc = int(new.item)
    df_sub = df[df['zip_code']==zc]
    #source_sub2 = get_graph_df(df_sub)
    x,y=get_graph_df(df_sub)
    source_sub2.data = {'month': x, 'duration': y}
    #p.line(x='month',y='duration', line_width=2,color='green',source=source_sub,legend_label='2020 data in zipcode 2')

d1.on_click(draw_line_zip1)
d2.on_click(draw_line_zip2)

# input: df output: df for graph (two cols: month,duration)
def get_graph_df(df):

    months = df['month'].unique()
    months_list = list(months)
    months_list.sort()
    avg_dur = []

    # iterate through months, calculate mean in duration for each 
    for i in months_list:
        df_filter = df[df['month']==i]
        dur_i = df_filter['duration'].mean()
        avg_dur.append(dur_i)

    # df for bokeh plot
    #d = {'month':months_list,'duration':avg_dur}
    #df_new = pd.DataFrame.from_dict(d)
    #source = ColumnDataSource(df_new)
    #return(source)
    return months_list,avg_dur

months_list,avg_dur = get_graph_df(df)
d = {'month':months_list,'duration':avg_dur}

source = ColumnDataSource(data=d)

#source = get_graph_df(df)
null_df = {'month': [],'duration': []}
source_sub1 = ColumnDataSource(data=null_df)
source_sub2 = ColumnDataSource(data=null_df)

# plot
p = figure(x_axis_label='Month', y_axis_label='Average incident create-to-closed time (in hours)',y_range=(0, 400))
p.line(x='month',y='duration',line_width=2,line_color='red',source=source,legend_label='All 2020 data')
p.line(x='month',y='duration', line_width=2,color='blue',source=source_sub1,legend_label='2020 data in zipcode 1')
p.line(x='month',y='duration', line_width=2,color='green',source=source_sub2,legend_label='2020 data in zipcode 2')
p.legend.location = 'top_left'

curdoc().add_root(column(d1,d2,p))

