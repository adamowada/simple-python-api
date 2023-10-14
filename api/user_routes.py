import json
from db.models import User
from db.session import get_session


# Utility to extract JSON data from a request
def extract_request_payload(request):
    content_length = int(request.headers['Content-Length'])
    return json.loads(request.rfile.read(content_length).decode('utf-8'))


def get_user(user_id):
    """Retrieve user details based on user_id."""
    session = get_session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()

    if not user:
        return {
            'status': 'error',
            'message': f'User with ID {user_id} not found'
        }, 404

    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }
    return user_data, 200


def create_user(request):
    """Create a new user."""
    data = extract_request_payload(request)

    if not all(key in data for key in ('username', 'email', 'password')):
        return {
            'status': 'error',
            'message': 'Missing required data'
        }, 400

    user = User(username=data['username'], email=data['email'],
                password=data['password'])  # TODO: Hash password before storage for security
    session = get_session()
    session.add(user)
    session.commit()
    session.close()

    return {
        'status': 'success',
        'message': f'User {user.username} created successfully',
        'user_id': user.id
    }, 201


def update_user(user_id, request):
    """Update user details based on user_id."""
    session = get_session()
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        session.close()
        return {
            'status': 'error',
            'message': f'User with ID {user_id} not found'
        }, 404

    data = extract_request_payload(request)

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']  # TODO: Hash password before storage for security

    session.commit()
    session.close()

    return {
        'status': 'success',
        'message': f'User {user.username} updated successfully'
    }, 200


def delete_user(user_id):
    """Delete a user based on user_id."""
    session = get_session()
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        session.close()
        return {
            'status': 'error',
            'message': f'User with ID {user_id} not found'
        }, 404

    session.delete(user)
    session.commit()
    session.close()

    return {
        'status': 'success',
        'message': f'User {user.username} deleted successfully'
    }, 200
