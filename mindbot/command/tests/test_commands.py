import pytest

from mindbot.router import CommandRouter


def get_commands():
    commands_list = []
    for command in CommandRouter.get_commands_help():
        commands_list.append(command[0])
    return commands_list


@pytest.fixture()
def fake_user():
    return {
        "id": 123,
        "first_name": "FirstName",
        "last_name": "LastName",
        "username": "UserName"
        }


@pytest.fixture()
def fake_chat():
    return {
        "id": 123,
        "first_name": "FirstName",
        "last_name": "LastName",
        "username": "UserName",
        "type": "private"
        }


@pytest.fixture()
def fake_entities():
    return [{
        "type": "bot_command",
        "offset": 0,
        "length": 5
        }]


@pytest.fixture(params=get_commands())
def fake_empty_command_message(request):
    return {
        "message_id": 1486,
        "from": fake_user(),
        "chat": fake_chat(),
        "date": 1494692389,
        "text": request.param,
        "entities": fake_entities()
        }


@pytest.fixture(params=get_commands())
def fake_text_command_message(request):
    return {
        "message_id": 1486,
        "from": fake_user(),
        "chat": fake_chat(),
        "date": 1494692389,
        "text": request.param+" horse",
        "entities": fake_entities()
        }


def test_empty_commands(fake_empty_command_message):
    CommandRouter.route(fake_empty_command_message)


def test_text_commands(fake_text_command_message):
    CommandRouter.route(fake_text_command_message)
