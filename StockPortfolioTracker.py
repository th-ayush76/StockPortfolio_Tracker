# Author: Ayush
# Project: Stock Portfolio Tracker 
# Description: just a tracker which makes the user more friendly to the portfolio of the stocks
"""
╔══════════════════════════════════════════╗
║       STOCK PORTFOLIO TRACKER v1.0       ║
║   Track investments using live prices    ║
╚══════════════════════════════════════════╝
"""

import csv
import os
from datetime import datetime

# ─────────────────────────────────────────────
#  HARDCODED STOCK PRICE DICTIONARY (in USD)
# ─────────────────────────────────────────────
STOCK_PRICES = {
    "AAPL":  182.50,   # Apple Inc.
    "TSLA":  248.00,   # Tesla Inc.
    "GOOGL": 175.30,   # Alphabet Inc.
    "AMZN":  195.80,   # Amazon.com Inc.
    "MSFT":  415.20,   # Microsoft Corp.
    "NVDA":  875.40,   # NVIDIA Corp.
    "META":  490.10,   # Meta Platforms Inc.
    "NFLX":  635.00,   # Netflix Inc.
    "BABA":   85.20,   # Alibaba Group
    "RELIANCE": 2950.00,  # Reliance Industries (INR)
    "TCS":  3850.00,   # Tata Consultancy Services (INR)
    "INFY":  1560.00,  # Infosys Ltd (INR)
}

# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

def print_banner():
    print("\n" + "═" * 50)
    print("       📈  STOCK PORTFOLIO TRACKER")
    print("═" * 50)

def print_available_stocks():
    """Show all available stocks with prices."""
    print("\n  Available Stocks:")
    print("  " + "─" * 42)
    print(f"  {'Symbol':<10} {'Company / Stock':<22} {'Price':>8}")
    print("  " + "─" * 42)

    descriptions = {
        "AAPL":     "Apple Inc.",
        "TSLA":     "Tesla Inc.",
        "GOOGL":    "Alphabet Inc.",
        "AMZN":     "Amazon.com Inc.",
        "MSFT":     "Microsoft Corp.",
        "NVDA":     "NVIDIA Corp.",
        "META":     "Meta Platforms",
        "NFLX":     "Netflix Inc.",
        "BABA":     "Alibaba Group",
        "RELIANCE": "Reliance Industries",
        "TCS":      "Tata Consultancy Svcs",
        "INFY":     "Infosys Ltd",
    }

    for symbol, price in STOCK_PRICES.items():
        name = descriptions.get(symbol, symbol)
        print(f"  {symbol:<10} {name:<22} {price:>8.2f}")
    print("  " + "─" * 42)

def print_portfolio_summary(portfolio: dict):
    """Display a formatted portfolio summary table."""
    print("\n" + "═" * 58)
    print("              📊  PORTFOLIO SUMMARY")
    print("═" * 58)
    print(f"  {'Stock':<8} {'Qty':>6}  {'Price':>10}  {'Value':>14}")
    print("  " + "─" * 50)

    total = 0.0
    for symbol, qty in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * qty
        total += value
        print(f"  {symbol:<8} {qty:>6}  {price:>10.2f}  {value:>14.2f}")

    print("  " + "─" * 50)
    print(f"  {'TOTAL INVESTMENT VALUE':>40}  {total:>14.2f}")
    print("═" * 58)
    return total

# ─────────────────────────────────────────────
#  INPUT & VALIDATION
# ─────────────────────────────────────────────

