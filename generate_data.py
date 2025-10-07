import csv
import random
import os
from datetime import datetime, timedelta

# Create directory for large datasets
os.makedirs("data/stress_test", exist_ok=True)

# Generate large customers table (10,000 customers)
print("Generating customers table...")
with open("data/stress_test/customers.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["customer_id", "name", "email", "country", "state", "city", "registration_date", "lifetime_value", "is_premium", "credit_score"])
    
    countries = ["USA", "Canada", "UK", "Germany", "France", "Japan", "Australia", "Brazil", "India", "China"]
    states = ["CA", "NY", "TX", "FL", "WA", "IL", "MA", "PA", "OH", "GA"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    
    for i in range(1, 10001):
        name = f"Customer_{i}"
        email = f"customer{i}@example.com"
        country = random.choice(countries)
        state = random.choice(states) if country == "USA" else "N/A"
        city = random.choice(cities)
        reg_date = (datetime.now() - timedelta(days=random.randint(1, 1825))).strftime("%Y-%m-%d")
        lifetime_value = round(random.uniform(100, 50000), 2)
        is_premium = "true" if random.random() > 0.7 else "false"
        credit_score = random.randint(300, 850)
        
        writer.writerow([i, name, email, country, state, city, reg_date, lifetime_value, is_premium, credit_score])

# Generate large products table (5,000 products)
print("Generating products table...")
with open("data/stress_test/products.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["product_id", "name", "category", "subcategory", "brand", "price", "cost", "weight", "is_active", "rating"])
    
    categories = ["Electronics", "Clothing", "Home", "Sports", "Books", "Toys", "Food", "Beauty", "Garden", "Automotive"]
    subcategories = ["Premium", "Standard", "Budget", "Luxury", "Essential"]
    brands = ["BrandA", "BrandB", "BrandC", "BrandD", "BrandE", "BrandF", "BrandG", "BrandH", "BrandI", "BrandJ"]
    
    for i in range(1, 5001):
        name = f"Product_{i}"
        category = random.choice(categories)
        subcategory = random.choice(subcategories)
        brand = random.choice(brands)
        price = round(random.uniform(5, 2000), 2)
        cost = round(price * random.uniform(0.3, 0.7), 2)
        weight = round(random.uniform(0.1, 50), 2)
        is_active = "true" if random.random() > 0.1 else "false"
        rating = round(random.uniform(1, 5), 1)
        
        writer.writerow([i, name, category, subcategory, brand, price, cost, weight, is_active, rating])

# Generate large orders table (50,000 orders)
print("Generating orders table...")
with open("data/stress_test/orders.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["order_id", "customer_id", "order_date", "status", "payment_method", "shipping_method", "subtotal", "tax", "shipping_cost", "total"])
    
    statuses = ["COMPLETED", "PENDING", "SHIPPED", "CANCELLED", "REFUNDED"]
    payment_methods = ["CREDIT", "DEBIT", "PAYPAL", "BITCOIN", "CASH"]
    shipping_methods = ["STANDARD", "EXPRESS", "OVERNIGHT", "ECONOMY", "PRIORITY"]
    
    for i in range(1, 50001):
        customer_id = random.randint(1, 10000)
        order_date = (datetime.now() - timedelta(days=random.randint(1, 730))).strftime("%Y-%m-%d")
        status = random.choice(statuses)
        payment_method = random.choice(payment_methods)
        shipping_method = random.choice(shipping_methods)
        subtotal = round(random.uniform(10, 5000), 2)
        tax = round(subtotal * 0.08, 2)
        shipping_cost = round(random.uniform(5, 50), 2)
        total = round(subtotal + tax + shipping_cost, 2)
        
        writer.writerow([i, customer_id, order_date, status, payment_method, shipping_method, subtotal, tax, shipping_cost, total])

# Generate large order_items table (150,000 items)
print("Generating order_items table...")
with open("data/stress_test/order_items.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent", "line_total"])
    
    item_id = 1
    for order_id in range(1, 50001):
        # Each order has 1-5 items
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            product_id = random.randint(1, 5000)
            quantity = random.randint(1, 10)
            unit_price = round(random.uniform(5, 2000), 2)
            discount_percent = random.choice([0, 5, 10, 15, 20, 25])
            line_total = round(quantity * unit_price * (1 - discount_percent / 100), 2)
            
            writer.writerow([item_id, order_id, product_id, quantity, unit_price, discount_percent, line_total])
            item_id += 1

# Generate inventory table (5,000 entries - one per product)
print("Generating inventory table...")
with open("data/stress_test/inventory.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["inventory_id", "product_id", "warehouse_id", "quantity_on_hand", "quantity_reserved", "reorder_point", "last_restocked"])
    
    for i in range(1, 5001):
        product_id = i
        warehouse_id = random.randint(1, 10)
        quantity_on_hand = random.randint(0, 1000)
        quantity_reserved = random.randint(0, min(100, quantity_on_hand))
        reorder_point = random.randint(10, 100)
        last_restocked = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
        
        writer.writerow([i, product_id, warehouse_id, quantity_on_hand, quantity_reserved, reorder_point, last_restocked])

# Generate reviews table (100,000 reviews)
print("Generating reviews table...")
with open("data/stress_test/reviews.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["review_id", "product_id", "customer_id", "order_id", "rating", "review_date", "verified_purchase", "helpful_count"])
    
    for i in range(1, 100001):
        product_id = random.randint(1, 5000)
        customer_id = random.randint(1, 10000)
        order_id = random.randint(1, 50000)
        rating = random.randint(1, 5)
        review_date = (datetime.now() - timedelta(days=random.randint(1, 730))).strftime("%Y-%m-%d")
        verified_purchase = "true" if random.random() > 0.2 else "false"
        helpful_count = random.randint(0, 500)
        
        writer.writerow([i, product_id, customer_id, order_id, rating, review_date, verified_purchase, helpful_count])

print("Data generation complete!")
print(f"Generated files in data/stress_test/:")
print("- customers.csv (10,000 rows)")
print("- products.csv (5,000 rows)")
print("- orders.csv (50,000 rows)")
print("- order_items.csv (~150,000 rows)")
print("- inventory.csv (5,000 rows)")
print("- reviews.csv (100,000 rows)")
