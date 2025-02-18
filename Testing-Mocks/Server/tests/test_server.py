from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


def test_sign_user_new():
    response = client.post("/registry", params={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert response.json() == {"exit_code": "200"}


def test_sign_user_existing():
    client.post("/registry", params={
        "username": "existinguser",
        "password": "testpass"
    })

    response = client.post("/registry", params={
        "username": "existinguser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert response.json() == {"already used": "200"}


def test_get_users():
    client.post("/registry", params={
        "username": "user1",
        "password": "pass1"
    })
    client.post("/registry", params={
        "username": "user2",
        "password": "pass2"
    })

    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert "user1" in users
    assert "user2" in users


def test_upload_file_user_not_found():
    response = client.post("/upload", params={
        "username": "nonexistentuser",
        "password": "nonexistentpass",
        "file_str": "some,csv,content"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_upload_file_empty_content():
    client.post("/registry", params={
        "username": "fileuser",
        "password": "filepass"
    })

    response = client.post("/upload", params={
        "username": "fileuser",
        "password": "filepass",
        "file_str": ""
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "File content is required"

@patch('main.parse_csv')
def test_get_json(mock_parse_csv):
    expected_result = {"data": "test"}
    mock_parse_csv.return_value = expected_result

    response = client.get("/json", params={"string": "test.csv"})
    assert response.status_code == 200
    assert response.json() == expected_result
    mock_parse_csv.assert_called_once_with("test.csv")

def test_get_files_all():
    client.post("/registry", params={
        "username": "filelistuser",
        "password": "filelistpass"
    })
    
    client.post("/upload", params={
        "username": "filelistuser",
        "password": "filelistpass",
        "file_str": "col1,col2\n1,2"
    })
    
    client.post("/upload", params={
        "username": "filelistuser",
        "password": "filelistpass",
        "file_str": "col3,col4\n3,4"
    })

    response = client.get("/myfiles", params={
        "username": "filelistuser",
        "password": "filelistpass"
    })
    assert response.status_code == 200
    files = response.json()
    assert isinstance(files, list)
    assert len(files) > 0

def test_get_files_user_not_found():
    response = client.get("/myfiles", params={
        "username": "nonexistentuser",
        "password": "wrongpass"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_files_wrong_password():
    client.post("/registry", params={
        "username": "passuser",
        "password": "correctpass"
    })

    response = client.get("/myfiles", params={
        "username": "passuser",
        "password": "wrongpass"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
