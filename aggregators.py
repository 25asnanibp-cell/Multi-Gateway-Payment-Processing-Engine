"""Aggregator hierarchy.

An Aggregator represents a payment gateway (Stripe, Razorpay, ...). It does
not build PaymentMethod objects itself - it delegates that job to its own
FactoryPaymentMethod subclass, then calls pay() on the result.
"""

from abc import ABC, abstractmethod
from typing import Type

from payment_factories import FactoryPaymentMethod, RazorpayFactory, StripeFactory


class Aggregator(ABC):
    """Base class for every payment gateway."""

    name: str
    processing_fee_percent: float

    @property
    @abstractmethod
    def payment_factory(self) -> Type[FactoryPaymentMethod]:
        """The FactoryPaymentMethod subclass this aggregator delegates to."""
        raise NotImplementedError

    def call_get_payment_object(self, method_type: str, amount: float, **kwargs) -> bool:
        payment_object = self.payment_factory.get_payment_object(method_type, **kwargs)
        return payment_object.pay(amount)


class RazorpayAggregator(Aggregator):
    name = "razorpay"
    processing_fee_percent = 2.0

    @property
    def payment_factory(self) -> Type[FactoryPaymentMethod]:
        return RazorpayFactory


class StripeAggregator(Aggregator):
    name = "stripe"
    processing_fee_percent = 2.9

    @property
    def payment_factory(self) -> Type[FactoryPaymentMethod]:
        return StripeFactory
