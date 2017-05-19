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
        "id": 175113727,
        "first_name": "FirstName",
        "last_name": "LastName",
        "username": "UserName"
        }


@pytest.fixture()
def test_chat():
    return {
        "id": 175113727,
        "first_name": "Julia",
        "last_name": "K",
        "username": "JulikSp",
        "type": "private"
        }


@pytest.fixture()
def fake_entities():
    return [{
        "type": "bot_command",
        "offset": 0,
        "length": 5
        }]


@pytest.fixture()
def fake_command_message():
    return {
        "message_id": 1486,
        "from": fake_user(),
        "chat": test_chat(),
        "date": 1494875753,
        "text": '/help',
        "entities": fake_entities()
        }


@pytest.fixture()
def fake_result_message():
    return {
        "update_id": 547461412,
        "message": fake_command_message()
        }


@pytest.fixture(params=get_commands())
def fake_commands_message(request):
    return [{
        "update_id": 547461412,
        "message": {
            "message_id": 1486,
            "from": fake_user(),
            "chat": test_chat(),
            "date": 1494875753,
            "text": request.param,
            "entities": fake_entities()
            }
        }]


@pytest.fixture()
def fake_updates():
    return {
        "ok": "true",
        "result": [fake_result_message()]
    }


@pytest.fixture()
def fake_command_updates():
    return {
        "ok": "true",
        "result": fake_commands_message()
    }


@pytest.fixture()
def fake_empty_updates():
    return {
        "ok": "true",
        "result": []
    }
