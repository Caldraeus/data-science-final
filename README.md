# Data Science Group Projcet

## Introduction
For our group project, we chose to work with a surprisingly limiting dataset containing information on purchases at a Market Basket over two years. Our goal was to look at these purchases and see what we could deduce from the information granted to us. 

## Selection of Data
For our data, we used a dataset from Kaggle containing records of purchases by registered Market Basket members over two years. The dataset had only three columns for us to work with.
1. Member_id
	- This was an integer representing the customer/member's ID
2. Date
	- This was the date that the transaction occured
3. itemDescription
	- This was a one or two word description of what the item was (ex. milk, water, vegetables).

Thankfully, our dataset here didn't have any null values within the columns. At some point, we did convert the date column into proper DateTime format, but that was only for one operation.

## Methods
We used a couple of methods discussed in our course to complete our data analysis.

First, we used `.value_counts()` multiple times to count unique purchases, members, etc. For example, one of our first lines of code is:
```python
counts = df["Member_number"].value_counts()
```
This got us a frame with all the unique member IDs, which we could then take the `len()` of to generate the total amount of members who made purchases.

We also made use of some of the indexing methods we talked about in class. When determining the three members who made the most purchases, we did the following: 
```python
top_3_shoppers = counts.iloc[:3].items()

# Just iterate through and print here because it's easier.
for member_id, purchases in top_3_shoppers:
    print(f"Member ID: {member_id}\n\tTotal Purchases: {purchases}\n")
```
Here, we made use of both `.iloc[]` and `.items()` to index only the top three items, and then only get their items' values. We then iterated over this in a `for x,y in z` format to easily print out their ID and total purchases made at Market Basket.

We also made use of index manipulation. To determine the top 10 most purchased items, we did the following.
```python
print(f"\n\n.: 10 Most Commonly Purchased Items :.\n")

top_10_items = item_counts.iloc[:10].to_frame() # Grab only 10
top_10_items = top_10_items.reset_index() # Reset index
top_10_items.index += 1 # Add 1 to index so we start at 1 and not 0
top_10_items.index.name = "Item No." # Give our index a name.

top_10_items.rename(columns={top_10_items.columns[0]:'Item Name', top_10_items.columns[1]:'# Purchased'}, inplace=True) # Rename the columns

print(top_10_items)
```

Here, we start by doing an `iloc[:10]` to get the top 10 items. We follow this with a `.to_frame()` call to convert this Series to a DataFrame object for manipulation.

Next, we reset our index, because it's the random numbers from the original index currently. This resets it to a basic auto-incrementing number, starting with zero. However, when we rank things in a "top 10" format, we don't start at zero - we start at one. To fix this, we do `top_10_items.index += 1` to quickly add 1 to every index, offsetting it all by one. Finally, we rename our index and columns for readability, then output the results to the terminal window.

We also made use of MatPlotLib in order to construct a few graphs visualizing our data. Thankfully, Pandas and MatPlotLib work in tandem with one another, so the code was simple:
```python
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
```
The most complicated part of this wasn't creating the bar graph, it was actually just using `.apply()` to convert the dates into DateTime, then sorting it all before spitting it into a graph. 

Additionally, we also converted the previously talked about "Top 10 Items" data into a graph, which was a more simple process. 
```python
top_10_graph = top_10_items.plot.bar(x="Item Name")

plt.show()
```
Finally, the last thing we did was a little bit of data analysis. We wanted to calculate the average purchases made by customers who previously purchases re-usable bags against customers who didn't. We will expand more on why later, but the code for this part was a little more complicated.
```python
query = df.query("itemDescription == 'shopping bags'")

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
```
There's a lot going on here, but to break it down simply...

1. We use `.loc` to first grab the mebers who did and didn't purchase bags, making use of Panda's `~` relational symbol.
2. Next, we make sure we filtered properly by calling `.empty`, which if we did everything correctly, should be `True`
3. Finally, we use `.value_counts()` to count the number of bag owners and non-bag owners, then compute the average purchases and output the resulting values.

## Results
First, lets take a look at the Top 3 Customers (ranked by most purchases.)

