from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import requests
import questionary
from CLI.CLI import CLI_client 


def test_cli_sign_in(mocker):
    """
        test register
    """
    usr="test_user"
    pwd= "some_pwd"
    cli = CLI_client()
    mocker.patch.object(questionary, "select") 
    questionary.select.return_value.ask.return_value = "sign in"
    mocker.patch.object(questionary, "text")
    questionary.text.return_value.ask.return_value = usr
    mocker.patch.object(questionary, "password")
    questionary.password.return_value.ask.return_value =pwd
    mock_post = mocker.patch("requests.post")
    mocker.patch.object(cli, "start")
    cli.start()
    testing_url = "http://localhost:8000/registry"
    testing_json = {"username": usr, "password": pwd}
    mock_post.assert_called_once_with(testing_url, json=testing_json)
    cli.start.assert_called_once()


def test_get_users_list(mocker, capsys):
    """
    test get users
    """
    cli = CLI_client()
    mocker.patch.object(questionary, "select")
    questionary.select.return_value.ask.return_value = "get users list"
    mock_response = MagicMock()
    mock_response.json.return_value = ["user1", "user2"]
    mocker.patch("requests.get", return_value=mock_response)
    mocker.patch.object(cli, "start")
    cli.start()
    CLI_output = capsys.readouterr()
    assert "user1" in CLI_output.out
    assert "user2" in CLI_output.out
    requests.get.assert_called_once_with("http://127.0.0.1:8000/users")


