from langchain.tools import tool
from data import users_data

from dotenv import load_dotenv
import logging

from objects import PurchaseItem
from datetime import datetime

load_dotenv()  # Load environment variables from .env file

@tool
def get_user_purchase_history(username: str) -> dict:
    """
    Get the purchase history of a user.
    """
    logging.info(f"Fetching purchase history for user: {username}")
    if users_data.get(username) :
        return users_data[username]
    
        logging.warning(f"No purchase history found for user: {username}")
    return users_data.get(username, {})

@tool
def calculate_right_refund(username: str, item_name: str) -> str:
    """
    Calculate the refund amount for a specific item purchased by a user.
    """
    logging.info(f"Calculating refund for user: {username}, item: {item_name}")
    user_history = users_data.get(username)
    if not user_history:
        logging.warning(f"No purchase history found for user: {username}")
        return "User not found"

    item = user_history.get(item_name)
    if not item:
        logging.warning(f"Item '{item_name}' not found in purchase history for user: {username}")
        return "Item not found"

    purchase_date = datetime.strptime(item["date"], "%Y-%m-%d")
    current_date = datetime.now()
    days_since_purchase = (current_date - purchase_date).days

    if days_since_purchase > 30:
        logging.info(f"Refund not eligible for item '{item_name}' purchased on {item['date']}. Days since purchase: {days_since_purchase}")
        return "Refund not eligible due to time limit"

    logging.info(f"Refund eligible for item '{item_name}'. Refund amount: {item['price']}")
    return f"Refund eligible. Amount: ${item['price']}"


@tool
def issue_refund_ticket(username: str, item_name: str) -> str:
    """
    Issue a refund ticket for a specific item purchased by a user.
    """
    logging.info(f"Issuing refund ticket for user: {username}, item: {item_name}")
    user_history = users_data.get(username)
    if not user_history:
        logging.warning(f"No purchase history found for user: {username}")
        return "User not found"

    item = user_history.get(item_name)
    if not item:
        logging.warning(f"Item '{item_name}' not found in purchase history for user: {username}")
        return "Item not found"

    # Here you would implement the logic to issue a refund ticket.
    # For this example, we'll just return a success message.
    logging.info(f"Refund ticket issued for item '{item_name}' purchased by user '{username}'.")
    return f"Refund ticket issued for item '{item_name}' purchased by user '{username}'."


@tool
def check_current_date() -> str:
    """
    Check the current date.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    logging.info(f"Current date is: {current_date}")
    return current_date


@tool
def check_item_eligibility(username: str, item_name: str) -> str:
    """
    Check if a specific item purchased by a user is eligible for a refund.
    """
    logging.info(f"Checking refund eligibility for user: {username}, item: {item_name}")
    user_history = users_data.get(username)
    if not user_history:
        logging.warning(f"No purchase history found for user: {username}")
        return "User not found"

    item = user_history.get(item_name)
    if not item:
        logging.warning(f"Item '{item_name}' not found in purchase history for user: {username}")
        return "Item not found"

    purchase_date = datetime.strptime(item["date"], "%Y-%m-%d")
    current_date = datetime.now()
    days_since_purchase = (current_date - purchase_date).days

    if days_since_purchase > 30:
        logging.info(f"Refund not eligible for item '{item_name}' purchased on {item['date']}. Days since purchase: {days_since_purchase}")
        return "Refund not eligible due to time limit"

    logging.info(f"Refund eligible for item '{item_name}'.")
    return "Refund eligible"

@tool
def get_purchase_item(username: str, item_name: str) -> PurchaseItem:
    """
    Get the purchase item details for a specific item purchased by a user.
    """
    logging.info(f"Fetching purchase item details for user: {username}, item: {item_name}")
    user_history = users_data.get(username)
    if not user_history:
        logging.warning(f"No purchase history found for user: {username}")
        return None

    item = user_history.get(item_name)
    if not item:
        logging.warning(f"Item '{item_name}' not found in purchase history for user: {username}")
        return None

    purchase_item = PurchaseItem(name=item_name, price=item["price"], date=item["date"])
    logging.info(f"Purchase item details fetched: {purchase_item}")
    return purchase_item


book=PurchaseItem(name="notebook", price=15.99, date="2023-10-01")
pen=PurchaseItem(name="pen", price=2.99, date="2026-10-26")
# print(calculate_right_refund.invoke({"username": "user123", "items":[book,pen]})) 
print(calculate_right_refund.invoke({"username": "user123", "item_name": "pen"})) # Example usage
print(calculate_right_refund.invoke({"username": "user129", "item_name": "folder"}))
