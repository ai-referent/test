"""
Process orders from orders.csv and update products.csv and sales.csv.

Usage: python process_orders.py [--dry-run]
"""
import csv
import sys
from pathlib import Path

ORDERS_FILE = Path("orders.csv")
PRODUCTS_FILE = Path("products.csv")
SALES_FILE = Path("sales.csv")


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def process_orders(dry_run=False):
    orders = read_csv(ORDERS_FILE)
    products = {r["product_id"]: r for r in read_csv(PRODUCTS_FILE)}
    sales = {r["cust_id"]: r for r in read_csv(SALES_FILE)}

    processed = []
    rejected = []

    for order in orders:
        cust_id = order["cust_id"]
        product_id = order["product_id"]
        order_date = order["order_date"]

        product = products.get(product_id)
        if product is None:
            rejected.append((order, "product not found"))
            continue

        if int(product["nb_available"]) <= 0:
            rejected.append((order, "out of stock"))
            continue

        price = float(product["price"])

        if not dry_run:
            product["nb_available"] = int(product["nb_available"]) - 1

            if cust_id not in sales:
                sales[cust_id] = {"cust_id": cust_id, "amount": 0.0}
            sales[cust_id]["amount"] = float(sales[cust_id]["amount"]) + price

        processed.append((order, price))

    if not dry_run:
        write_csv(
            PRODUCTS_FILE,
            list(products.values()),
            ["product_id", "product_name", "price", "nb_available"],
        )
        write_csv(
            SALES_FILE,
            list(sales.values()),
            ["cust_id", "amount"],
        )

    # Report
    print(f"{'[DRY RUN] ' if dry_run else ''}Order processing report")
    print("=" * 40)
    print(f"  Orders read   : {len(orders)}")
    print(f"  Processed     : {len(processed)}")
    print(f"  Rejected      : {len(rejected)}")

    if processed:
        print("\nProcessed orders:")
        for order, price in processed:
            print(
                f"  [{order['order_date']}] cust={order['cust_id']} "
                f"product={order['product_id']} price={price:.2f}"
            )

    if rejected:
        print("\nRejected orders:")
        for order, reason in rejected:
            print(
                f"  [{order['order_date']}] cust={order['cust_id']} "
                f"product={order['product_id']} -> {reason}"
            )

    print()
    if not dry_run:
        print("products.csv and sales.csv updated.")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    process_orders(dry_run=dry_run)