def get_portfolio_from_user() -> dict:
    """Interactively collect stock names and quantities from the user."""
    portfolio = {}

    print_available_stocks()
    print("\n  Enter your stocks one by one.")
    print("  Type 'DONE' when finished.\n")

    while True:
        symbol = input("  Stock symbol (e.g. AAPL): ").strip().upper()

        if symbol == "DONE":
            if not portfolio:
                print("  ⚠  No stocks added yet. Please add at least one.")
                continue
            break

        if symbol not in STOCK_PRICES:
            print(f"  ✗  '{symbol}' not found. Choose from the list above.\n")
            continue

        if symbol in portfolio:
            print(f"  ℹ  {symbol} already added (qty: {portfolio[symbol]}).")
            update = input("     Update quantity? (y/n): ").strip().lower()
            if update != 'y':
                continue

        while True:
            qty_input = input(f"  Quantity for {symbol}: ").strip()
            try:
                qty = int(qty_input)
                if qty <= 0:
                    print("  ✗  Quantity must be a positive integer.")
                    continue
                break
            except ValueError:
                print("  ✗  Please enter a whole number (e.g. 10).")

        portfolio[symbol] = qty
        price = STOCK_PRICES[symbol]
        print(f"  ✓  Added: {qty} × {symbol} @ {price:.2f} = {qty * price:.2f}\n")

    return portfolio

# ─────────────────────────────────────────────
#  FILE SAVING
# ─────────────────────────────────────────────

def save_as_txt(portfolio: dict, total: float):
    """Save the portfolio report as a .txt file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"portfolio_report_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write("=" * 50 + "\n")
        f.write("        STOCK PORTFOLIO REPORT\n")
        f.write(f"  Generated: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"  {'Stock':<8} {'Qty':>6}  {'Price':>10}  {'Value':>14}\n")
        f.write("  " + "-" * 46 + "\n")

        for symbol, qty in portfolio.items():
            price = STOCK_PRICES[symbol]
            value = price * qty
            f.write(f"  {symbol:<8} {qty:>6}  {price:>10.2f}  {value:>14.2f}\n")

        f.write("  " + "-" * 46 + "\n")
        f.write(f"  {'TOTAL':<8} {'':>6}  {'':>10}  {total:>14.2f}\n")
        f.write("\n" + "=" * 50 + "\n")

    print(f"\n  ✅  Saved as text file  →  {filename}")
    return filename

def save_as_csv(portfolio: dict, total: float):
    """Save the portfolio as a .csv file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"portfolio_report_{timestamp}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Stock Symbol", "Quantity", "Price Per Share", "Total Value"])

        for symbol, qty in portfolio.items():
            price = STOCK_PRICES[symbol]
            value = price * qty
            writer.writerow([symbol, qty, f"{price:.2f}", f"{value:.2f}"])

        writer.writerow([])
        writer.writerow(["TOTAL", "", "", f"{total:.2f}"])

    print(f"  ✅  Saved as CSV file     →  {filename}")
    return filename

def offer_save(portfolio: dict, total: float):
    """Ask user if they want to save the results."""
    print("\n  ── Save Results ──────────────────────────────")
    print("  [1]  Save as .txt  (readable report)")
    print("  [2]  Save as .csv  (spreadsheet-ready)")
    print("  [3]  Save both")
    print("  [4]  Skip — don't save")
    print("  " + "─" * 46)

    choice = input("  Your choice (1/2/3/4): ").strip()

    if choice == "1":
        save_as_txt(portfolio, total)
    elif choice == "2":
        save_as_csv(portfolio, total)
    elif choice == "3":
        save_as_txt(portfolio, total)
        save_as_csv(portfolio, total)
    elif choice == "4":
        print("  ℹ  Results not saved.")
    else:
        print("  ✗  Invalid choice. Skipping save.")

# ─────────────────────────────────────────────
#  MAIN PROGRAM
# ─────────────────────────────────────────────

def main():
    print_banner()
    print("\n  Welcome! This tool calculates your total stock")
    print("  investment based on current snapshot prices.\n")

    while True:
        # Step 1: Collect stocks
        portfolio = get_portfolio_from_user()

        # Step 2: Show summary
        total = print_portfolio_summary(portfolio)

        # Step 3: Optionally save
        offer_save(portfolio, total)

        # Step 4: Track another portfolio?
        print("\n  " + "─" * 46)
        again = input("  Track another portfolio? (y/n): ").strip().lower()
        if again != 'y':
            break

    print("\n  Thank you for using Stock Portfolio Tracker! 📈")
    print("═" * 50 + "\n")


if __name__ == "__main__":
    main()