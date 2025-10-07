import json
import os

# Create directory if it doesn't exist
os.makedirs("data/stress_test", exist_ok=True)

# Customers schema
customers_schema = {
    "name": "customers",
    "file": "customers.csv",
    "columns": [
        {"name": "customer_id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "email", "type": "string"},
        {"name": "country", "type": "string"},
        {"name": "state", "type": "string"},
        {"name": "city", "type": "string"},
        {"name": "registration_date", "type": "string"},
        {"name": "lifetime_value", "type": "float"},
        {"name": "is_premium", "type": "bool"},
        {"name": "credit_score", "type": "int"}
    ]
}

# Products schema
products_schema = {
    "name": "products",
    "file": "products.csv",
    "columns": [
        {"name": "product_id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "category", "type": "string"},
        {"name": "subcategory", "type": "string"},
        {"name": "brand", "type": "string"},
        {"name": "price", "type": "float"},
        {"name": "cost", "type": "float"},
        {"name": "weight", "type": "float"},
        {"name": "is_active", "type": "bool"},
        {"name": "rating", "type": "float"}
    ]
}

# Orders schema
orders_schema = {
    "name": "orders",
    "file": "orders.csv",
    "columns": [
        {"name": "order_id", "type": "int"},
        {"name": "customer_id", "type": "int"},
        {"name": "order_date", "type": "string"},
        {"name": "status", "type": "string"},
        {"name": "payment_method", "type": "string"},
        {"name": "shipping_method", "type": "string"},
        {"name": "subtotal", "type": "float"},
        {"name": "tax", "type": "float"},
        {"name": "shipping_cost", "type": "float"},
        {"name": "total", "type": "float"}
    ]
}

# Order items schema
order_items_schema = {
    "name": "order_items",
    "file": "order_items.csv",
    "columns": [
        {"name": "item_id", "type": "int"},
        {"name": "order_id", "type": "int"},
        {"name": "product_id", "type": "int"},
        {"name": "quantity", "type": "int"},
        {"name": "unit_price", "type": "float"},
        {"name": "discount_percent", "type": "int"},
        {"name": "line_total", "type": "float"}
    ]
}

# Inventory schema
inventory_schema = {
    "name": "inventory",
    "file": "inventory.csv",
    "columns": [
        {"name": "inventory_id", "type": "int"},
        {"name": "product_id", "type": "int"},
        {"name": "warehouse_id", "type": "int"},
        {"name": "quantity_on_hand", "type": "int"},
        {"name": "quantity_reserved", "type": "int"},
        {"name": "reorder_point", "type": "int"},
        {"name": "last_restocked", "type": "string"}
    ]
}

# Reviews schema
reviews_schema = {
    "name": "reviews",
    "file": "reviews.csv",
    "columns": [
        {"name": "review_id", "type": "int"},
        {"name": "product_id", "type": "int"},
        {"name": "customer_id", "type": "int"},
        {"name": "order_id", "type": "int"},
        {"name": "rating", "type": "int"},
        {"name": "review_date", "type": "string"},
        {"name": "verified_purchase", "type": "bool"},
        {"name": "helpful_count", "type": "int"}
    ]
}

# Write schema files
schemas = [
    ("customers.schema.json", customers_schema),
    ("products.schema.json", products_schema),
    ("orders.schema.json", orders_schema),
    ("order_items.schema.json", order_items_schema),
    ("inventory.schema.json", inventory_schema),
    ("reviews.schema.json", reviews_schema)
]

for filename, schema in schemas:
    with open(f"data/stress_test/{filename}", "w") as f:
        json.dump(schema, f, indent=2)
    print(f"Created {filename}")

print("All schema files created!")
