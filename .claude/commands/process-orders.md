# Process Orders

Simulate the processing of customer orders from `orders.csv`.

For each order:
- Check that the product exists and has available stock in `products.csv`
- Decrement `nb_available` in `products.csv`
- Add the product price to the customer's `amount` in `sales.csv`
- Report processed and rejected orders

## Steps

1. Run the order processor:
   ```bash
   python process_orders.py $ARGUMENTS
   ```
   Supported arguments: `--dry-run` (preview without writing changes)

2. Show the contents of the updated CSV files:
   ```bash
   echo "--- products.csv ---" && cat products.csv
   echo "--- sales.csv ---" && cat sales.csv
   ```

3. Summarize the results to the user, highlighting:
   - How many orders were processed vs rejected
   - Which products are now out of stock (nb_available = 0)
   - Which customers had their sales amount updated
