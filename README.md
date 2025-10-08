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

