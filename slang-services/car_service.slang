system: CarService
function: perform_oil_change
agent: AutoShopAI
intent: Provide an oil change service
context:
  service: "oil change"
  budget: 60
  no_wait: true
  availability: "weekend"
input: N/A
output: service_ticket