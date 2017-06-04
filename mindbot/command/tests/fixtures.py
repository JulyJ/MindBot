import pytest
from time import gmtime, strftime

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


@pytest.fixture()
def fake_xkcd():
    return {
        "num": 1839,
        "safe_title": "Doctor Visit",
        "alt": "According to these blood tests, you're like 30% cereal.",
        "img": "https://imgs.xkcd.com/comics/doctor_visit.png",
    }


@pytest.fixture()
def fake_urban():
    return {
        "list": [{
            "definition": "Heroin.",
            "permalink": "http://horse.urbanup.com/183954",
            "thumbs_up": 1764,
            "thumbs_down": 693
        }]}


@pytest.fixture()
def fake_empty_urban():
    return {
        "list": []}


@pytest.fixture()
def fake_hknews_list():
    return [14386413]


@pytest.fixture()
def fake_hknews_item():
    return {
        "score": 2,
        "title": "Ask HN: How to find audience for FOSS project?",
        "url": "http://some.url.com"
    }


@pytest.fixture()
def fake_exchange():
    return {
        "base": "CAD",
        "rates": {
            "EUR": 0.65924
        }
    }


@pytest.fixture()
def fake_dict():
    return {
        "results": [{
            "id": "string",
            "language": "string",
            "lexicalEntries": [{
                "entries": [{
                    "senses": [{
                        "definitions": ["definition"]
                        }]
                    }]
                }]
            }]
        }


@pytest.fixture()
def fake_empty_results():
    return {
        "results": []
        }


@pytest.fixture()
def fake_empty_lexical_entries():
    return {
        "results": [{
            "id": "string",
            "language": "string",
            "lexicalEntries": []
                }]
        }


@pytest.fixture()
def fake_empty_entries():
    return {
        "results": [{
            "id": "string",
            "language": "string",
            "lexicalEntries": [{
                "entries": []
                }]
            }]
        }


@pytest.fixture()
def fake_empty_senses():
    return {
        "results": [{
            "id": "string",
            "language": "string",
            "lexicalEntries": [{
                "entries": [{
                    "senses": []
                    }]
                }]
            }]
        }


@pytest.fixture()
def fake_ocr_response():
    return {
        "ParsedResults": [
                {
                    "FileParseExitCode": 1,
                    "ParsedText": "This is a sample parsed result",
                    "ErrorMessage": "null",
                    "ErrorDetails": "null"
                }
            ],
        "OCRExitCode": 1,
        "ErrorMessage": "null",
        "ErrorDetails": "null"
    }


@pytest.fixture()
def fake_ocr_error_response():
    return {
        "ParsedResults": [
                {
                    "FileParseExitCode": 1,
                    "ParsedText": "This is a sample parsed result",
                    "ErrorMessage": "null",
                    "ErrorDetails": "null"
                }
            ],
        "OCRExitCode": 2,
        "ErrorMessage": "null",
        "ErrorDetails": "null"
    }


@pytest.fixture()
def fake_apod_message():
    return {
          "copyright": "ESA",
          "date": "2017-05-28",
          "explanation": "What's happened in Hebes Chasma on Mars?",
          "title": "Collapse in Hebes Chasma on Mars",
          "url": "https://apod.nasa.gov/apod/image/1705/HebesChasma_esa_960.jpg"
        }


@pytest.fixture()
def fake_canadanews_article():
    return {
                "date": "May 29, 2017",
                "photo": "/dai-quo/ssi/homepage/release_photo/946.jpg",
                "title": "Study: Women in Canada: Women with Disabilities",
                "summary": "Over 2 million women aged 15 or older.",
                "link": "/daily-quotidien/170529/dq170529a-eng.htm"
            }


@pytest.fixture()
def fake_canadanews():
    return {
        "daily": {
            "article": [
                fake_canadanews_article()
            ]
        }
    }


@pytest.fixture()
def fake_asteroid_message():
    return {
        "near_earth_objects": {
            strftime("%Y-%m-%d", gmtime()): [{
                'name': 'test',
                'nasa_jpl_url': 'http://test.url',
                'absolute_magnitude_h': 1234.43,
                'estimated_diameter': {
                    'kilometers': {
                        'estimated_diameter_min': 12,
                        'estimated_diameter_max': 24
                    }
                },
                'is_potentially_hazardous_asteroid': True
            }]
        }
    }


@pytest.fixture()
def fake_curiosity_message():
    return {
        'photos': [{
            'earth_date': '2017-04-05',
            'img_src': 'http://test.src',
            'camera': {
                'full_name': 'camera'
            }
        }]
    }
