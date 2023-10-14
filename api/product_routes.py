from db.models import Product
from db.session import SessionFactory
import json


def get_product(product_id):
    """Retrieve a product based on its ID."""
    session = SessionFactory()
    product = session.query(Product).filter(Product.id == product_id).one_or_none()

    if not product:
        return {'error': 'Product not found'}, 404

    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    session.close()
    return product_data, 200


def create_product(data):
    """Add a new product."""
    session = SessionFactory()

    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data['stock'],
        created_at=data.get('created_at')
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    product_data = {
        'id': new_product.id,
        'name': new_product.name,
        'description': new_product.description,
        'price': new_product.price,
        'stock': new_product.stock,
        'created_at': new_product.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    session.close()
    return product_data, 201


def update_product(product_id, data):
    """Update details of an existing product."""
    session = SessionFactory()
    product = session.query(Product).filter(Product.id == product_id).one_or_none()

    if not product:
        session.close()
        return {'error': 'Product not found'}, 404

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)

    session.commit()

    updated_product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    session.close()
    return updated_product_data, 200


def delete_product(product_id):
    """Delete a product by its ID."""
    session = SessionFactory()
    product = session.query(Product).filter(Product.id == product_id).one_or_none()

    if not product:
        session.close()
        return {'error': 'Product not found'}, 404

    session.delete(product)
    session.commit()

    session.close()
    return {'message': 'Product deleted successfully'}, 200
