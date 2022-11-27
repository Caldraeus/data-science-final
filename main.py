import pandas as pd # For dataframes and etc
from datetime import datetime as dt # For date/time comprehension
import matplotlib.pyplot as plt # For images of data plots

# Import datasheet.
df = pd.read_csv("Data/Groceries_dataset.csv")

print(f"Total Purchases: {len(df.index)}")
# Member_number | Date | itemDescription

counts = df["Member_number"].value_counts()

print(f"Total Unique Shoppers: {len(counts)}")

print("\n.: Top 3 Shoppers by ID :.")

top_3_shoppers = counts.iloc[:3].items()

# Just iterate through and print here because it's easier.
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

# Graphical Ver.
top_10_graph = top_10_items.plot.bar(x="Item Name")

plt.show()

# Next I think we're going to do some date-time stuff, which is going to be a little bit of a pain, but c'est la vie.
print(f"\n{'-'*25}\n") # Just to separate the output log
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

# For our final question, we asked the following:
# "Are customers who bought shopping bags more often buying groceries?"

query = df.query("itemDescription == 'shopping bags'") # Grabs all customer ID's who bought a shopping bag.

# Next, we want to compare the amount of purchases of those who bought shopping bags VS those who did not.
# Only one issue - this data set is very, very large, so there happens to be a LOT more people who just happened to buy things,
# but never bought shopping bags.

# How do we solve this issue?

# Simple - we should compute the averages in order to have some normalised values.

# Compute total purchases / amount of customers == average purchases by those who bought shopping bags
bag_owners_purchases = df.loc[df['Member_number'].isin(query["Member_number"])]
no_bags_purchases = df.loc[~df['Member_number'].isin(query["Member_number"])]

print(f"\n{'-'*25}\n")
print(bag_owners_purchases)
print(no_bags_purchases)

# Just double check that we did the above operations correctly.
check = no_bags_purchases.query("itemDescription == 'shopping bags'").index.empty
print(f"Properly Filtered Bag Owners?: {check}")

# Now that we have # of purchases done by people who bought bags and those who didn't, compute their averages.
# We need to just compute # of customers (just get unique member IDs) then divide the total purchases by that number.

bag_owners = bag_owners_purchases["Member_number"].value_counts() # Gets us # of bag owners
no_bag_owners = no_bags_purchases["Member_number"].value_counts() # Gets us # of people who dont own bags

print(f"Bag Owners: {len(bag_owners)}")
print(f"No Bag Owners: {len(no_bag_owners)}")

avg_bag = len(bag_owners_purchases) / len(bag_owners) # Compute avg
avg_no_bag = len(no_bags_purchases) / len(no_bag_owners) # Compute avg


print(f"\n{'-'*25}\n\nAverage Purchases of Customers w/ Re-usable Bags VS. Average Purchases of Customers w/ No Reusable Bag\n\t\t{avg_bag} vs {avg_no_bag}")

# If someone is buying re-usable bags, it means they probably shop at this store enough to want to
# save money by using re-usable bags, as opposed to someone who only comes to the store for one or
# two purchases, or is just less often buying stuff at this store.