import pandas as pd # For dataframes and etc
from datetime import datetime as dt # For date/time comprehension
import matplotlib.pyplot as plt

# Import datasheet.
df = pd.read_csv("Data/Groceries_dataset.csv")

print(f"Total Purchases: {len(df.index)}")
# Member_number | Date | itemDescription

counts = df["Member_number"].value_counts()

print(f"Total Unique Shoppers: {len(counts)}")

print("\n.: Top 3 Shoppers by ID :.")

top_3_shoppers = counts.iloc[:3].items()

for member_id, purchases in top_3_shoppers:
    print(f"Member ID: {member_id}\n\tTotal Purchases: {purchases}\n")

item_counts = df["itemDescription"].value_counts()

print(f"How many unique items were purchased?: {len(item_counts)}")

print(f"\n\n.: 10 Most Commonly Purchased Items :.\n")

top_10_items = item_counts.iloc[:10].to_frame() # Grab only 10
top_10_items = top_10_items.reset_index() # Reset index
top_10_items.index += 1 # Add 1 to index so we start at 1 and not 0
top_10_items.index.name = "Item No." # Give our index a name.

top_10_items.rename(columns={top_10_items.columns[0]:'Item Name', top_10_items.columns[1]:'# Purchased'}, inplace=True) # Rename the columns

print(top_10_items)

# Next I think we're going to do some date-time stuff, which is going to be a little bit of a pain, but c'est la vie.
print("\n------------------------------------------------------\n") # Just to separate the output log
items_date = df[['itemDescription','Date']].copy()

# I'm going to use .apply with a lambda function to just to add a "year" and "month" column, just to split up the overall date column
items_date['Year'] = items_date['Date'].apply(lambda x: dt.strptime(x, "%d-%m-%Y").year) 
items_date['Month'] = items_date['Date'].apply(lambda x: dt.strptime(x, "%d-%m-%Y").month) 

# Note: We only have records from 2015 and 2014, so year might not be as useful
sorted_monthly = items_date["Month"].value_counts().sort_index()
print(sorted_monthly)

print(type(sorted_monthly.plot.bar()))

bar_graph = sorted_monthly.plot.bar()
bar_graph.set_xlabel("Month")
bar_graph.set_ylabel("# Purchases")

plt.show()