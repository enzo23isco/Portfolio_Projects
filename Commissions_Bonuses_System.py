#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 19:38:38 2022

@author: enzovillafuerte
"""

# import libraries
import pandas as pd 
import numpy as np

# import data file for testing and cleaning

report = pd.read_csv("salesReport copy.csv")
report.head()

# CLEANING
# Get rid of the columns we won't use
report.columns 
'''
Columns:
    
Vendedor, Numero de Documento, 
Fecha de Venta, Marca, Producto/Servicio, Precio Neto Unitario, Cantidad, Subtotal Impuestos, Subtotal Bruto,
Costo Neto Unitario, Costo Total Neto 

ADD one column: "Comission"
'''

report_final = report.drop(columns=['Tipo Movimiento', 'Sucursal', 'Vendedor', 'Cliente', 'RUC Cliente',
       'Tipo de Documento', 'Prefijo del Numero de Serie',
       'Numero de Serie', 'Tracking Number', 'Fecha Venta', 
       'Lista de Precio', 'Variante', 'Otros Atributos', 'Margen', '% Margen', 
       'Detalle de Productos/Servicios Pack/Promo',
       'Dirección Cliente', 'Ciudad Cliente', 'Ciudad', 'Email Cliente'])

report_final.head()

# Set parameters for Brand commissions by creating a dataframe. This values come from the company's management Input
# initialize list of lists
data = [['pegasus', 0.02], ['zoje', 0.02], ['brother', 0.03], ['domesticas', 0.03], ['maya', 0.03],
        ['new star', 0.02], ['yakumo', 0.02], ['santian', 0.03], ['kingtex', 0.015], ['juki', 0.01],
        ['kangda', 0.02], ['yao han', 0.02], ['seize', 0.03], ['weihuan', 0.03], ['battistella', 0.03],
        ['otm', 0.02], ['cn', 0.01]]
 
# Create the pandas DataFrame
brand_commissions_df = pd.DataFrame(data, columns=['Marca', 'Comision'])
 
# print dataframe.
brand_commissions_df.head()

# CONVERT report_final["Marca"] to lower
report_final["Marca"] = report_final["Marca"].str.lower()

''' 
--------------------------------------------------------------------------------------
PART 1: BRAND COMMISSIONS - (TESTED AND WORKING)
--------------------------------------------------------------------------------------
'''

# Create a new column (commissions):
report_final["Brand Commissions"] = ' '   # we gotta append the values obtain in the loop into this

# For loop to iterate...

counter_1 = 0
counter_2 = 0


len(brand_commissions_df["Marca"])

while (counter_1 < len(report_final["Marca"])-1):
    while (counter_2 < len(brand_commissions_df['Marca'])):
        if report_final['Marca'][counter_1] == brand_commissions_df['Marca'][counter_2]:
            a = report_final["Subtotal Bruto"][counter_1] * brand_commissions_df["Comision"][counter_2]
            report_final["Brand Commissions"][counter_1] = a
            print(brand_commissions_df['Marca'][counter_2], counter_2, a)
        counter_2 += 1
    counter_2 = 0
    counter_1 += 1


length = len(report_final["Brand Commissions"])-1
report_final["Brand Commissions"][0:length].sum()  # esto tengo que modificarlo


report_final.columns
brand_commissions_df.columns

# TOTAL COMISION: DONE

''' 
--------------------------------------------------------------------------------------
PART 2: PRODUCTION BONUS (IF SUM()>X: A ....) 
--------------------------------------------------------------------------------------
'''
usd = float(input("Enter the USD currency value: "))

bonus_1 = 40000*usd
bonus_2 = 50000*usd
bonus_3= 60000*usd


if (report_final["Brand Commissions"][0:length].sum()) > bonus_3:
    production_bonus = 300*usd
    print("Production bonus of: " + str(production_bonus))
elif (report_final["Brand Commissions"][0:length].sum()) > bonus_2:
    production_bonus = 200*usd
    print("Production bonus of: " + str(production_bonus)) 
elif (report_final["Brand Commissions"][0:length].sum()) > bonus_1:
    production_bonus = 100*usd
    print("Production bonus of: " + str(production_bonus))
else:
    production_bonus = 0
    print("No bonus available given the parameters")
 

# TOTAL PRODUCTION BONUS: DONE    

''' 
--------------------------------------------------------------------------------------
PART 3: BRAND BONUS (Thinking of doing a pivot/groupby table and try to convert it into a dataframe
                     for later querying | MIGHT WORK, but will look for solutions online.
--------------------------------------------------------------------------------------
'''    
# get the rows from the original dataframe if it contains ["pegasus", "zoje" or "maya"] as the brand associated with the product
pegasus_data = report_final.loc[report_final["Marca"] == "pegasus"]  
zoje_data = report_final.loc[report_final["Marca"] == "zoje"]        
maya_data = report_final.loc[report_final["Marca"] == "maya"]

pegasus_data = pegasus_data.append(zoje_data)
pegasus_data = pegasus_data.append(maya_data)
brand_bonus_df = pegasus_data # append the data in a single dataframe called brand_bonus_df

brand_bonus_df = brand_bonus_df.reset_index()
brand_bonus_df.head()

# add brand variables for sum of values
pegasus_total = 0
zoje_total = 0
maya_total = 0

counter = 0
# create the loop

while counter < len(brand_bonus_df):
    if brand_bonus_df["Marca"][counter] == "pegasus":
        pegasus_total = float(brand_bonus_df["Subtotal Bruto"][counter])
        counter += 1
    elif brand_bonus_df["Marca"][counter] == "zoje":    
        zoje_total += float(brand_bonus_df["Subtotal Bruto"][counter])
        counter += 1
    else:
        maya_total += float(brand_bonus_df["Subtotal Bruto"][counter])
        counter += 1
    
total_bonus = 0        
        
if pegasus_total >= 36000:
    total_bonus += 410

if zoje_total >= 36000:
    total_bonus += 410

if maya_total >= 36000:
    total_bonus += 820
    
    
''' 
--------------------------------------------------------------------------------------
PART 4: DISPLAY RESULTS
--------------------------------------------------------------------------------------
'''

total_pay = report_final['Brand Commissions'][0:length].sum() +     production_bonus + total_bonus

print(f"The total Commission value is: {report_final['Brand Commissions'][0:length].sum()} S/.")
print(f"The total Production Bonus is: {production_bonus} S/.")
print(f"The total Brand Bonus is: {total_bonus} S/.")

print(f"TOTAL AMOUNT TO PAY: {total_pay} S/.")    
     
    

