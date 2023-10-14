from db.models import Order, User
from db.session import SessionFactory

# Create a session
session = SessionFactory()


def get_all_orders():
    """Retrieve all orders."""
    return session.query(Order).all()


def get_order(order_id):
    """Retrieve a specific order by its ID."""
    return session.query(Order).filter(Order.id == order_id).first()


def create_order(user_id, total):
    """Create a new order for a user."""
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        return "User not found", 404

    order = Order(user_id=user_id, total=total)
    session.add(order)
    session.commit()

    return order


def update_order(order_id, total=None):
    """Update the total amount of an order by its ID."""
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        return "Order not found", 404

    if total:
        order.total = total
        session.commit()

    return order


def delete_order(order_id):
    """Delete an order by its ID."""
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        return "Order not found", 404

    session.delete(order)
    session.commit()

    return "Order deleted successfully", 200
