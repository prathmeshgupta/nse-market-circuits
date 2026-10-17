from typing import Optional, Dict, Any

class CircuitAnalyzer:
    """Evaluates whether trade orders would be realistically filled or locked by circuits."""

    @staticmethod
    def evaluate_feasibility(
        open_p: float,
        high_p: float,
        low_p: float,
        close_p: float,
        upper_circuit: Optional[float] = None,
        lower_circuit: Optional[float] = None
    ) -> Dict[str, Any]:
        is_uc_hit = 0
        is_lc_hit = 0
        can_buy = True
        can_sell = True

        if upper_circuit and high_p >= upper_circuit and low_p >= upper_circuit:
            is_uc_hit = 1
            can_buy = False  # Locked at Upper Circuit: buy orders cannot fill

        if lower_circuit and low_p <= lower_circuit and high_p <= lower_circuit:
            is_lc_hit = 1
            can_sell = False  # Locked at Lower Circuit: sell orders cannot fill

        return {
            "is_upper_circuit_hit": is_uc_hit,
            "is_lower_circuit_hit": is_lc_hit,
            "can_buy": can_buy,
            "can_sell": can_sell,
            "is_executable": can_buy and can_sell
        }
