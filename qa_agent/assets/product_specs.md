# Product Specifications - E-Shop Checkout

## Pricing Rules
- **Wireless Headphones**: $50.00 per unit.
- **Smart Watch**: $100.00 per unit.

## Discount Codes
- **SAVE15**: Applies a 15% discount to the subtotal (before shipping).
- Any other code is considered invalid.

## Shipping Rules
- **Standard Shipping**: Free ($0.00). Delivery in 5-7 business days.
- **Express Shipping**: Flat rate of $10.00. Delivery in 1-2 business days.

## Order Logic
- Total Price = (Sum of Item Prices * (1 - Discount Rate)) + Shipping Cost.
- Users must select at least one item (quantity > 0) to proceed (implied).