![Shoppers](https://github.com/Caldraeus/data-science-final/blob/master/Images/Shoppers.png)
___
Next, here are the results for the 10 most popular items bought.

![Top Ten](https://github.com/Caldraeus/data-science-final/blob/master/Images/Figure_1.png)

The figure above shows a graphical representation of the 10 most purchased items from Market Basket. To break it down, we have the following.
1. Whole Milk - 2502 Purchases
2. Other Vegetables - 1898 Purchases
3. Rolls/Buns - 1716 Purchases
4. Soda - 1514 Purchases
5. Yogurt - 1334 Purchases
6. Root Vegetables - 1071 Purchases
7. Tropical Fruit - 1032 Purchases
8. Bottled Water - 933 Purchases
9. Sausage - 924 Purchases
10. Citrus Fruit - 812 Purchases 
___
![Monthly](https://github.com/Caldraeus/data-science-final/blob/master/Images/Figure_2.png)
The figure above shows the amount of purchases per month, over the course of 2014-2015. Specifically, we have the following up values.
1. Jan - 3324
2. Feb - 2997
3. Mar - 3133
4. Apr - 3260
5. May - 3408
6. Jun - 3264
7. Jul - 3300
8. Aug - 3496
9. Sep - 3059
10. Oct - 3261
11. Nov - 3254
12. Dec - 3009
___
We also took some time to compare the average purchases done by customers who purchased re-usable shopping bags against customers who didn't buy re-usable bags.

![Monthly](https://github.com/Caldraeus/data-science-final/blob/master/Images/avgs.png)
## Discussion
After reviewing our data, we came to a few conclusions that could be helpful for Market Basket.

First, let's talk about what the information about our top 3 shoppers could be useful for. The results from this show that our 3 shoppers made around 30 purchases each. This can be useful for determining what products these customers keep coming back for. Additionally, a lot of grocery stores these days have a "rewards" program of some sort. Seeing that the most dedicated shoppers only make 30 purchases over two years can provide insights into when to give a customer a "reward" such as X% off. 

###### *(It is worth mentioning that we don't know any other logistical information about this Market Basket - it could be in the middle of a busy city, a small town, or have other things that affected the purchases and return rate of customers.)*
---
Secondly, we calculated the top 10 most purchased items from the store, then charted it on a graph for some visualization. This revealed some interesting results:
- Whole milk was the most purchased item from the store, which makes sense as milk is one of the most common groceries in the world.
- Yogurt was ranked number five, which was a lot higher than expected.
- It was interesting that Market Basket counts citrus fruit, tropical fruit, other vegetables and root vegetables as seperate categories, instead of being more specific or combining them.
- It's also interesting that Sausage was in the top 10, but steak/chicken/fish wasn't.
---
Next, we calculated the amount of purchases per month from 2014-2015. This, surprisingly, had a very consistent amount of purchases for month, averaging at about 3230.42 purchases per month. 

When we were checking out the data, we noticed February was the only month with less than 3000 purchases. At first, we were trying to figure out what kind  of events happen in February that would make customers  purchase less groceries... until we realised it was because February has significantly less days than every other month.

Additionally, we had expected November and December to have a little bit more purchases than the others, due to Thanksgiving and Christmas. But, as our data showed, there wasn't any significant raise in purchases during these months. 

--- 

Finally, we computed the average purchases of customers who previously bought re-usable bags vs. customers who never bought a re-usable bag. Before we had computed the data, we were skeptical that there would be much a difference, due to the dataset being very large, and we didn't expect there to be much of a difference.

However, after calculating, we saw that customers who bought re-usable bags made, on average, 12 purchases, while customers who never bought re-usable bags only had an average of 9 purchases.

This could be for a couple of reasons - more dedicated customers that come to this store as their main grocery store probably want to save money by investing in re-usable bags instead of buying platsic ones every time, while customers who might not be coming to this Market Basket as often (such as tourists, or people that happen to be in the area) may not have a reason to invest in a re-usable bag.
## Summary
Taking all of our data into consideration, we can come to a few conclusions that might be useful for grocery stores.
1. Market Basket should always be stocking up on milk, more than any other item, due to it's popularity.
2. November and December don't yield more purchases, so you don't need to invest in more items overall during these months - rather, just the items that become more popular instead.
3. Dedicated customers are more likely to buy re-usable bags, and once they do, are more likely to keep making purchases.
4. The average customer makes about 30 purchases over the span of a year to two years.
5. Sausage is a more popular and more oftenly purchased meat than any other meats.

This information can be useful for Market Basket in order to determine what they should stock up on, how they should treat dedicated customers, and what expectations they should have for how many purchases individual customers make.

## References
https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset