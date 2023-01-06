import pytest
from . import create_app
from User import User

# ----------------------------------- 
# SETUP
# ----------------------------------- 

@pytest.fixture()
def app():
    app = create_app()

    app.config.update({
        "TESTING": True,
        "LOGIN_DISABLED": True
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def user():
    return User("user")



# ----------------------------------- 
# TESTS
# -----------------------------------


# routing
def test_default_route(client):
    res = client.get("/", follow_redirects=True)
    assert res.request.path == "/login"

def test_login_route(client):
    res = client.get("/login")
    assert res.request.path == "/login"

def test_logout_route(client):
    res = client.get("/logout", follow_redirects=True)
    assert res.request.path == "/login"

def test_home_route(client):
    with client.session_transaction() as s:
        s["curr_user"] = "admin"
    res = client.get("/home")
    assert res.request.path == "/home"

def test_json_route(client):
    with client.session_transaction() as s:
        s["curr_user"] = "admin"
    res = client.get("/json")
    assert res.request.path == "/json"

# tasks 
def test_add_task(client):
    # user not logged in
    with pytest.raises(Exception) as e:
        client.get("/addTask")

def test_remove_task(client):
    # user not logged in
    with pytest.raises(Exception) as e:
        client.get("/removeTask")

def test_update_task(client):
    # user not logged in
    with pytest.raises(Exception) as e:
        client.get("/updateTask")

# user
def test_user(user):
    assert user.is_authenticated == False
    assert user.get_id() == "user"