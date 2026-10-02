
from typing import Dict, Type

from aggregators import Aggregator, RazorpayAggregator, StripeAggregator


class AggregatorFactory:
    factory: Dict[str, Type[Aggregator]] = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator,
    }

    @classmethod
    def get_aggregator_object(cls, aggregator_name: str) -> Aggregator:
        aggregator_class = cls.factory.get(aggregator_name)
        if aggregator_class is None:
            supported = ", ".join(sorted(cls.factory)) or "none"
            raise ValueError(
                f"Unsupported aggregator '{aggregator_name}'. Supported: {supported}"
            )
        return aggregator_class()
