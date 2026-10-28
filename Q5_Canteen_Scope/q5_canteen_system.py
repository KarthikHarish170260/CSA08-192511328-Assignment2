"""
Task 05: Functions, Parameters and Scope - College Canteen Order System
Course: CSA08 / CSA0807 Python Programming (CO2)
Bloom's Level: K4 - Analyse

Principle: "A default value is created once, when the function is defined - not each time the function is called."
"""

# ==============================================================================
# Complete the Code: Buggy vs Corrected Functions
# ==============================================================================
def add_item_buggy(item: str, order: list = []):
    """Buggy implementation: Uses mutable default parameter []."""
    order.append(item)
    return order


def add_item(item: str, order: list = None) -> list:
    """
    TODO 1: Corrected implementation using sentinel default None.
    A fresh list is instantiated at runtime if order is None.
    """
    if order is None:
        order = []
    order.append(item)
    return order


# ==============================================================================
# Parameter Types Demonstration: Positional, Keyword, Default, Keyword-Only
# ==============================================================================
# Price lookup for canteen items
MENU = {
    "Tea": 15.0,
    "Coffee": 20.0,
    "Vada": 25.0,
    "Masala Dosa": 60.0,
    "Idli": 30.0,
    "Upma": 35.0,
}


def calculate_bill(
    order: list[str],
    discount_pct: float = 0.0,  # Default parameter
    *,
    gst_rate: float = 0.05,  # Keyword-only parameter (preceded by *)
) -> tuple[float, float, float]:
    """
    Demonstrates:
    1. Positional parameter: order
    2. Default parameter: discount_pct
    3. Keyword-only parameter: gst_rate (enforced by *)
    4. Multiple return values: (subtotal, gst, final_total) returned as a tuple.
    """
    subtotal = sum(MENU.get(item, 0.0) for item in order)
    discount_amount = subtotal * (discount_pct / 100.0)
    taxable_amount = subtotal - discount_amount
    gst_amount = taxable_amount * gst_rate
    final_total = taxable_amount + gst_amount

    # Returns 3 values as an immutable tuple
    return subtotal, gst_amount, final_total


# ==============================================================================
# Scope Demonstrations: Local vs Global vs Nonlocal
# ==============================================================================
# Global scope variable
canteen_daily_revenue = 0.0  # Shared across all module functions


def record_transaction_global(amount: float) -> None:
    """
    Demonstrates 'global' keyword.
    Why required: Without 'global', assigning to canteen_daily_revenue creates
    a local variable or raises UnboundLocalError.
    Why avoided: Introduces hidden state, violates encapsulation, and causes race conditions.
    """
    global canteen_daily_revenue
    canteen_daily_revenue += amount


def make_canteen_session(customer_name: str):
    """
    Demonstrates 'nonlocal' scope inside a Closure.
    Alternative Concept: Order kept inside closure state instead of default parameter.
    """
    customer_order: list[str] = []  # Enclosing (nonlocal) variable

    def order_item(item: str) -> list[str]:
        nonlocal customer_order  # Binds to the enclosing customer_order list
        customer_order.append(item)
        return list(customer_order)  # Returns copy to prevent external mutation

    return order_item


# ==============================================================================
# Test Suite and Evidence Generation
# ==============================================================================
def run_canteen_tests():
    print("=" * 85)
    print("TASK 05: COLLEGE CANTEEN ORDER SYSTEM - FUNCTIONS & SCOPE")
    print("=" * 85)

    # 1. Official assignment verification
    print("\n[Official Assignment Execution Check]:")
    print("Buggy Output :", add_item_buggy("Tea"), add_item_buggy("Vada"))
    print("Correct Output:", add_item("Tea"), add_item("Vada"))

    print("\n[Inspecting __defaults__ Attribute]:")
    print("add_item_buggy.__defaults__ :", add_item_buggy.__defaults__)
    print("add_item.__defaults__       :", add_item.__defaults__)
    print("-> Explanation: add_item_buggy.__defaults__ references the mutated list object in memory,")
    print("   carrying forward items to all future callers who omit the 'order' argument.")

    # 2. Sequential 3-Customer Isolation Test
    print("\n" + "=" * 85)
    print("TESTING 3 CUSTOMERS IN SEQUENCE (INDEPENDENT ORDERS)")
    print("=" * 85)

    # Customer 1
    c1_order = add_item("Masala Dosa")
    c1_order = add_item("Tea", c1_order)
    sub1, gst1, tot1 = calculate_bill(c1_order, discount_pct=5.0, gst_rate=0.05)
    record_transaction_global(tot1)

    # Customer 2 (Should NOT have Masala Dosa or Tea!)
    c2_order = add_item("Idli")
    c2_order = add_item("Vada", c2_order)
    c2_order = add_item("Coffee", c2_order)
    sub2, gst2, tot2 = calculate_bill(c2_order, discount_pct=0.0, gst_rate=0.05)
    record_transaction_global(tot2)

    # Customer 3 (Starts fresh)
    c3_order = add_item("Upma")
    sub3, gst3, tot3 = calculate_bill(c3_order)
    record_transaction_global(tot3)

    print(f"Customer 1 Order: {str(c1_order):<25} | Subtotal: Rs {sub1:6.2f} | GST: Rs {gst1:5.2f} | Total: Rs {tot1:6.2f}")
    print(f"Customer 2 Order: {str(c2_order):<25} | Subtotal: Rs {sub2:6.2f} | GST: Rs {gst2:5.2f} | Total: Rs {tot2:6.2f}")
    print(f"Customer 3 Order: {str(c3_order):<25} | Subtotal: Rs {sub3:6.2f} | GST: Rs {gst3:5.2f} | Total: Rs {tot3:6.2f}")
    print(f">> Accumulated Global Daily Revenue: Rs {canteen_daily_revenue:.2f}")

    # 3. Closure-based Alternative Execution
    print("\n" + "=" * 85)
    print("ALTERNATIVE CONCEPT: CLOSURE-BASED ORDER STATE (NONLOCAL)")
    print("=" * 85)
    session_anand = make_canteen_session("Anand")
    session_priya = make_canteen_session("Priya")

    print("Anand adds Tea   :", session_anand("Tea"))
    print("Priya adds Vada  :", session_priya("Vada"))
    print("Anand adds Samosa:", session_anand("Masala Dosa"))
    print("Priya's order remains isolated:", session_priya("Coffee"))


if __name__ == "__main__":
    run_canteen_tests()
