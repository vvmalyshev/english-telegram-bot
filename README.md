# English Telegram Bot

Telegram Bot for learning your English vocabulary.

## What does it do?

You may add words in your dictionary and train your English vocabulary. Study mode randomly give you word or translation for answering from your study list. Every word you add has 5 trying to be guessing. After you guess 5 times, word is dropped out from your study list.

## What skills I used in this project:

* pandas library
* regular expressions
* parsing HTML
* basic algoritms, cycles, functions
* exceptions 

## How does it do?

Bot listen all messages to your bot on api.telegram.org
<br>After he recognized message which has not answered yet and work with it.
<br>Depending on the message, bot reply appropriately.
<br>There are two .csv files: dictionary.csv, config.csv

* dictionary.csv contains words, translations for every user, who have unique chat_id.
* config.csv contains user's information:chat_id, mode of work(study, add, delete, seeing dictionary)

All adding, changing and deleting work with Pandas library.
<br>There is full security from wrong typing in any situations

## Installing

<br>First of all, you need install Python 3 and follow libraries: Pandas, Json, Requests, Beautiful Soup 4, Random, Re, Time.
<br>Also you must fill files: my_proxy.py(your proxy server), my_token.py(token of your telegram bot), my_chat_id(your chat id  in telegram for retranslating you all messages of other people, who use your bot).
<br>start Englishbot.py

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
