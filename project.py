#step 1 :  import all the libraries
import numpy as nm
import pandas as pl
import seaborn as ss
import matplotlib.pyplot as ml

#step 2 :  read/load the file or dataset
df = pl.read_csv("Ecommerce_data.csv")
# print(df.columns)
# pl.set_option("display.max_columns",22)

# step 3 :  to check the overall info of dataset
"""
print(df.info())
print("missing values : =") # check the null values
print(df.isnull().sum())
print("Duplicated values in unique column ")  #check duplicates values
print(df["order_id"].duplicated().sum())
print("Databset statistical summary \n",df.describe())
"""
#step 4 : handle duplicate data or missing/null data
# drop duplicate values on a specific column
df.drop_duplicates(subset="order_id",inplace=True,keep="first")  #keep=False --removes all the duplicate data

# fill the missing data in multiple column at a time
for col in df.select_dtypes(include=['object']):   #replace the null value with the first value in column
    df[col].fillna(df[col].mode()[0])
for col  in df.select_dtypes(include=['number']):  #replace the null value with the mean value of column
    df[col].fillna(df[col].mean())


# step 5 :  check data types and change data type
# df["ship_date"] = df["ship_date"].astype("datetime64[ns]")

date_col  = ['ship_date','order_date']
for i in date_col:
    df[i]=pl.to_datetime(df[i],dayfirst=True,errors='coerce')

# drop rows with invalid dates
df=df.dropna(subset=date_col)

# print(df.info())

"""
['customer_id', 'customer_first_name', 'customer_last_name',
       'category_name', 'product_name', 'customer_segment', 'customer_city',
       'customer_state', 'customer_country', 'customer_region',
       'delivery_status', 'order_date', 'order_id', 'ship_date',
       'shipping_type', 'days_for_shipment_scheduled',
       'days_for_shipment_real', 'order_item_discount', 'sales_per_order',
       'order_quantity', 'profit_per_order']
"""
#extract the new features
df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days

# profit margin
df['profit_margin'] = df['profit_per_order']/df['sales_per_order']

#time based analysis
df['order_year']=df['order_date'].dt.year
df['order_month']=df['order_date'].dt.month
print(df['order_month'])

