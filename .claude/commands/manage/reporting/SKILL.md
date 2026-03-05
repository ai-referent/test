---
description: "Génère un rapport de synthèse depuis sales.csv et products.csv avec le classement des meilleurs clients. Utiliser quand l'utilisateur veut un rapport ou des statistiques de ventes."
allowed-tools:
  - Bash
---

# Sales Report

Generate a summary report from `sales.csv` and `products.csv`.

## Steps

1. Run the report:
   ```bash
   python .claude/commands/manage/reporting/scripts/report.py $ARGUMENTS
   ```
   Supported arguments: `--top N` (show top N customers by amount, default 3)

2. Display the report output to the user.
