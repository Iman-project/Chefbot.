# agent.py

# This is your main AI logic for CHEFBOT

# Example in-memory database for demonstration
restaurants = {
    "TOKEN1": {
        "name": "Bella Pizza",
        "menu": {
            "Monday": ["Pepperoni Pizza", "Veggie Pizza"],
            "Tuesday": ["Margherita Pizza", "BBQ Chicken Pizza"]
        }
    },
    "TOKEN2": {
        "name": "Nigerian Bites",
        "menu": {
            "Monday": ["Jollof Rice", "Fried Plantain"],
            "Tuesday": ["Egusi Soup", "Pounded Yam"]
        }
    }
}

# Store orders
orders = {}

# ----------------------------
def handle_message(phone_number, text, restaurant_token="default"):
    """
    Main function to process incoming WhatsApp messages.
    Returns a string reply to send back to the user.
    """

    restaurant = restaurants.get(restaurant_token)
    if not restaurant:
        return "Sorry, restaurant not recognized."

    text_lower = text.lower()

    # 1. Greetings
    if "hi" in text_lower or "hello" in text_lower:
        return f"Hello! Welcome to {restaurant['name']}. Send 'menu' to see today's menu."

    # 2. Show menu
    if "menu" in text_lower:
        from datetime import datetime
        day = datetime.today().strftime("%A")  # Get current day
        today_menu = restaurant["menu"].get(day)
        if not today_menu:
            return f"Sorry, {restaurant['name']} has no menu today."
        menu_text = f"Today's menu at {restaurant['name']}:\n"
        for idx, item in enumerate(today_menu, 1):
            menu_text += f"{idx}. {item}\n"
        menu_text += "Reply with 'order <number>' to place an order."
        return menu_text

    # 3. Place order
    if text_lower.startswith("order"):
        try:
            order_number = int(text_lower.split()[1])
        except:
            return "Please reply with 'order <number>' using the menu number."

        from datetime import datetime
        day = datetime.today().strftime("%A")
        today_menu = restaurant["menu"].get(day)
        if not today_menu or order_number < 1 or order_number > len(today_menu):
            return "Invalid order number. Please check the menu."
        
        order_item = today_menu[order_number - 1]
        order_code = f"{phone_number[-4:]}{len(orders)+1}"  # simple unique code
        orders[order_code] = {
            "phone": phone_number,
            "restaurant": restaurant["name"],
            "item": order_item,
            "status": "Received"
        }
        return f"Thank you! Your order for '{order_item}' has been received. Your order code is {order_code}."

    # 4. Check order status
    if text_lower.startswith("status"):
        try:
            order_code = text_lower.split()[1]
        except:
            return "Please reply with 'status <order_code>' to check your order."

        order = orders.get(order_code)
        if not order:
            return "Order not found."
        return f"Your order '{order['item']}' at {order['restaurant']} is currently: {order['status']}."

    # 5. Default reply
    return "Sorry, I did not understand. You can say 'hi', 'menu', 'order <number>', or 'status <order_code>'."
