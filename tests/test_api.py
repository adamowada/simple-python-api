import pytest
import json
from http.client import HTTPConnection
from server import SimpleHTTPRequestHandler, HTTPServer

# Assuming the use of an in-memory SQLite for these tests. We'll need a setup for that.
DATABASE_URL = "sqlite:///./test.db"


# Set up a fixture for our server
@pytest.fixture(scope='module')
def server():
    httpd = HTTPServer(('localhost', 8001), SimpleHTTPRequestHandler)
    yield httpd
    httpd.server_close()


@pytest.fixture
def client():
    conn = HTTPConnection("localhost", 8001)
    yield conn
    conn.close()


# Individual Test Functions

def test_create_user(client):
    headers = {'Content-type': 'application/json'}
    user_data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'securepassword',
    }

    client.request('POST', '/users', body=json.dumps(user_data), headers=headers)
    response = client.getresponse()

    assert response.status == 200

    response_data = json.loads(response.read().decode())
    assert 'id' in response_data
    assert response_data['username'] == 'test_user'
    assert response_data['email'] == 'test@example.com'
    # Ideally, we'd never return the password, even if it's hashed
    assert 'password' not in response_data


def test_create_product(client):
    headers = {'Content-type': 'application/json'}
    product_data = {
        'name': 'Cool T-Shirt',
        'description': 'A very cool T-shirt',
        'price': 19.99,
        'stock': 100,
    }

    client.request('POST', '/products', body=json.dumps(product_data), headers=headers)
    response = client.getresponse()

    assert response.status == 200

    response_data = json.loads(response.read().decode())
    assert 'id' in response_data
    assert response_data['name'] == 'Cool T-Shirt'


def test_update_user(client):
    headers = {'Content-type': 'application/json'}
    update_data = {
        'username': 'updated_user',
    }

    client.request('PUT', '/users/1', body=json.dumps(update_data), headers=headers)  # Assuming user with ID 1 exists
    response = client.getresponse()

    assert response.status == 200

    response_data = json.loads(response.read().decode())
    assert 'id' in response_data
    assert response_data['username'] == 'updated_user'


def test_delete_user(client):
    client.request('DELETE', '/users/1')  # Assuming user with ID 1 exists
    response = client.getresponse()

    assert response.status == 200

    response_data = json.loads(response.read().decode())
    assert response_data['message'] == "User deleted successfully"


def test_create_order(client):
    headers = {'Content-type': 'application/json'}
    order_data = {
        'user_id': 1,  # Assuming user with ID 1 exists
        'total': 19.99
    }

    client.request('POST', '/orders', body=json.dumps(order_data), headers=headers)
    response = client.getresponse()

    assert response.status == 200

    response_data = json.loads(response.read().decode())
    assert 'id' in response_data


def test_order_details(client):
    headers = {'Content-type': 'application/json'}
    order_detail_data = {
        'order_id': 1,  # Assuming order with ID 1 exists
        'product_id': 1,  # Assuming product with ID 1 exists
        'quantity': 2,
        'sub_total': 39.98
    }

    client.request('POST', '/orderdetails', body=json.dumps(order_detail_data), headers=headers)
    response = client.getresponse()

    assert response.status == 200

    response_data = json.loads(response.read().decode())
    assert 'id' in response_data


# Functional Test: Creating a user, product, order, and checking order details.
def test_functional_workflow(client):
    # Create User
    user_data = {
        'username': 'functional_test_user',
        'email': 'functionaltest@example.com',
        'password': 'securepassword',
    }

    client.request('POST', '/users', body=json.dumps(user_data), headers={'Content-type': 'application/json'})
    user_response = json.loads(client.getresponse().read().decode())

    # Create Product
    product_data = {
        'name': 'Functional Test T-Shirt',
        'description': 'A T-shirt for functional tests',
        'price': 19.99,
        'stock': 100,
    }

    client.request('POST', '/products', body=json.dumps(product_data), headers={'Content-type': 'application/json'})
    product_response = json.loads(client.getresponse().read().decode())

    # Create Order
    order_data = {
        'user_id': user_response['id'],
        'total': product_response['price']
    }

    client.request('POST', '/orders', body=json.dumps(order_data), headers={'Content-type': 'application/json'})
    order_response = json.loads(client.getresponse().read().decode())

    # Check Order Details
    order_detail_data = {
        'order_id': order_response['id'],
        'product_id': product_response['id'],
        'quantity': 1,
        'sub_total': product_response['price']
    }

    client.request('POST', '/orderdetails', body=json.dumps(order_detail_data),
                   headers={'Content-type': 'application/json'})
    order_details_response = json.loads(client.getresponse().read().decode())

    assert 'id' in order_details_response
    assert order_details_response['quantity'] == 1
