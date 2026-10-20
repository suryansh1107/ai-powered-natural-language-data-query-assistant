"""
Data Quality Validation
AI-Powered Natural Language Data Query Assistant
"""

from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main():
    validation_errors = []
    print("=" * 60)
    print("DATA QUALITY VALIDATION")
    print("=" * 60)

    # Expected dataset sizes
    expected_rows = {
        "customers.csv": 1000,
        "products.csv": 1000,
        "orders.csv": 5000,
        "order_items.csv": 12000,
        "payments.csv": 5000,
    }

    datasets = {}

    # Check files and load data
    for filename, expected_count in expected_rows.items():
        file_path = RAW_DATA_DIR / filename

        if not file_path.exists():
            print(f"\nFAIL: Missing file: {filename}")
            continue

        df = pd.read_csv(file_path)
        datasets[filename] = df

        print(f"\nDataset: {filename}")
        print(f"Rows: {len(df)}")
        print(f"Expected rows: {expected_count}")

        if len(df) == expected_count:
            print("Row count: PASS")
        else:
            print("Row count: FAIL")

        missing_values = int(df.isnull().sum().sum())
        print(f"Missing values: {missing_values}")

        duplicate_rows = int(df.duplicated().sum())
        print(f"Duplicate rows: {duplicate_rows}")

        if missing_values == 0:
            print("Missing-value check: PASS")
        else:
            print("Missing-value check: FAIL")

        if duplicate_rows == 0:
            print("Duplicate-row check: PASS")
        else:
            print("Duplicate-row check: FAIL")

    # Check primary-key uniqueness
    primary_keys = {
        "customers.csv": "customer_id",
        "products.csv": "product_id",
        "orders.csv": "order_id",
        "order_items.csv": "order_item_id",
        "payments.csv": "payment_id",
    }

    print("\n" + "=" * 60)
    print("PRIMARY KEY VALIDATION")
    print("=" * 60)

    for filename, key in primary_keys.items():
        if filename not in datasets:
            continue

        df = datasets[filename]

        if key not in df.columns:
            print(f"{filename}: FAIL - Missing column {key}")
            continue

        duplicate_ids = int(df[key].duplicated().sum())
        null_ids = int(df[key].isnull().sum())

        if duplicate_ids == 0 and null_ids == 0:
            print(f"{filename}: PASS - {key} is unique and non-null")
        else:
            print(
                f"{filename}: FAIL - "
                f"duplicate IDs={duplicate_ids}, null IDs={null_ids}"
            )

    # Check foreign-key relationships
    print("\n" + "=" * 60)
    print("FOREIGN KEY VALIDATION")
    print("=" * 60)

    relationships = [
        ("orders.csv", "customer_id", "customers.csv", "customer_id"),
        ("order_items.csv", "order_id", "orders.csv", "order_id"),
        ("order_items.csv", "product_id", "products.csv", "product_id"),
        ("payments.csv", "order_id", "orders.csv", "order_id"),
    ]

    for child_file, child_col, parent_file, parent_col in relationships:
        if child_file not in datasets or parent_file not in datasets:
            validation_errors.append(f"Missing dataset for relationship:{child_file}->{parent_file}")
            print(f"{child_file}->{parent_file}:FAIL-Missing dataset")
            
            continue
                

        child_df = datasets[child_file]
        parent_df = datasets[parent_file]

        if child_col not in child_df.columns or parent_col not in parent_df.columns:
            print(f"{child_file} -> {parent_file}: FAIL - Missing column")
            continue

        valid_ids = set(parent_df[parent_col].dropna())
        invalid_ids = int(
            (~child_df[child_col].isin(valid_ids)).sum()
        )

        if invalid_ids == 0:
            print(f"{child_file} -> {parent_file}: PASS")
        else:
            print(
                f"{child_file} -> {parent_file}: "
                f"FAIL - {invalid_ids} invalid references"
            )

    print("\n" + "=" * 60)
    print("VALIDATION RUN COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()