# Cofi Checkout System
Cofi is a simple and efficient checkout system designed to manage products, apply discounts, and calculate total prices. This project is built using Python and follows best practices for code organization and testing.

## Features
- Add products with unique codes and prices.
- Apply discounts based on product codes and quantities.
- Calculate total price of items in the cart.
- Easy to extend with new products and discount rules.
- Promotion types supported:
  -  2 for 1: Buy one, get one free.
  - Bulk discount: Reduced price when buying a certain quantity.
  - Bundle discount: Fixed price for a set of products.
- Bundles applied before other discounts.

## Project Structure
- `cofi/`: Main package containing the checkout system implementation.
- `tests/`: Unit tests for the checkout system.
- config.json: Configuration file for products and discounts.
- README.md: Project documentation.
- requirements.txt: List of dependencies.

## How to Use
1. The system is configured using a `config.json` file. You can modify this file to add or change products and discounts.
2. You can scan items in any order using the `scan` method.
   - checkout.scan("VOUCHER")
   - checkout.scan("TSHIRT")
   - checkout.scan("MUG")
3. Call the `total` method to get the total price of the items in the cart.
   - total_price = checkout.total()

## Example Configuration (config.json)
```
{
  "products": [
    {
      "skuName": "VOUCHER",
      "skuID": 1,
      "name": "Cofi Voucher",
      "price": 500
    },
    {
      "skuName": "TSHIRT",
      "skuID": 2,
      "name": "Cofi T-Shirt",
      "price": 2000
    },
    {
      "skuName": "MUG",
      "skuID": 3,
      "name": "Cofi Coffee Mug",
      "price": 750
    }
  ],
  "promotions": [
    {
      "promoName": "SWAG",
      "promoType": "bundle",
      "priority": 1,
      "skuItems": [
        "TSHIRT",
        "VOUCHER",
        "MUG"
      ],
      "price": 2500
    },
    {
      "promoName": "2-for-1 Voucher",
      "promoType": "twoForOne",
      "priority": 2,
      "skuItem": "VOUCHER"
    },
    {
      "promoName": "Bulk  Discount",
      "promoType": "bulkPrice",
      "priority": 1,
      "skuItem": "TSHIRT",
      "minQty": 3,
      "unitPrice": 1900
    }
  ]
}
```
## Requirements
Install dependencies using pip:
```pip install -r requirements.txt
```
## Usage Example
python checkout_with_promo_priority.py --config config.json VOUCHER TSHIRT MUG

## CLI Commands
- `--config`: Specify the path to the configuration file (default is `config.json`
- VOUCHER, TSHIRT, MUG: List of SKUs to scan.

## Running Tests
Run the unit tests using pytest:
```pytest -q
```
### With coverage report 
pytest -q --cov=checkout_with_promo_priority --cov-report=term-missing 

## Project Structure
```.
├── cofi
│   ├── checkout_with_promo_priority.py
│   ├── config.py
│   ├── requirements.txt
│   └── tests
│       ├── test_checkout_with_promos.py
│       └── ...
├   └── README.md
```