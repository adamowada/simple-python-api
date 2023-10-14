from db.session import SessionFactory
from db.models import OrderDetails, Order, Product
from http import HTTPStatus
import json


def get_order_detail(order_detail_id):
    """Retrieve details for a specific order detail item."""
    session = SessionFactory()
    order_detail = session.query(OrderDetails).filter_by(id=order_detail_id).first()
    session.close()

    if not order_detail:
        return HTTPStatus.NOT_FOUND, json.dumps({'error': 'OrderDetail not found'})

    data = {
        'id': order_detail.id,
        'order_id': order_detail.order_id,
        'product_id': order_detail.product_id,
        'quantity': order_detail.quantity,
        'sub_total': order_detail.sub_total
    }

    return HTTPStatus.OK, json.dumps(data)


def create_order_detail(order_id, product_id, quantity):
    """Create a new order detail item."""
    session = SessionFactory()

    # Check if order and product exist
    order = session.query(Order).filter_by(id=order_id).first()
    product = session.query(Product).filter_by(id=product_id).first()

    if not order or not product:
        session.close()
        return HTTPStatus.BAD_REQUEST, json.dumps({'error': 'Invalid order or product ID'})

    sub_total = product.price * quantity
    order_detail = OrderDetails(order_id=order_id, product_id=product_id, quantity=quantity, sub_total=sub_total)

    session.add(order_detail)
    session.commit()

    data = {
        'id': order_detail.id,
        'order_id': order_detail.order_id,
        'product_id': order_detail.product_id,
        'quantity': order_detail.quantity,
        'sub_total': order_detail.sub_total
    }

    session.close()

    return HTTPStatus.CREATED, json.dumps(data)


def update_order_detail(order_detail_id, quantity=None):
    """Update a specific order detail item."""
    session = SessionFactory()
    order_detail = session.query(OrderDetails).filter_by(id=order_detail_id).first()

    if not order_detail:
        session.close()
        return HTTPStatus.NOT_FOUND, json.dumps({'error': 'OrderDetail not found'})

    if quantity:
        order_detail.quantity = quantity
        product = session.query(Product).filter_by(id=order_detail.product_id).first()
        order_detail.sub_total = product.price * quantity

    session.commit()

    data = {
        'id': order_detail.id,
        'order_id': order_detail.order_id,
        'product_id': order_detail.product_id,
        'quantity': order_detail.quantity,
        'sub_total': order_detail.sub_total
    }

    session.close()

    return HTTPStatus.OK, json.dumps(data)


def delete_order_detail(order_detail_id):
    """Delete a specific order detail item."""
    session = SessionFactory()
    order_detail = session.query(OrderDetails).filter_by(id=order_detail_id).first()

    if not order_detail:
        session.close()
        return HTTPStatus.NOT_FOUND, json.dumps({'error': 'OrderDetail not found'})

    session.delete(order_detail)
    session.commit()
    session.close()

    return HTTPStatus.NO_CONTENT, json.dumps({'message': 'OrderDetail successfully deleted'})
