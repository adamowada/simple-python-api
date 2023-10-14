import pytest
import json
from http.client import HTTPConnection
from server import SimpleHTTPRequestHandler, HTTPServer
from db.base import Base, engine
from db.session import SessionFactory
import threading

# Global variable for the server thread
server_thread = None

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///./test.db"  # Change this in `server.py` when running tests or use "sqlite://"


def setup_module():
    """Start the server before tests."""
    # Create tables
    Base.metadata.create_all(engine)

    global server_thread
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()


def teardown_module():
    """Stop the server after tests."""
    global server_thread
    if server_thread:
        server_thread.join(timeout=1)

    # Drop tables
    Base.metadata.drop_all(engine)


# Set up a fixture for our server
@pytest.fixture
def server():
    httpd = HTTPServer(('localhost', 8001), SimpleHTTPRequestHandler)
    yield httpd
    httpd.server_close()


@pytest.fixture
def client():
    conn = HTTPConnection("localhost", 8001)
    yield conn
    conn.close()


@pytest.fixture(autouse=True)  # autouse ensures that it's used automatically without explicit invocation
def handle_sessions():
    SessionFactory.begin_nested()  # start a transaction
    yield
    SessionFactory.rollback()  # rollback the transaction after test
    SessionFactory.close()  # close the session


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


@pytest.mark.skip
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


@pytest.mark.skip
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


@pytest.mark.skip
def test_delete_user(client):
    client.request('DELETE', '/users/1')  # Assuming user with ID 1 exists
    response = client.getresponse()

    assert response.status == 200

    response_data = json.loads(response.read().decode())
    assert response_data['message'] == "User deleted successfully"


@pytest.mark.skip
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


@pytest.mark.skip
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
@pytest.mark.skip
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
