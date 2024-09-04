import json


def test_registration(test_app_with_db):
    # Given
    dummy_data = json.dumps({
        "email": "example3@example.com",
        "password_hash": "example_password_312"
    })
    # When

    response = test_app_with_db.post("/auth/users", data=dummy_data)
    # then
    dummy_id = response.json()['id']
    assert response.status_code == 200
    assert response.json()['email'] == 'example3@example.com'
    test_app_with_db.delete(f"/auth/users/{dummy_id}")
    # assert

def test_all_users(test_app_with_db):
    # given
    # when
    response = test_app_with_db.get("/auth/users/")
    # then
    assert response.status_code == 200
    # assert response.json()[0]['id'] == 1

def test_delete_user(test_app_with_db):
    # given 
    dummy_id = test_app_with_db.get("/auth/users/").json()[0]['id']
    # when
    response = test_app_with_db.delete(f"/auth/users/{dummy_id}")
    #then
    print(response)
    assert response.status_code == 200


def test_ununique_registration(test_app_with_db):
    # Given
    dummy_data = json.dumps({
        "email": "example@example.com",
        "password_hash": "example_password_2"
    })
    # When

    response = test_app_with_db.post("/auth/users", data=dummy_data)
    response = test_app_with_db.post("/auth/users", data=dummy_data)
    # then
    assert response.status_code == 422
    # assert response.json()['id'] == 1
    # assert response.json()['email'] == 'example@example.com'
    # assert 

def test_get_user_id(test_app_with_db):
    # Given
    dummy_id = test_app_with_db.get("/auth/users/").json()[0]['id']
    # When

    response = test_app_with_db.get(f"/auth/users/{dummy_id}")
    # then
    assert response.status_code == 200
    assert response.json()['id'] == dummy_id
    # assert

def test_update_user(test_app_with_db):
    # given
    dummy_user = test_app_with_db.get("/auth/users/").json()[0]
    dummy_id = dummy_user['id']
    del dummy_user['id'] # no id in class
    # when
    dummy_user["email"] = 'newemail@example.com'
    print(type(dummy_user))
    response = test_app_with_db.put(
        f"/auth/users/{dummy_id}",
        json=dummy_user
    )
    assert response.status_code == 200