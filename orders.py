# orders.py
from database import SessionLocal, Order, Customer
import datetime

# -----------------------------
# Simulated WhatsApp notification
# -----------------------------
def notify_customer(phone, message):
    """
    Simulates sending a WhatsApp message.
    Replace with real API later.
    """
    print(f"[WHATSAPP] To {phone}: {message}")


# -----------------------------
# Create a new order
# -----------------------------
def create_order(restaurant_id, customer_id, items, total_amount):
    """
    Creates a new order and returns the order reference.
    """
    session = SessionLocal()
    order_ref = f"CB-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    order = Order(
        restaurant_id=restaurant_id,
        customer_id=customer_id,
        order_ref=order_ref,
        items=items,
        total_amount=total_amount,
        status="pending"
    )
    session.add(order)
    session.commit()
    session.close()
    return order_ref


# -----------------------------
# Update order status
# -----------------------------
def update_order_status(order_ref, status):
    """
    Updates order status and notifies the customer.
    status: "packed", "sent", "delivered"
    """
    session = SessionLocal()
    order = session.query(Order).filter(Order.order_ref == order_ref).first()
    if not order:
        session.close()
        return False, "Order not found"

    order.status = status
    session.commit()

    # Notify customer
    customer = session.query(Customer).filter(Customer.id == order.customer_id).first()
    if customer:
        msg = f"Your order {order_ref} status: {status.upper()}"
        notify_customer(customer.phone, msg)

    session.close()
    return True, f"Order {order_ref} updated to {status}"
