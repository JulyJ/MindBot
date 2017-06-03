## MindBot

This repo contains source code for Telegram @MindDumpBot.

For beginning you can install bot with pip manager:

```
$ git clone https://github.com/JulyJ/MindBot
$ pip install -e .
```

You must add environment variables:

Short sample *.env* file

```
# http://openweathermap.org/appid
WEATHER_TOKEN="<TOKEN>"
# https://core.telegram.org/bots
TELEGRAM_TOKEN="<TOKEN>"
# https://developer.oxforddictionaries.com/
DICTIONARY_APP_ID="<APP_ID>"
DICTIONARY_APP_KEY="<APP_KEY>"
# https://ocr.space/ocrapi
OCR_API_KEY="<API_KEY>"
```

To run bot you need just type to console

```
mindbot
```

Available bot commands:
- `/apod` -  Each day a different image or photograph of our fascinating universe.
- `/asteroid` -  Retrieve a list of 5 Asteroids based on today closest approach to Earth.
- `/bestnews`  - Get N best Hacker News stories.
- `/curiosity` - N Random photos from Curiosity rover
- `/exchange`  - Money exchange.
- `/forecast`  - Show 3 days weather forecast for the specified location.
- `/google` - Trying to perform "feeling lucky" google search.
- `/latestnews` - Get N latest Hacker News stories.
- `/ocr`  - Parse text from an image.
- `/oxford`  - Look for definitions in Oxford Dictionary.
- `/qr`  - Generate QR code.
- `/remember` - Write this message to the database.
- `/search`  - Search database for messages with tags.
- `/topnews`  - Get N top Hacker News stories.
- `/urban`  - Look for definitions in Urban Dictionary.
- `/weather`  - Show current weather in the specified location.
- `/wiki` - Try to search Wikipedia article for the specified topic.
- `/xkcd`  - Latest or specific xkcd comics.
