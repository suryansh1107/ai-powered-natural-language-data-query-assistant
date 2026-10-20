"""
Generate realistic synthetic e-commerce data
for the AI Natural Language Data Query Assistant.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# Reproducible random data
RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)

# Project root:
# scripts/generate_data.py → parent = scripts → parent = project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw data output folder
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("Data generation script started.")

    # We will add customers, products, orders,
    # order_items and payments here in the next steps.

        # -----------------------------
    # Generate customers
    # -----------------------------

    n_customers = 1000

    cities_states = [
        ("Delhi", "Delhi"),
        ("Mumbai", "Maharashtra"),
        ("Pune", "Maharashtra"),
        ("Bengaluru", "Karnataka"),
        ("Hyderabad", "Telangana"),
        ("Chennai", "Tamil Nadu"),
        ("Kolkata", "West Bengal"),
        ("Ahmedabad", "Gujarat"),
        ("Jaipur", "Rajasthan"),
        ("Lucknow", "Uttar Pradesh"),
        ("Noida", "Uttar Pradesh"),
        ("Agra", "Uttar Pradesh"),
        ("Kanpur", "Uttar Pradesh"),
        ("Surat", "Gujarat"),
        ("Bhopal", "Madhya Pradesh"),
        ("Indore", "Madhya Pradesh"),
        ("Patna", "Bihar"),
        ("Chandigarh", "Chandigarh"),
        ("Kochi", "Kerala"),
        ("Guwahati", "Assam"),
    ]

    segments = ["Consumer", "Corporate", "Small Business"]

    customer_ids = np.arange(1, n_customers + 1)

    selected_locations = rng.choice(
        len(cities_states),
        size=n_customers
    )

    names = [
        f"Customer {customer_id}"
        for customer_id in customer_ids
    ]

    cities = [
        cities_states[index][0]
        for index in selected_locations
    ]

    states = [
        cities_states[index][1]
        for index in selected_locations
    ]

    customer_segments = rng.choice(
        segments,
        size=n_customers,
        p=[0.65, 0.20, 0.15]
    )

    signup_dates = pd.to_datetime(
        rng.integers(
            pd.Timestamp("2022-01-01").value // 10**9,
            pd.Timestamp("2025-12-31").value // 10**9,
            size=n_customers
        ),
        unit="s"
    ).date

    customers_df = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "name": names,
            "city": cities,
            "state": states,
            "segment": customer_segments,
            "signup_date": signup_dates,
        }
    )

    customers_path = RAW_DATA_DIR / "customers.csv"
    customers_df.to_csv(customers_path, index=False)

    print(f"Generated {len(customers_df)} customers.")
    print(f"Saved to: {customers_path}")
        # -----------------------------
    # Generate products
    # -----------------------------

    n_products = 1000

    categories = {
        "Electronics": ["Mobiles", "Laptops", "Accessories"],
        "Fashion": ["Clothing", "Footwear", "Watches"],
        "Home & Kitchen": ["Furniture", "Kitchenware", "Decor"],
        "Books": ["Education", "Fiction", "Comics"],
        "Sports": ["Fitness", "Outdoor", "Equipment"],
    }

    product_ids = np.arange(1, n_products + 1)

    category_names = list(categories.keys())

    product_categories = rng.choice(
        category_names,
        size=n_products
    )

    subcategories = [
        rng.choice(categories[category])
        for category in product_categories
    ]

    product_names = [
        f"{category} Product {product_id}"
        for product_id, category in zip(
            product_ids, product_categories
        )
    ]

    prices = np.round(
        rng.uniform(100, 50000, size=n_products), 2
    )

    unit_costs = np.round(
        prices * rng.uniform(0.40, 0.80, size=n_products), 2
    )

    products_df = pd.DataFrame({
        "product_id": product_ids,
        "product_name": product_names,
        "category": product_categories,
        "subcategory": subcategories,
        "price": prices,
        "unit_cost": unit_costs,
    })

    products_path = RAW_DATA_DIR / "products.csv"
    products_df.to_csv(products_path, index=False)

    print(f"Generated {len(products_df)} products.")
    print(f"Saved to: {products_path}")

    # -----------------------------
    # Generate orders
    # -----------------------------

    n_orders = 5000

    order_ids = np.arange(1, n_orders + 1)

    customer_order_ids = rng.integers(
        1, n_customers + 1, size=n_orders
    )

    order_dates = pd.to_datetime(
        rng.integers(
            pd.Timestamp("2024-01-01").value // 10**9,
            pd.Timestamp("2026-01-01").value // 10**9,
            size=n_orders
        ),
        unit="s"
    ).date

    regions = [
        "North", "South", "East", "West", "Central"
    ]

    sales_channels = [
        "Online", "Retail Store", "Mobile App"
    ]

    order_statuses = [
        "Completed", "Cancelled", "Returned"
    ]

    orders_df = pd.DataFrame({
        "order_id": order_ids,
        "customer_id": customer_order_ids,
        "order_date": order_dates,
        "region": rng.choice(regions, size=n_orders),
        "sales_channel": rng.choice(
            sales_channels, size=n_orders
        ),
        "order_status": rng.choice(
            order_statuses,
            size=n_orders,
            p=[0.80, 0.10, 0.10]
        ),
    })

    orders_path = RAW_DATA_DIR / "orders.csv"
    orders_df.to_csv(orders_path, index=False)

    print(f"Generated {len(orders_df)} orders.")
    print(f"Saved to: {orders_path}")
        # -----------------------------
    # Generate order items
    # -----------------------------

    n_order_items = 12000

    order_item_ids = np.arange(1, n_order_items + 1)

    item_order_ids = rng.integers(
        1, n_orders + 1, size=n_order_items
    )

    item_product_ids = rng.integers(
        1, n_products + 1, size=n_order_items
    )

    quantities = rng.integers(
        1, 6, size=n_order_items
    )

    product_price_map = dict(
        zip(products_df["product_id"], products_df["price"])
    )

    item_unit_prices = np.array([
        product_price_map[product_id]
        for product_id in item_product_ids
    ])

    discounts = rng.choice(
        [0.00, 0.05, 0.10, 0.15, 0.20],
        size=n_order_items,
        p=[0.40, 0.20, 0.20, 0.15, 0.05]
    )

    order_items_df = pd.DataFrame({
        "order_item_id": order_item_ids,
        "order_id": item_order_ids,
        "product_id": item_product_ids,
        "quantity": quantities,
        "unit_price": item_unit_prices,
        "discount": discounts,
    })

    order_items_path = RAW_DATA_DIR / "order_items.csv"
    order_items_df.to_csv(order_items_path, index=False)

    print(f"Generated {len(order_items_df)} order items.")
    print(f"Saved to: {order_items_path}")
        # -----------------------------
    # Generate payments
    # -----------------------------

    n_payments = n_orders

    payment_ids = np.arange(1, n_payments + 1)

    payment_order_ids = np.arange(1, n_orders + 1)

    order_totals = (
        order_items_df.assign(
            line_total=(
                order_items_df["quantity"]
                * order_items_df["unit_price"]
                * (1 - order_items_df["discount"])
            )
        )
        .groupby("order_id")["line_total"]
        .sum()
    )

    payment_amounts = np.round(
        [
            order_totals.get(order_id, 0.0)
            for order_id in payment_order_ids
        ],
        2
    )

    payment_methods = rng.choice(
        ["UPI", "Credit Card", "Debit Card", "Net Banking", "COD"],
        size=n_payments,
        p=[0.40, 0.20, 0.20, 0.10, 0.10]
    )

    payment_statuses = rng.choice(
        ["Paid", "Pending", "Failed", "Refunded"],
        size=n_payments,
        p=[0.80, 0.08, 0.07, 0.05]
    )

    payments_df = pd.DataFrame({
        "payment_id": payment_ids,
        "order_id": payment_order_ids,
        "amount": payment_amounts,
        "payment_method": payment_methods,
        "payment_status": payment_statuses,
    })

    payments_path = RAW_DATA_DIR / "payments.csv"
    payments_df.to_csv(payments_path, index=False)

    print(f"Generated {len(payments_df)} payments.")
    print(f"Saved to: {payments_path}")

if __name__ == "__main__":
    main()