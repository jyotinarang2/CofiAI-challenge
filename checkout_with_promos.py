import json
from collections import Counter


class Checkout:
    def __init__(self, cfg):
        # Load products and prices from config
        self.products = {p['skuName']: p['price'] for p in cfg.get('products', [])}
        # Load promotions from config
        self.bundles = []
        self.per_sku_promos = {}

        for promo in cfg.get('promotions', []):
            ptype = promo.get('promoType')
            if ptype == 'bundle':
                self.bundles.append(
                    {
                        'name': promo['promoName'],
                        'items': list(promo['skuItems']),
                        'price': promo['price'],

                    }
                )
            elif ptype == 'bulkPrice':
                self.per_sku_promos[promo['skuItem']] = {
                    'name': promo['promoName'],
                    'minQty': promo.get('minQty'),
                    'unitPrice': promo.get('unitPrice'),
                    'type': ptype
                }
            elif ptype == 'twoForOne':
                self.per_sku_promos[promo['skuItem']] = {
                    'name': promo['promoName'],
                    'type': ptype
                }

        self.counts = Counter()

    def scan(self, sku):
        if sku not in self.products:
            raise ValueError(f"Unknown SKU: {sku}")
        self.counts[sku] += 1

    def total(self):
        total_cents = self._compute_total()
        return f"{total_cents / 100:.2f}€"

    def _compute_total(self):
        remaining = Counter(self.counts)
        total = 0
        # Apply bundle promotions first (exclusive)
        for bundle in self.bundles:
            packs = min(remaining.get(s, 0) for s in bundle['items'])
            if packs > 0:
                total += packs * bundle['price']
                for s in bundle['items']:
                    remaining[s] -= packs

        # Test for 2-for-1 voucher tip
        voucher_qty = remaining.get('VOUCHER', 0)
        if voucher_qty % 2 == 1 and voucher_qty > 0:
            print(f"💡 Tip: You have {voucher_qty} voucher(s). Add one more to get another free under the 2-for-1 offer!")

        # Apply per-SKU discounts
        for sku, qty in remaining.items():
            if qty <= 0:
                continue
            base_price = self.products[sku]
            promo = self.per_sku_promos.get(sku)

            if promo and promo.get('type') == 'twoForOne':
                payable = qty - (qty // 2)
                total += payable * base_price

            elif promo and 'minQty' in promo:
                unit_price = promo['unitPrice'] if qty >= promo['minQty'] else base_price
                total += qty * unit_price
            else:
                total += qty * base_price
        return total

def load_config(path):
    with open(path, 'r') as f:
        cfg = json.load(f)
    return Checkout(cfg)

if __name__ == '__main__':
    #Load configuration
    checkout = load_config('config.json')
    # Scan items
    items_to_scan = ["VOUCHER", "TSHIRT", "MUG", "VOUCHER", "MUG", "TSHIRT", "TSHIRT"]
    for item in items_to_scan:
        checkout.scan(item)
    # Calculate total
    print("Total amount:", checkout.total())



