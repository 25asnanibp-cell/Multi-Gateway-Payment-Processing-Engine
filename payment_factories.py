"""Factories responsible for creating PaymentMethod objects.

Each gateway (Razorpay, Stripe, ...) owns a factory that maps a method_type
string ("card", "upi") to the concrete PaymentMethod class it should build.
"""

from abc import ABC
from typing import Dict, Type

from payment_methods import (
    PaymentMethod,
    RazorpayCardPayment,
    RazorpayUPIPayment,
    StripeCardPayment,
    StripeUPIPayment,
)


class FactoryPaymentMethod(ABC):
    """Base factory. Subclasses only need to declare their `factory` mapping."""

    factory: Dict[str, Type[PaymentMethod]] = {}

    @classmethod
    def get_payment_object(cls, method_type: str, **kwargs) -> PaymentMethod:
        payment_class = cls.factory.get(method_type)
        if payment_class is None:
            supported = ", ".join(sorted(cls.factory)) or "none"
            raise ValueError(
                f"Unsupported payment method '{method_type}'. Supported: {supported}"
            )
        return payment_class(**kwargs)


class RazorpayFactory(FactoryPaymentMethod):
    factory: Dict[str, Type[PaymentMethod]] = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment,
    }


class StripeFactory(FactoryPaymentMethod):
    factory: Dict[str, Type[PaymentMethod]] = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment,
    }
