# Python 3.7

import requests
from bs4 import BeautifulSoup
from pyrogram import Client
import schedule
import time
import session


def get_text(web):
    final_text = ''
    response = requests.get(web, stream=True)
    soup = BeautifulSoup(response.content, 'html.parser')
    word_or_idiom = soup.h1.text
    word_or_idiom_text = soup.h2.text
    meaning = soup.h3.text
    meaning_text = soup.find_all('p')
    if meaning_text[0].text.startswith('Today'):
        meaning_text = meaning_text[1].text
    examples = soup.find('', class_='example')
    if examples:
        examples = examples.text
    if not examples:
        examples = ''

    final_text += '**' + word_or_idiom + ':**' + '\n'\
                  + word_or_idiom_text + '\n'\
                  + '**' + meaning + '**' + '\n'\
                  + meaning_text + '\n'\
                  + examples
    return final_text


def send_message():
    session_token = session.session_token
    with Client(session_token) as app:
        app.send_message('@englishwospam', time.localtime())
        website_links = ['https://www.englishclub.com/ref/idiom-of-the-day.php',
                         'https://www.englishclub.com/ref/slang-of-the-day.php',
                         'https://www.englishclub.com/ref/phrasal-verb-of-the-day.php',
                         'https://www.englishclub.com/ref/saying-of-the-day.php']

        for web in website_links:
            text = get_text(web)
            app.send_message('@englishwospam', text)
            print(text)


def print_time():
    print(time.localtime())


# schedule crawler
schedule.every(1).minutes.do(print_time)
schedule.every(2).minutes.do(send_message)
schedule.every().day.at("10:30").do(send_message)

# run script infinitely
while True:
    schedule.run_pending()
    time.sleep(2)
