"""Payment method hierarchy: an abstract PaymentMethod and its concrete
implementations for the Razorpay and Stripe gateways."""

from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    """Common interface every concrete payment method must implement."""

    @abstractmethod
    def get_details(self) -> str:
        """Return a human-readable, non-sensitive summary of this payment method."""
        raise NotImplementedError

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Simulate charging `amount` and return whether it succeeded."""
        raise NotImplementedError


class _CardPayment(PaymentMethod):
    """Shared behavior for card-based payment methods.

    Not registered in any factory directly - concrete gateway card classes
    inherit from this to avoid duplicating masking/validation logic.
    """

    def __init__(self, card_number: str) -> None:
        if not card_number or not card_number.strip():
            raise ValueError("card_number is required")
        self._card_number = card_number.strip()

    def _masked_card_number(self) -> str:
        digits = self._card_number
        if len(digits) <= 4:
            return "*" * len(digits)
        return "*" * (len(digits) - 4) + digits[-4:]

    def pay(self, amount: float) -> bool:
        # Simulated payment - a real integration would call the gateway's API here.
        return amount > 0


class _UPIPayment(PaymentMethod):
    """Shared behavior for UPI-based payment methods."""

    def __init__(self, upi_id: str) -> None:
        if not upi_id or not upi_id.strip():
            raise ValueError("upi_id is required")
        self._upi_id = upi_id.strip()

    def pay(self, amount: float) -> bool:
        # Simulated payment - a real integration would call the gateway's API here.
        return amount > 0


class RazorpayCardPayment(_CardPayment):
    def get_details(self) -> str:
        return f"Razorpay Card ending in {self._masked_card_number()[-4:]}"


class RazorpayUPIPayment(_UPIPayment):
    def get_details(self) -> str:
        return f"Razorpay UPI ({self._upi_id})"


class StripeCardPayment(_CardPayment):
    def get_details(self) -> str:
        return f"Stripe Card ending in {self._masked_card_number()[-4:]}"


class StripeUPIPayment(_UPIPayment):
    def get_details(self) -> str:
        return f"Stripe UPI ({self._upi_id})"
