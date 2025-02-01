import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read the dataset
df = pd.read_csv("Superstore.csv", encoding="latin1")

# extract first 5 rows
print(df.head(10))

# extract last 5 rows
print(df.tail(10))

# extract columns
print(df.columns)
"""
['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
       'Customer ID', 'Customer Name', 'Segment', 'Country', 'City', 'State',
       'Postal Code', 'Region', 'Product ID', 'Category', 'Sub-Category',
       'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit']
"""

# overview of dataset

print(df.info())  #dtypes: float64(1), int64(8), object(11)
print("Check null values ",df.isnull().sum())
print("Check the duplicate data",df["Order ID"].duplicated().sum())   #duplicate data : = 4985 rows


# delete unwanted column such as row id, postal code
df = df.drop(columns=['Row ID','Postal Code'])
# print(df.columns)
print("Extract statistical values \n",df.describe())

# drop the duplicate values
df.drop_duplicates(subset="Order ID",inplace=True)

# check datatype and modify
date_col  = ['Order Date', 'Ship Date']
for i in date_col:
    df[i]=pd.to_datetime(df[i],dayfirst=True,errors='coerce')

# print(df.info())



# New Quires
print("----------------------------------------------------------------------------------")
# Extract month from date
df['Month'] = df['Order Date'].dt.month
print("----------------------------------------------------------------------------------")

#Count the number of unique customers
print("Unique Customers:", df['Customer ID'].nunique())
print("----------------------------------------------------------------------------------")

#Count the number of orders per customer
print("Orders per Customer:")
print(df['Customer ID'].value_counts())
print("----------------------------------------------------------------------------------")

#List of products ordered by their total sales Highest first
product_sales = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False)
print("Products by Total Sales:\n",product_sales)
print("----------------------------------------------------------------------------------")

#Average discount applied by category
avg_discount_by_category = df.groupby('Category')['Discount'].mean()
print("Average Discount by Category:")
print(avg_discount_by_category)
print("----------------------------------------------------------------------------------")

#Filter orders from a specific state (e.g., California)
california_sales = df[df['State'] == 'California']
print("Sales from California:")
print(california_sales)
print("----------------------------------------------------------------------------------")

#Top 10 customers with the highest total sales
top_customers = df.groupby('Customer ID')['Sales'].sum().sort_values(ascending=False).head(10)
print("Top 10 Customers by Total Sales:")
print(top_customers)
print("----------------------------------------------------------------------------------")

#Filter products with profit greater than $1000
high_profit_products = df[df['Profit'] > 1000]
print("Products with Profit > $1000:")
print(high_profit_products)
print("----------------------------------------------------------------------------------")

#Number of orders by ship mode
ship_mode_count = df['Ship Mode'].value_counts()
print("Number of Orders by Ship Mode:")
print(ship_mode_count)
print("----------------------------------------------------------------------------------")

#Average profit by product category
avg_profit_by_category = df.groupby('Category')['Profit'].mean()
print("Average Profit by Category:")
print(avg_profit_by_category)
print("----------------------------------------------------------------------------------")

#Filter records where profit is negative
negative_profit = df[df['Profit'] < 0]
print("Orders with Negative Profit:")
print(negative_profit)
print("----------------------------------------------------------------------------------")


#total sales by city
sales_by_city = df.groupby('City')['Sales'].sum().sort_values(ascending=False)
print("Total Sales by City:")
print(sales_by_city)
print("----------------------------------------------------------------------------------")

#Total number of products sold by region
products_by_region = df.groupby('Region')['Quantity'].sum()
print("Total Products Sold by Region:")
print(products_by_region)
print("----------------------------------------------------------------------------------")

#Profit by ship mode
profit_by_ship_mode = df.groupby('Ship Mode')['Profit'].sum()
print("Profit by Ship Mode:")
print(profit_by_ship_mode)
print("----------------------------------------------------------------------------------")

#Top 5 products with the highest quantity sold
top_quantity_products = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5)
print("Top 5 Products by Quantity Sold:")
print(top_quantity_products)
print("----------------------------------------------------------------------------------")




# Data Visualization
fig1, axes1 = plt.subplots(2, 2, figsize=(16, 10))

# Total Sales by Region (Bar Plot)
region_summary = df.groupby('Region')[['Sales']].sum()
sns.barplot(x=region_summary.index, y=region_summary['Sales'], ax=axes1[0, 0])
axes1[0, 0].set_title('Total Sales by Region')
axes1[0, 0].set_xlabel('Region')
axes1[0, 0].set_ylabel('Total Sales')

# Profit by Region (Pie Chart)
region_profit = df.groupby('Region')['Profit'].sum()
region_profit.plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3', ax=axes1[0, 1])
axes1[0, 1].set_title('Profit Distribution by Region')
axes1[0, 1].set_ylabel('')

# Sales vs Profit (Scatter Plot)
sns.scatterplot(x='Sales', y='Profit', data=df, ax=axes1[1, 0])
axes1[1, 0].set_title('Sales vs Profit')
axes1[1, 0].set_xlabel('Sales')
axes1[1, 0].set_ylabel('Profit')

# Total Profit by Product Category (Horizontal Bar Plot)
profit_by_category = df.groupby('Category')['Profit'].sum()
sns.barplot(x=profit_by_category.values, y=profit_by_category.index, orient='h', palette='Set2', ax=axes1[1, 1])
axes1[1, 1].set_title('Total Profit by Product Category')
axes1[1, 1].set_xlabel('Total Profit')
axes1[1, 1].set_ylabel('Category')

plt.tight_layout()
plt.show()



fig2, axes2 = plt.subplots(2, 2, figsize=(16, 10))

# Number of Orders by Ship Mode (Bar Chart)
sns.countplot(x='Ship Mode', data=df, palette='Set3', ax=axes2[0, 0])
axes2[0, 0].set_title('Number of Orders by Ship Mode')
axes2[0, 0].set_xlabel('Ship Mode')
axes2[0, 0].set_ylabel('Number of Orders')

# Monthly Sales Trend (Line Plot)
monthly_sales = df.groupby('Month')['Sales'].sum()
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, ax=axes2[0, 1])
axes2[0, 1].set_title('Monthly Sales Trend')
axes2[0, 1].set_xlabel('Month')
axes2[0, 1].set_ylabel('Sales')

# Sales by Customer Segment (Pie Chart)
sales_by_segment = df.groupby('Segment')['Sales'].sum()
sales_by_segment.plot.pie(autopct='%1.1f%%', startangle=90, figsize=(8, 8), cmap='Set2', ax=axes2[1, 0])
axes2[1, 0].set_title('Sales by Customer Segment')
axes2[1, 0].set_ylabel('')

# Correlation between Sales, Quantity, and Profit (Heatmap)
correlation_data = df[['Sales', 'Quantity', 'Profit']].corr()
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=axes2[1, 1])
axes2[1, 1].set_title('Correlation between Sales, Quantity, and Profit')

plt.tight_layout()
plt.show()
