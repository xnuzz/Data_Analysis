import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

food_categories = {
    'Dairy': ['Milk', 'Cheese', 'Yogurt'],
    'Bakery': ['Bread', 'Croissant', 'Bagel'],
    'Meat': ['Chicken', 'Beef', 'Pork'],
    'Produce': ['Apple', 'Banana', 'Lettuce'],
    'Frozen': ['Pizza', 'Vegetables', 'Ice Cream'],
    'Canned': ['Soup', 'Beans', 'Tuna'],
    'Snacks': ['Chips', 'Cookies', 'Nuts'],
    'Beverages': ['Soda', 'Juice', 'Water']
}

def random_expiry():
    days = np.random.choice([
        random.randint(1,30),
        random.randint(31,60),
        random.randint(61,90),
        random.randint(91,180),
        random.randint(181,365),
        random.randint(366,730)
    ], p=[0.1,0.12,0.1,0.2,0.25,0.23])
    return (datetime.now() + timedelta(days=int(days))).strftime('%Y-%m-%d')

def generate_inventory(n):
    data = []
    for _ in range(n):
        cat = random.choice(list(food_categories.keys()))
        item = random.choice(food_categories[cat])
        price = round(random.uniform(0.5, 20), 2)
        qty = random.randint(1, 100)
        expiry = random_expiry()
        data.append([item, cat, expiry, price, qty, round(price*qty,2)])
    return pd.DataFrame(data, columns=['Item','Category','Expiry Date','Price','Quantity','Total Value'])

def view_menu(df):
    print("\nView options:")
    print("1. Random sample")
    print("2. By category")
    print("3. Expiring soon (<=30 days)")
    v = input("Choose (1-3): ")
    if v=='1':
        print(df.sample(10))
    elif v=='2':
        cat = input(f"Enter category {list(food_categories.keys())}: ")
        print(df[df['Category']==cat].sample(10) if cat in food_categories else "Invalid category")
    elif v=='3':
        days_left = (pd.to_datetime(df['Expiry Date']) - pd.to_datetime('today')).dt.days
        print(df[days_left<=30].sort_values('Expiry Date').head(10))
    else:
        print("Invalid choice")

def export_menu(df):
    print("\nExport options:")
    print("1. Excel")
    print("2. CSV")
    print("3. Parquet")
    e = input("Choose (1-3): ")
    if e=='1':
        df.to_excel('food_inventory.xlsx', index=False)
        print("Exported to food_inventory.xlsx")
    elif e=='2':
        df.to_csv('food_inventory.csv', index=False)
        print("Exported to food_inventory.csv")
    elif e=='3':
        df.to_parquet('food_inventory.parquet')
        print("Exported to food_inventory.parquet")
    else:
        print("Invalid choice")

def main():
    print("Generating inventory...")
    inventory = generate_inventory(500000)  # Change number as needed
    print("Done! Total items:", len(inventory))
    while True:
        print("\nMENU\n1. View inventory\n2. Export data\n3. Exit")
        c = input("Choose (1-3): ")
        if c=='1':
            view_menu(inventory)
        elif c=='2':
            export_menu(inventory)
        elif c=='3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()