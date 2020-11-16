import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import altair as alt

st.set_page_config(layout="wide")

Logo=Image.open('SIM-Logo.jpeg')
st.image(Logo,width=500)

FC=pd.read_excel('Forecast_W47.xlsx')
FC.set_index('Part_No',inplace=True)

db=pd.read_excel('Database.xlsx','DB')

st.title('The Data Forecast Update')
st.subheader('WeeklyForecast Update')

FC['Total-20']=(FC['WK45']+FC['WK46']+FC['WK47']+FC['WK48']+FC['WK49']+FC['WK50']+FC['WK51']+FC['WK52'])
FCall=FC[['WK45','WK46','WK47','WK48','WK49','WK50','WK51','WK52']]
FCm=pd.merge(FC,db[['PartNo','Part_No','Type','HDMC']],on='Part_No',how='right')
FCm.set_index('PartNo',inplace=True)

st.subheader('The Week Selected Forecast Volumes')

selected_Week = st.sidebar.multiselect('Select Weekly Forecast', ['WK45','WK46','WK47','WK48','WK49','WK50','WK51','WK52'],default=['WK47','WK48'],)

Show_Week=FCm[selected_Week].fillna(0)

FCmTT=FCm["G-TT"] = FCm[selected_Week].sum(axis=1)
FCmTT=FCmTT[FCmTT > 0]

st.write(Show_Week)
st.bar_chart(Show_Week)

st.subheader('The Total Volumes base on WK selected')
st.write(FCmTT)
st.bar_chart(FCmTT)

st.write('The SUM of Volumes based Week Selected')
FCmTTsum=FCmTT.sum()
st.success(FCmTTsum)

selected_Part = st.sidebar.multiselect('Select PartNo', ['1632','1732','2532','2633','9231','9330','1231','1530','1630','2731','2831','4333','4433','5130','5230','5330','2001','2031','2902','3102','5402',
'6803','7702','7802','9701','0201','0231','0802','2130','2200','4600','2102','3000','3100','4900','5000','9907','9910','493C','4946','8549','8551','9112','9115','9524',
'9115','9706','9708','0626','0628','5679','5400','5501','0702','0801','8551','0802','1771','T3100','3113','9775','9680'],default=['3000','3100'],)
Show_Part=FCm.loc[selected_Part][selected_Week]
Show_Part['TT']=Show_Part.sum(axis=1)
Show_Part2=FCm.loc[selected_Part][selected_Week]

st.subheader('Sort Forecast by Part Selected')
st.write(Show_Part)

st.bar_chart(Show_Part2)

FCm=pd.merge(FC,db[['PartNo','Part_No','Type','HDMC','Price']],on='Part_No',how='right')
FCm.set_index('HDMC',inplace=True)

selected_HDMC = st.sidebar.multiselect('Select HDMC',['650T','400T','350T-02','350T-01','NYS'],default=['650T','400T'],)
Show_HDMC=FCm.loc[selected_HDMC][['PartNo','WK46','WK47']]
Show_HDMC['Total']=Show_HDMC.sum(axis=1)
Show_HDMC=Show_HDMC.fillna(0)
Show_HDMC=Show_HDMC[Show_HDMC['Total']>0]

st.subheader('Sort Forecast by HDMC Selected')
st.write(Show_HDMC)
Show_HDMC_SUM2=FCm.loc[selected_HDMC][['WK48','WK49']]
st.bar_chart(Show_HDMC_SUM2)

st.write('The SUM of Selected HDMC')
Show_HDMC_SUM = Show_HDMC.sum()[['WK47', 'WK48', 'Total']]
st.table(Show_HDMC_SUM)

st.success('End of Report')
