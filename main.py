"""Command-line client for the Multi-Gateway Payment Processing Engine.

The CLI only ever talks to Aggregator/PaymentMethod through AggregatorFactory
and the polymorphic Aggregator interface - it never instantiates a concrete
aggregator or payment method directly.
"""

from aggregator_factory import AggregatorFactory

AGGREGATOR_CHOICES = {"1": "stripe", "2": "razorpay"}
METHOD_CHOICES = {"1": "card", "2": "upi"}
DISPLAY_LABELS = {"stripe": "Stripe", "razorpay": "Razorpay", "card": "Card", "upi": "UPI"}


def prompt_choice(prompt: str, choices: dict) -> str:
    """Ask the user to pick from `choices` until they enter a valid option."""
    while True:
        print(prompt)
        for key, label in choices.items():
            print(f"{key}. {DISPLAY_LABELS.get(label, label.capitalize())}")
        selected = input("Enter choice: ").strip()
        if selected in choices:
            return choices[selected]
        print(f"Invalid choice '{selected}'. Please try again.\n")


def prompt_payment_details(method_type: str) -> dict:
    """Collect the raw kwargs needed to build a payment method, retrying on empty input."""
    if method_type == "card":
        while True:
            card_number = input("Enter Card Number: ").strip()
            if card_number:
                return {"card_number": card_number}
            print("Card number cannot be empty. Please try again.")
    else:
        while True:
            upi_id = input("Enter UPI ID: ").strip()
            if upi_id:
                return {"upi_id": upi_id}
            print("UPI ID cannot be empty. Please try again.")


def prompt_amount() -> float:
    while True:
        raw_amount = input("Enter amount: ").strip()
        try:
            amount = float(raw_amount)
        except ValueError:
            print("Amount must be a number. Please try again.")
            continue
        if amount <= 0:
            print("Amount must be greater than zero. Please try again.")
            continue
        return amount


def run() -> None:
    print("=== Payment Processing Engine ===\n")

    gateway_name = prompt_choice("\nSelect payment gateway:", AGGREGATOR_CHOICES)
    method_type = prompt_choice("\nSelect payment method:", METHOD_CHOICES)
    payment_details = prompt_payment_details(method_type)
    amount = prompt_amount()

    try:
        aggregator = AggregatorFactory.get_aggregator_object(gateway_name)
        print("\nProcessing payment...\n")
        success = aggregator.call_get_payment_object(method_type, amount, **payment_details)
    except (ValueError, TypeError) as error:
        print(f"Payment failed: {error}")
        return

    if success:
        print("Payment successful.")
        print(f"Gateway: {aggregator.name}")
        print(f"Method: {method_type}")
        print(f"Amount: {amount:.2f}")
    else:
        print("Payment failed. Please try again.")


if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
