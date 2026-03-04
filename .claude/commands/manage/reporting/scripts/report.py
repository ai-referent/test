import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--top", type=int, default=3)
args = parser.parse_args()

products = {}
with open("products.csv") as f:
    for row in csv.DictReader(f):
        products[row["product_id"]] = row

sales = []
with open("sales.csv") as f:
    for row in csv.DictReader(f):
        sales.append(row)

sales.sort(key=lambda r: float(r["amount"]), reverse=True)

print("=== Sales Report ===")
print(f"\nTop {args.top} customers by amount:")
for row in sales[:args.top]:
    print(f"  {row['cust_id']}: {float(row['amount']):.2f} €")

out_of_stock = [p for p in products.values() if int(p["nb_available"]) == 0]
print(f"\nOut of stock ({len(out_of_stock)}/{len(products)} products):")
for p in out_of_stock:
    print(f"  {p['product_id']} - {p['product_name']} ({p['price']} €)")
