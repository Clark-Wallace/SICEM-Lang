system: GroceryPickup
function: pickup_groceries
agent: GroceryAI
intent: Purchase and deliver groceries
context:
  items:
    - "milk"
    - "bread"
    - "eggs"
  max_budget: 50
  delivery_window: "18:00-20:00"
  contactless: true
input: N/A
output: order_receipt