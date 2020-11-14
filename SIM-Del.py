import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import altair as alt

#st.set_page_config(layout="wide")
st.set_page_config(layout="wide")
Logo=Image.open('SIM-Logo.jpeg')
st.image(Logo,width=500)

st.header('**Delivery and Sales Update**')
st.text('November 2020')
Del=pd.read_excel('Del-Data.xlsx')
#FC.set_index('Part_No',inplace=True)
#Delg=Del.groupby
db=pd.read_excel('Database.xlsx','DB')

Delm=pd.merge(db,Del[['Date','Part_No','Qty','TT-B']],on='Part_No',how='left')
Delm.set_index('PartNo',inplace=True)
Delm=Delm.fillna(0)

Sales=Delm[['Date','Qty','TT-B']]
#Sales=Sales.astype(int)
st.write(Sales)

Saleschart=Sales.groupby('PartNo').sum()
Saleschart=Saleschart[Saleschart>0]
Saleschart=Saleschart.dropna()
st.subheader('Sales (B) by Part Update')
Saleschart['TT-B']
st.bar_chart(Saleschart['TT-B'])
st.subheader('Sales (Pcs) by Part Update')
Saleschart['Qty']
st.bar_chart(Saleschart['Qty'])


Salesupdate=Sales['TT-B'].sum()
st.subheader('Total Sales Update (B)')
st.success(Salesupdate)
#st.dataframe(Sales.apply(lambda y: "%.2f" % y))

selected_Part = st.sidebar.multiselect('Select PartNo', ['1632','1732','2532','2633','9231','9330','1231','1530','1630','2731','2831','4333','4433','5130','5230','5330','2001','2031','2902','3102','5402',
'6803','7702','7802','9701','0201','0231','0802','2130','2200','4600','2102','3000','3100','4900','5000','9907','9910','493C','4946','8549','8551','9112','9115','9524',
'9115','9706','9708','0626','0628','5679','5400','5501','0702','0801','8551','0802','1771','T3100','3113','9775','9680'],default='3000',)
Show_Sales=Sales.loc[selected_Part]

st.subheader('Sort Sales by PartNo-Selected')
st.write(Show_Sales)
SumSales=Show_Sales['Qty'].sum()
SumSales2=Show_Sales['TT-B'].sum()
st.subheader('Total (Pcs)')
st.success(SumSales)
st.subheader('Total (B)')
st.success(SumSales2)

Delm.set_index('Type',inplace=True)

selected_Type = st.sidebar.multiselect('Select Type', ['RM-OES','RM-OEM','MC-OES','MC-OEM'],default='RM-OES',)
Show_Type=Delm.loc[selected_Type]

st.subheader('Sort Sales Update by Type')
Show_Type[['Date','Part_No','Qty','TT-B']]

SUMType=Show_Type[['Date','Part_No','Qty','TT-B']].sum()['TT-B']
st.subheader('SUM By Type Total (B)')
st.success(SUMType)

SUMType2=Show_Type[['Date','Part_No','Qty','TT-B']].sum()['Qty']
st.subheader('SUM By Type Total (Pcs)')
st.success(SUMType2)

