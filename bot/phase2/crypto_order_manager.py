import logging
from core.order_manager import OrderManager

logger = logging.getLogger("polyfarm.crypto_orders")


class CryptoOrderManager(OrderManager):
    """
    Reuses Phase 1 OrderManager class.
    Same entry, exit, and trigger logic.
    Same wallet, floor, and tier protection.
    Capital split: max 60% each phase when
    both phases are active.
    """

    def __init__(self, client, wallet, alerts,
                 position_monitor):
        super().__init__(
            client, wallet, alerts,
            position_monitor
        )
        self.max_phase_allocation = 0.60

    def _get_phase_budget(self) -> float:
        """
        Returns max capital for Phase 2.
        When both phases active: 60% each
        (total can exceed 100% via overlap).
        """
        total = self.wallet.state.live_portfolio_value
        return total * self.max_phase_allocation
