# Example 2: Orders and Line Items

This folder contains two related tables plus JSON plans that exercise stacked Select operators, Limit, arithmetic in projections, and an equi-join. All examples stay within the Chunk 1 grammar.

## Schemas

Load the provided schema files (`orders.schema.json`, `order_items.schema.json`) into your catalog before running the plans.

`orders.csv`

| column      | type   | description                     |
|-------------|--------|---------------------------------|
| order_id    | int    | Order identifier                |
| customer_id | int    | Owning customer                 |
| status      | string | `OPEN`, `SHIPPED`, `CANCELLED`  |
| total       | float  | Order total in USD              |
| country     | string | Two-to-three letter country tag |
| order_year  | int    | Calendar year of the order      |

`order_items.csv`

| column     | type   | description                    |
|------------|--------|--------------------------------|
| item_id    | int    | Line item identifier           |
| order_id   | int    | Foreign key to orders.order_id |
| sku        | string | Product SKU                    |
| quantity   | int    | Units purchased                |
| unit_price | float  | Price per unit in USD          |

## SQL Equivalents for JSON Plans

### query_open_high_value_orders.json
```sql
SELECT o.order_id,
       o.customer_id,
       o.total
FROM orders AS o
WHERE o.status = 'OPEN'
  AND o.total > 200.0
LIMIT 10;
```

### query_recent_usa_discount.json
```sql
SELECT o.order_id,
       o.country,
       o.total * 0.9 AS discounted_total
FROM orders AS o
WHERE o.country = 'USA'
  AND o.order_year = 2024;
```

### query_open_order_line_totals.json
```sql
SELECT o.order_id,
       i.sku,
       i.quantity * i.unit_price AS line_total
FROM orders AS o
JOIN order_items AS i
  ON o.order_id = i.order_id
WHERE o.status = 'OPEN';
```

Use these statements to cross-check the JSON plans against a reference database if desired.
