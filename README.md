# Multi-Gateway Payment Processing Engine

A small, extensible payment processing engine that simulates routing a
payment through one of several gateways (Stripe, Razorpay), each supporting
multiple payment methods (Card, UPI).

## Design Patterns Used

- **Factory Pattern** – `RazorpayFactory` / `StripeFactory` create the
  correct `PaymentMethod` subclass from a `method_type` string.
- **Abstract Factory concept** – each `Aggregator` owns a specific
  `FactoryPaymentMethod` subclass (`payment_factory`), so the aggregator you
  pick determines the *family* of payment methods you get.
- **Factory Pattern (again, one level up)** – `AggregatorFactory` creates
  `Aggregator` objects from a gateway name, so the CLI never instantiates a
  concrete aggregator directly.
- **Abstraction / Inheritance / Polymorphism** – `PaymentMethod`,
  `FactoryPaymentMethod`, and `Aggregator` are `ABC`s; all concrete gateways
  and payment methods are used through these common interfaces.
- **Encapsulation** – payment details (card number, UPI ID) live only inside
  the relevant payment method class; card numbers are masked when displayed.
- **Delegation** – `Aggregator.call_get_payment_object` doesn't build
  payment methods itself; it delegates that to `self.payment_factory`.
- **Open/Closed Principle** – adding a new gateway (e.g. PayPal) never
  requires editing existing classes; see "Adding a New Gateway" below.

## Project Structure

```
payment_processing_engine/
├── payment_methods.py      # PaymentMethod (abstract) + concrete methods
├── payment_factories.py    # FactoryPaymentMethod (abstract) + gateway factories
├── aggregators.py          # Aggregator (abstract) + StripeAggregator/RazorpayAggregator
├── aggregator_factory.py   # AggregatorFactory
├── main.py                 # CLI entry point
├── test_payment_engine.py  # unittest test suite
└── README.md
```

## How to Run

```bash
cd payment_processing_engine
python3 main.py
```

You'll be prompted to choose a gateway, a payment method, the relevant
payment details, and an amount.

## How to Run Tests

```bash
cd payment_processing_engine
python3 -m unittest test_payment_engine.py -v
```

## Example CLI Workflow

```
=== Payment Processing Engine ===

Select payment gateway:
1. Stripe
2. Razorpay

Enter choice: 1

Select payment method:
1. Card
2. UPI

Enter choice: 2

Enter UPI ID: user@upi
Enter amount: 1500

Processing payment...

Payment successful.
Gateway: stripe
Method: upi
Amount: 1500.00
```

Invalid gateway/method choices, empty card numbers or UPI IDs, and
non-numeric or non-positive amounts are all caught and re-prompted without
crashing the application.

## Adding a New Gateway (e.g. PayPal)

No existing file needs to change. Just add the new pieces and register them:

1. In `payment_methods.py`: add `PayPalCardPayment` and `PayPalUPIPayment`
   (subclassing `_CardPayment` / `_UPIPayment` or `PaymentMethod` directly).
2. In `payment_factories.py`: add

   ```python
   class PayPalFactory(FactoryPaymentMethod):
       factory = {"card": PayPalCardPayment, "upi": PayPalUPIPayment}
   ```

3. In `aggregators.py`: add

   ```python
   class PayPalAggregator(Aggregator):
       name = "paypal"
       processing_fee_percent = 3.5

       @property
       def payment_factory(self):
           return PayPalFactory
   ```

4. In `aggregator_factory.py`: add `"paypal": PayPalAggregator` to
   `AggregatorFactory.factory`.

The CLI, the `Aggregator` base class, and every existing gateway keep
working unmodified.
