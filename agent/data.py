from datetime import datetime, timedelta

# Refunds are allowed up to 30 days after purchase (see calculate_right_refund).
# Dates are set relative to today so eligibility never drifts as real days pass.


def days_ago(days: int) -> str:
    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")


def item(price: int, bought_days_ago: int) -> dict:
    return {"price": price, "date": days_ago(bought_days_ago)}


users_data = {
    # One eligible item, one too old.
    "user123": {
        "book": item(23, 36),       # too old
        "pen": item(7, 25),         # eligible -> $7
    },
    # Single eligible item. Used for "user didn't name the item".
    "user124": {
        "notebook": item(12, 10),   # eligible -> $12
    },
    # Mixed result when both items are requested.
    "user125": {
        "pencil": item(3, 5),       # eligible -> $3
        "ruler": item(5, 45),       # too old
    },
    # Everything eligible.
    "user126": {
        "backpack": item(45, 3),    # eligible -> $45
        "water_bottle": item(18, 7),  # eligible -> $18
        "lunch_box": item(14, 14),  # eligible -> $14
    },
    # Only an old item. Asking for anything else -> "Item not found".
    "user127": {
        "eraser": item(2, 60),      # too old
    },
    # Edge of the 30-day window.
    "user128": {
        "stapler": item(11, 30),     # exactly 30 days -> still eligible -> $11
        "highlighter": item(4, 31),  # 31 days -> too old
    },
    # Several items. Used for "refund only the item asked for".
    "user129": {
        "calculator": item(29, 47),  # too old
        "folder": item(6, 16),       # eligible -> $6
        "usb_drive": item(16, 106),  # too old
    },
    # Single eligible item. Used for "just asking, not a refund".
    "user130": {
        "headphones": item(35, 20),  # eligible -> $35
    },
    # Two eligible items bought the same day.
    "user131": {
        "desk_lamp": item(28, 2),    # eligible -> $28
        "mouse": item(20, 2),        # eligible -> $20
    },
    # Mix of eligible and old.
    "user132": {
        "sketchbook": item(17, 27),  # eligible -> $17
        "paintbrush": item(9, 26),   # eligible -> $9
        "canvas": item(25, 103),     # too old
    },
}
