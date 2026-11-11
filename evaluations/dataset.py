from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import ToolCall

# Expected results match agent/data.py (dates there are relative to today).


def history(username):
    return ToolCall(name="get_user_purchase_history", input_parameters={"username": username})


def check(username, item_name):
    return ToolCall(
        name="calculate_right_refund",
        input_parameters={"username": username, "item_name": item_name},
    )


def issue(username, item_name):
    return ToolCall(
        name="issue_refund_ticket",
        input_parameters={"username": username, "item_name": item_name},
    )


dataset = EvaluationDataset(
    goldens=[
        # 1. Happy path: eligible item -> ticket issued.
        Golden(
            input="I am user126, I would like a refund for the lunch_box",
            expected_output="A refund ticket for $14 has been issued for the lunch_box.",
            expected_tools=[
                history("user126"),
                check("user126", "lunch_box"),
                issue("user126", "lunch_box"),
            ],
        ),
        # 2. Happy path, different user.
        Golden(
            input="Hi, this is user123. Can I get a refund for my pen?",
            expected_output="A refund ticket for $7 has been issued for the pen.",
            expected_tools=[
                history("user123"),
                check("user123", "pen"),
                issue("user123", "pen"),
            ],
        ),
        # 3. Too old -> no ticket.
        Golden(
            input="I am user123, I would like a refund for the book",
            expected_output="The book is not eligible for a refund because it was bought more than 30 days ago.",
            expected_tools=[
                history("user123"),
                check("user123", "book"),
            ],
        ),
        # 4. Item the user never bought -> no ticket.
        Golden(
            input="I am user127, I would like a refund for the lunch_box",
            expected_output="No refund can be issued because user127 has not purchased a lunch_box.",
            expected_tools=[history("user127")],
        ),
        # 5. Unknown user -> no ticket.
        Golden(
            input="I am user999, I want a refund for my headphones",
            expected_output="No purchase history was found for user999, so no refund can be issued.",
            expected_tools=[history("user999")],
        ),
        # 6. Missing username -> agent asks for it, no tools.
        Golden(
            input="I want a refund for my pen",
            expected_output="Could you please provide your username so I can look up your purchase?",
            expected_tools=[],
        ),
        # 7. Missing item -> agent asks which item.
        Golden(
            input="I am user124, I want a refund",
            expected_output="Which item would you like a refund for?",
            expected_tools=[],
        ),
        # 8. Refund only the requested item, not the others.
        Golden(
            input="I am user129, please refund the folder",
            expected_output="A refund ticket for $6 has been issued for the folder.",
            expected_tools=[
                history("user129"),
                check("user129", "folder"),
                issue("user129", "folder"),
            ],
        ),
        # 9. Two items, mixed result.
        Golden(
            input="I am user125, I want refunds for the pencil and the ruler",
            expected_output=(
                "A refund ticket for $3 has been issued for the pencil. "
                "The ruler is not eligible because it was bought more than 30 days ago."
            ),
            expected_tools=[
                history("user125"),
                check("user125", "pencil"),
                check("user125", "ruler"),
                issue("user125", "pencil"),
            ],
        ),
        # 10. Edge of the window: exactly 30 days is still eligible.
        Golden(
            input="I am user128, I would like a refund for the stapler",
            expected_output="A refund ticket for $11 has been issued for the stapler.",
            expected_tools=[
                history("user128"),
                check("user128", "stapler"),
                issue("user128", "stapler"),
            ],
        ),
        # 11. Edge of the window: 31 days is too old.
        Golden(
            input="I am user128, I would like a refund for the highlighter",
            expected_output="The highlighter is not eligible for a refund because it was bought more than 30 days ago.",
            expected_tools=[
                history("user128"),
                check("user128", "highlighter"),
            ],
        ),
        # 12. Not a refund request -> answer the question, no ticket.
        Golden(
            input="I am user130, what have I bought from you?",
            expected_output="You purchased headphones for $35.",
            expected_tools=[history("user130")],
        ),
    ]
)
