# Example 1: Customers Dataset

This folder provides a tiny dataset plus JSON query plans that match the Chunk 1 constraints. Use it to validate your Scan -> Select -> Project pipeline end to end.

## Schema

`customers.csv`

| column        | type   | description                      |
|---------------|--------|----------------------------------|
| customer_id   | int    | Unique identifier for the customer |
| name          | string | Customer name                    |
| country       | string | Country code/name                |
| is_active     | bool   | `true` if the customer is active |
| balance       | float  | Account balance in USD           |

### CSV snippet
```
customer_id,name,country,is_active,balance
1,Alice,USA,true,120.50
...
```

`is_active` values are `true`/`false`. Numeric values use dot decimal notation.

## SQL Equivalents for JSON Plans

### query_active_customers.json
```sql
SELECT c.customer_id,
       c.name,
       c.country
FROM customers AS c
WHERE c.is_active = TRUE;
```

### query_high_balance.json
```sql
SELECT c.name,
       c.balance
FROM customers AS c
WHERE c.balance > 100.0;
```

### query_discounted_balance.json
```sql
SELECT c.name,
       c.balance * 0.9 AS discounted_balance
FROM customers AS c
WHERE c.country = 'USA';
```

Each SQL statement exactly matches the corresponding JSON plan in this directory. Use them as ground truth if you want to compare results against SQLite, DuckDB, or any other reference engine.
