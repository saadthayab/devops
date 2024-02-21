import pytest
from app import app, db, Myapp


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def test_home_redirect(client):
    """Test that the home page redirects to /base."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/base' in response.location


def test_insert(client):
    """Test inserting a new item and redirecting to /base."""
    response = client.post('/insert', data={'c_name': 'Test Task'}, follow_redirects=True)
    print('saad')
    assert response.status_code == 200
    assert b'Test Task' in response.data


# def test_delete(client):
#     """Test deleting an item."""
#     # First, insert a new item
#     new_item = Myapp(c_name="Task to Delete")
#     db.session.add(new_item)
#     db.session.commit()
#
#     # Then, delete the item
#     response = client.get(f'/delete/{new_item.c_id}', follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Task to Delete' not in response.data


def test_base_route(client):
    """Test that the /base route can be accessed and displays correctly."""
    response = client.get('/base')
    assert response.status_code == 200
    assert b'My Daily Checklist' in response.data


# def test_model(client):
#     """Test the Myapp model by adding an item directly and querying it."""
#     new_item = Myapp(c_name="Direct Model Test")
#     db.session.add(new_item)
#     db.session.commit()
#
#     queried_item = Myapp.query.first()
#     assert queried_item.c_name == "Direct Model Test"


# def test_base_page_contents(client):
#     """Test that the base page contains specific elements and text."""
#     # Add a sample task to display
#     new_item = Myapp(c_name="Sample Task for Page")
#     db.session.add(new_item)
#     db.session.commit()
#
#     response = client.get('/base')
#     assert b'My Daily Checklist' in response.data
#     assert b'<form action="/insert" method="post">' in response.data
#     assert b'Sample Task for Page' in response.data


def test_delete_nonexistent_item(client):
    """Test deleting a non-existent item and ensure graceful handling."""
    response = client.get('/delete/999', follow_redirects=True)  # Assuming ID 999 does not exist
    assert response.status_code == 404  # or 200 if you handle it gracefully within your app


def test_insert_empty_name(client):
    """Test inserting an item with no name and ensure it's handled."""
    response = client.post('/insert', data={'c_name': ''}, follow_redirects=True)
    assert response.status_code == 200
    # Depending on how your application is supposed to handle this, check for an error message or verify no new task was added
