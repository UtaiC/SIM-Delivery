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
######Delivery Data #1 Data#############
sales_or=pd.read_excel('Del-Data-Or.xlsx')
sales_or.set_index('Part_No',inplace=True)
sales1=sales_or.groupby('Part_No').sum()
######Database Data#####################
db=pd.read_excel('Database.xlsx')
db.set_index('Part_No',inplace=True)
######Delivery-EDI Data Split PartNo and Made New DF #####################
Del=pd.read_excel('Deli.xlsx')
Del1= pd.DataFrame(Del['Part'].str.split('/',1).to_list(), columns=["Part_No","Part_Name"])
Deliver=pd.concat([Del,Del1],axis=1,sort=False)
Deliver2=Deliver.groupby('Part_No').sum()
###### Maerge 3 DFs #####################
sales=pd.merge(Deliver2,db['Price'],on='Part_No',how='left')
sales2=pd.merge(sales1['TT-B'],sales,on='Part_No',how='left')
sales2['TT-B-2']=(sales2['Del-Pcs']*sales2['Price'])
G_Total_Sales=(sales2['TT-B-2'].sum()+(sales2['TT-B'].sum()))
###### Make Calulate on Deli Data #####################
sales['Del-Sales']=sales['Del-Pcs']*sales['Price']
sales['EDI-Sales']=sales['EDI-Pcs']*sales['Price']
sales['Sales-Pct']=(sales['Del-Sales']/sales['EDI-Sales'])*100
Pct=sales['Sales-Pct'].mean()
###### Show Data Details #####################
Deli_Sales=sales[['EDI-Sales','Del-Sales']]
Deli_Sales2=sales[['EDI-Sales','Del-Sales','Sales-Pct']]
Deli_Sales1=Deli_Sales.fillna(0)
Deli_Sales1=Deli_Sales[Deli_Sales>0]
Deli_Sales2=Deli_Sales2.dropna()

###### Show Data #####################
############CheckBox Menu#########
if st.checkbox('Dailivery and EDI Report'):
    st.subheader('Daily Delivery details')
    Deliver[['Part_No','Date','EDI-Pcs','Del-Pcs']]
if st.checkbox('Sales Report'):
    st.subheader('Sales Report')
    Deli_Sales2
########### Fic On Show % ############
st.subheader('EDI Vs Delivery (%)')
st.success(Pct)
########### Fic On Show B ############
st.subheader('SUM of Sales (B)')
sumsales=G_Total_Sales.sum()
st.success(sumsales)
if st.checkbox('Sales & EDI on Chart'):
    st.bar_chart(Deli_Sales1)
################ Selet Part Section ##############
sales=pd.merge(db,Deliver2,on='Part_No',how='left')
sales2=pd.merge(sales1['TT-B'],sales,on='Part_No',how='left')
sales2.set_index('PartNo',inplace=True)
sales2['TT-B-2']=(sales2['Del-Pcs']*sales2['Price'])
sales2['Pct']=(sales2['Del-Pcs']/sales2['EDI-Pcs'])*100

###################Select Part Func #################
selected_Part = st.multiselect('Select PartNo', ['1632','1732','2532','2633','9231','9330','1231','1530','1630','2731','2831','4333','4433','5130','5230','5330','2001','2031','2902','3102','5402',
'6803','7702','7802','9701','0201','0231','0802','2130','2200','4600','2102','3000','3100','4900','5000','9907','9910','493C','4946','8549','8551','9112','9115','9524',
'9115','9706','9708','0626','0628','5679','5400','5501','0702','0801','8551','0802','1771','T3100','3113','9775','9680','2300-0','2300-1','2300-2'],default=['3000','3100'],)
Show_Part=sales2.loc[selected_Part][['EDI-Pcs','Del-Pcs','TT-B-2','Pct']]
st.subheader('Sort Part by Selected')
st.write(Show_Part)
############### End ############
st.warning('End Report')
###############################
