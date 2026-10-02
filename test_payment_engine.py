import unittest

from aggregator_factory import AggregatorFactory
from aggregators import RazorpayAggregator, StripeAggregator
from payment_factories import RazorpayFactory, StripeFactory
from payment_methods import (
    RazorpayCardPayment,
    RazorpayUPIPayment,
    StripeCardPayment,
    StripeUPIPayment,
)


class TestPaymentMethodCreation(unittest.TestCase):
    def test_stripe_card_payment_creation(self):
        payment = StripeFactory.get_payment_object("card", card_number="4111111111111111")
        self.assertIsInstance(payment, StripeCardPayment)

    def test_stripe_upi_payment_creation(self):
        payment = StripeFactory.get_payment_object("upi", upi_id="user@upi")
        self.assertIsInstance(payment, StripeUPIPayment)

    def test_razorpay_card_payment_creation(self):
        payment = RazorpayFactory.get_payment_object("card", card_number="4111111111111111")
        self.assertIsInstance(payment, RazorpayCardPayment)

    def test_razorpay_upi_payment_creation(self):
        payment = RazorpayFactory.get_payment_object("upi", upi_id="user@upi")
        self.assertIsInstance(payment, RazorpayUPIPayment)

    def test_invalid_payment_method_raises(self):
        with self.assertRaises(ValueError):
            StripeFactory.get_payment_object("wallet", wallet_id="abc")

    def test_kwargs_reach_constructor_correctly(self):
        # StripeUPIPayment must actually receive its upi_id through **kwargs.
        payment = StripeFactory.get_payment_object("upi", upi_id="alice@bank")
        self.assertIn("alice@bank", payment.get_details())


class TestAggregatorFactory(unittest.TestCase):
    def test_creates_stripe_aggregator(self):
        aggregator = AggregatorFactory.get_aggregator_object("stripe")
        self.assertIsInstance(aggregator, StripeAggregator)
        self.assertEqual(aggregator.name, "stripe")

    def test_creates_razorpay_aggregator(self):
        aggregator = AggregatorFactory.get_aggregator_object("razorpay")
        self.assertIsInstance(aggregator, RazorpayAggregator)
        self.assertEqual(aggregator.name, "razorpay")

    def test_invalid_aggregator_raises(self):
        with self.assertRaises(ValueError):
            AggregatorFactory.get_aggregator_object("paypal")


class TestPaymentProcessing(unittest.TestCase):
    def test_successful_payment(self):
        aggregator = AggregatorFactory.get_aggregator_object("stripe")
        result = aggregator.call_get_payment_object("card", 1500, card_number="4111111111111111")
        self.assertTrue(result)

    def test_invalid_amount_handling(self):
        aggregator = AggregatorFactory.get_aggregator_object("razorpay")
        result = aggregator.call_get_payment_object("upi", 0, upi_id="user@upi")
        self.assertFalse(result)

    def test_factory_delegation_uses_correct_gateway_factory(self):
        # A Stripe aggregator must build Stripe-specific payment classes, not Razorpay's.
        aggregator = AggregatorFactory.get_aggregator_object("stripe")
        self.assertIs(aggregator.payment_factory, StripeFactory)


if __name__ == "__main__":
    unittest.main()
