"""Checkout engine for a retail system with prioritized promotions.
Key Features:
- Load product and promotion configurations from a JSON file.
- Scan items by SKU and compute total price with applicable promotions.
- Current promotions include:
    - Bundle deals (e.g., buy a set of items for a special price).
    - Bulk pricing (e.g., discounted unit price when buying in bulk).
    - Two-for-one offers (e.g., buy one get one free).
- Promotions are applied based on their priority, allowing for flexible discount strategies.
- Items can be scanned via a command-line interface (CLI).
"""
import json
import os.path
import sys

import click
from collections import Counter


class Checkout:
    """Checkout system with prioritized promotions.
    Attributes:
        products (dict): Maps SKU names to their prices in cents.
        operators (list): List of promotions sorted by priority.
        counts (Counter): Tracks scanned item quantities.
    """

    def __init__(self, cfg):
        # Load products and prices from config
        self.products = {p['skuName']: p['price'] for p in cfg.get('products', [])}

        promo_order = []
        # Load promotions from config

        for promo in cfg.get('promotions', []):
            ptype = promo.get('promoType')
            promo_priority = promo.get('priority', 1)  # Default low priority if not set
            if ptype == 'bundle':
                promo_order.append(
                    {
                        'name': promo['promoName'],
                        'items': list(promo['skuItems']),
                        'price': promo['price'],
                        'priority': promo_priority,
                        'type': ptype
                    }
                )
            elif ptype == 'bulkPrice':
                promo_order.append({
                    'name': promo['promoName'],
                    'priority': promo_priority,
                    'minQty': promo.get('minQty'),
                    'skuItem': promo.get('skuItem'), # Single SKU for bulk pricing
                    'unitPrice': promo.get('unitPrice'),
                    'type': ptype
                })
            elif ptype == 'twoForOne':
                promo_order.append({
                    'name': promo['promoName'],
                    'type': ptype,
                    'priority': promo_priority,
                    'skuItem': promo.get('skuItem')
                })
        self.operators = sorted(promo_order, key=lambda x: x['priority'])
        self.counts = Counter()

    def scan(self, sku):
        """Scan an item by SKU.
        Raises ValueError if SKU is unknown."""
        if sku not in self.products:
            raise ValueError(f"Unknown SKU: {sku}")
        self.counts[sku] += 1

    def total(self):
        """Return total price of all products as a formatted string."""
        total_cents = self._compute_total()
        return f"{total_cents / 100:.2f}€"

    def _compute_total(self):
        """Compute total price applying promotions based on priority."""
        remaining = Counter(self.counts)
        total = 0

        for promo in self.operators:
            if promo.get('type') == 'bundle':
                packs = min(remaining.get(s, 0) for s in promo['items'])
                if packs > 0:
                    total += packs * promo['price']
                    for s in promo['items']:
                        remaining[s] -= packs

            elif promo.get('type') == 'twoForOne':
                sku = promo['skuItem']
                qty = remaining.get(sku, 0)
                # If the quantity is odd, remind user they could get one more free item
                if qty % 2 == 1 and qty > 0:
                    print(f"💡 Tip: You have {qty} {sku}(s). Add one more to get another free under the 2-for-1 offer!")
                if qty > 0:
                    payable = qty - (qty // 2)
                    total += payable * self.products[sku]
                    remaining[sku] = 0
            elif promo.get('type') == 'bulkPrice':
                sku = promo['skuItem']
                qty = remaining.get(sku, 0)
                if qty >= promo['minQty']:
                    total += qty * promo['unitPrice']
                    remaining[sku] = 0
        # Recalculate remaining items after applying all promotions
        for sku, qty in remaining.items():
            if qty > 0:
                total += qty * self.products[sku]

        return total

def load_config(path):
    """Load configuration from a JSON file."""
    with open(path, 'r') as f:
        cfg = json.load(f)
    return Checkout(cfg)


@click.command()
@click.option('--config', default='config.json', help='Path to the configuration file (price in cents).')
@click.argument('items', nargs=-1)
def cli(config, items):
    """CLI for the Checkout system.
    Example usage:
        python checkout_with_promo_priority.py --config config.json VOUCHER TSHIRT MUG
    """

    if not os.path.exists(config):
        click.echo(f"Config file {config} not found.")
        sys.exit(1)
    # Load configuration
    try:
        checkout = load_config(config)
    except Exception as e:
        click.echo(f"Error loading config: {e}")
        sys.exit(1)

    # If no items are scanned
    if not items:
        click.echo("No items scanned. Please provide item SKUs as arguments.")
        sys.exit(1)

    # Scan items
    for item in items:
        try:
            checkout.scan(item)
        except ValueError as e:
            click.echo(f"Skipping unknown item:{item}")
            continue
    click.echo(f"Total amount: €{checkout.total()}")

if __name__ == '__main__':
    cli()



