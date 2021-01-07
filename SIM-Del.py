import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import altair as alt
############# LOGO #############
Logo=Image.open('SIM-Logo.jpeg')
st.image(Logo,width=500)
#######Heading Text##########
st.title('**Sales Report**')
##### DataBase File ###################
db=pd.read_excel('Database.xlsx')
db.set_index('Part_No',inplace=True)
########## EDI File Data Split PartNo and Made New DF ################
EDIdata=pd.read_excel('EDI_Jan_21.xlsx')
EDIdata2= pd.DataFrame(EDIdata['Part'].str.split('/',1).to_list(), columns=["Part_No","Part_Name"])
EDIm=pd.concat([EDIdata,EDIdata2],axis=1,sort=False)
EDIm2=EDIm.groupby('Date').sum()
############ Delivery File Data Split PartNo and Made New DF #################
Del=pd.read_excel('Deli_Jan_21.xlsx')
Del1= pd.DataFrame(Del['Part'].str.split('/',1).to_list(), columns=["Part_No","Part_Name"])
Delm=pd.concat([Del,Del1],axis=1,sort=False)
Delm2=Delm.groupby('Part_No').sum()
############## Merg EDI-Del-db #######################
EDIDel=EDIm.merge(Delm[['Date','Part_No','Del-Pcs']],how = 'left', left_on = ['Date','Part_No'], right_on = ['Date','Part_No'])
EDIDel_ok=EDIDel.merge(db[['PartNo','Price']],on='Part_No',how='left')
EDIDel_ok=EDIDel_ok.fillna(0)
EDIDel_ok.set_index('Part_No',inplace=True)

############ Calulate ######################
EDIDel_ok['Diff']=(EDIDel_ok['EDI-Pcs']-EDIDel_ok['Del-Pcs'])
EDIDel_ok['EDI-B']=(EDIDel_ok['EDI-Pcs']*EDIDel_ok['Price'])
EDIDel_ok['Del-B']=(EDIDel_ok['Del-Pcs']*EDIDel_ok['Price'])
EDIDel_ok['Pct(%)']=((EDIDel_ok['Del-Pcs']/EDIDel_ok['EDI-Pcs'])*100)
Sales_B=EDIDel_ok[['Date','EDI-B','Del-B','Pct(%)']]
Del_PCT=((EDIDel_ok['Del-Pcs']/EDIDel_ok['EDI-Pcs'])*100).mean()
Del_Bsum=(EDIDel_ok['Del-Pcs']*EDIDel_ok['Price']).sum()
Del_pcs=EDIDel_ok['Del-Pcs'].sum()
################# Check Box ########################
if st.checkbox('Dailivery and EDI Report'):
    st.subheader('Daily EDI and Delivery details')
    EDIDel_ok[['Date','EDI-Pcs','Del-Pcs','Diff']]
if st.checkbox('Sales Report'):
    st.subheader('Sales Report')
    Sales_B
############# Show Data ##############################
st.subheader('Delivery Performance by %')
st.success(round(Del_PCT,2))
st.subheader('Delivery Performance by B')
st.success(round(Del_Bsum,2))
st.subheader('Delivery Performance (Pcs)')
st.success(round(Del_pcs))
#################### Show Chart #########################
EDIchart=EDIDel_ok[['EDI-Pcs','Del-Pcs']].groupby('Part_No').sum()
EDIchart2=EDIDel_ok['Pct(%)'].groupby('Part_No').mean()
if st.checkbox('Show Performance Chart'):
    st.subheader('Show Performance Chart by Pcs')
    st.bar_chart(EDIchart)
    st.subheader('Show Performance Chart by %')
    st.bar_chart(EDIchart2)
###################Select Part Func #################
EDIDel_ok.set_index('PartNo',inplace=True)
selected_Part = st.multiselect('Select PartNo', ['1632','1732','2532','2633','9231','9330','1231','1530','1630','2731','2831','4333','4433','5130','5230','5330','2001','2031','2902','3102','5402',
'6803','7702','7802','9701','0201','0231','0802','2130','2200','4600','2102','3000','3100','4900','5000','9907','9910','493C','4946','8549','8551','9112','9115','9524',
'9115','9706','9708','0626','0628','5679','5400','5501','0702','0801','8551','0802','1771','T3100','3113','9775','9680','2300-0','2300-1','2300-2'],default=['3000','3100'],)
Show_Part=EDIDel_ok.loc[selected_Part][['Date','EDI-Pcs','Del-Pcs','Pct(%)','Del-B']]
Show_Part_pct=EDIDel_ok.loc[selected_Part]['Pct(%)'].mean()
Show_Part_B=EDIDel_ok.loc[selected_Part]['Del-B'].sum()
Show_Part_P=EDIDel_ok.loc[selected_Part]['Del-Pcs'].sum()
if st.checkbox('Part Selected Data'):
    st.subheader('Sort Part by Selected')
    st.write(Show_Part)

st.subheader('Part Selected Delivery Performance by %')
st.success(round(Show_Part_pct,2))
st.subheader('Part Selected sum of Sales (B)')
st.success(round(Show_Part_B,2))
st.subheader('Part Selected sum of Sales (Pcs)')
st.success(round(Show_Part_P))
    
############### Select Dat ############
EDIDel_ok.set_index('Date',inplace=True)
selected_Date = st.multiselect('Select Delivery Date', ['Jan 1, 2021','Jan 2, 2021','Jan 3, 2021','Jan 4, 2021','Jan 5, 2021','Jan 6, 2021','Jan 7, 2021','Jan 8, 2021','Jan 9, 2021','Jan 10, 2021',
'Jan 11, 2021','Jan 12, 2021','Jan 13, 2021','Jan 14, 2021','Jan 15, 2021','Jan 16, 2021','Jan 17, 2021','Jan 18, 2021','Jan 19, 2021',
'Jan 20, 2021','Jan 21, 2021','Jan 22, 2021','Jan 23, 2021','Jan 24, 2021','Jan 25, 2021','Jan 26, 2021','Jan 27, 2021','Jan 28, 2021','Jan 29, 2021','Jan 30, 2021','Jan 31, 2021'],default=['Jan 4, 2021'],)
Show_Date=EDIDel_ok.loc[selected_Date][['Part','EDI-Pcs','Del-Pcs','Pct(%)','Del-B']]

Show_Date_pct=EDIDel_ok.loc[selected_Date]['Pct(%)'].mean()
Show_Date_B=EDIDel_ok.loc[selected_Date]['Del-B'].sum()
Show_Date_P=EDIDel_ok.loc[selected_Date]['Del-Pcs'].sum()
if st.checkbox('Date Selected Data'):
    st.subheader('Sort by Selected')
    st.write(Show_Date)

st.subheader('Date Selected Delivery Performance by %')
st.success(round(Show_Date_pct,2))
st.subheader('Date Selected sum of Sales (B)')
st.success(round(Show_Date_B,2))
st.subheader('Date Selected sum of Sales (Pcs)')
st.success(round(Show_Date_P))
##############################
st.warning('End Report')
###############################
