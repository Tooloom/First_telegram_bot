import requests
import misc
from yobit import get_btc
from time import sleep
from random import randint
#import json

token = misc.token
URL = 'https://api.telegram.org/bot' + token + '/'

#------------------------------------------------------------------------
def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()

def get_message():
	data = get_updates()
	last_object = data['result'][-1]
	chat_id = last_object['message']['chat']['id']
	update_id = last_object['update_id']

	if 'sticker' in last_object['message']:
		message_text = last_object['message']['sticker']
	elif 'text' in last_object['message']:
		message_text = last_object['message']['text']

	message = {'chat_id': chat_id,
				'text': message_text,
				'update_id': update_id}

	return message

def send_message(chat_id, text='Oops, something is wrong...'):
	url = URL + f'sendmessage?chat_id={chat_id}&text={text}'
	requests.get(url)

#------------------------------------------------------------------------
class Action:

	def bitcoin(chat_id):
		send_message(chat_id, get_btc())

	def hello(chat_id):
		send_message(chat_id, 'Ку!')

	def game(chat_id):
		number = randint(1, 6)
		send_message(chat_id, f'Окей! Выпало: {number}')

	def coin(chat_id):
		coin = ('Орёл!', 'Решка!')[randint(0, 1)]
		send_message(chat_id, f'Оп! И у нас... {coin}')

	def phrase_0(chat_id):
		send_message(chat_id, 'Мась')
	
		
#------------------------------------------------------------------------
def main():
#   d = get_updates()
#   with open('updates.json', 'w', encoding='utf-8') as file:
#        json.dump(d, file, indent=2, ensure_ascii=False)

	words = {'биткоин': Action.bitcoin,
				'привет!': Action.hello,
				'кость': Action.game,
				'монетка': Action.coin,
				'ась?': Action.phrase_0}

	previous_update = None

	while True:
		answer = get_message()
		chat_id = answer['chat_id']
		text = answer['text'].lower()
		update = answer['update_id']

		if update != previous_update:
			if text in words:
				words[text](chat_id)
			else:
				send_message(chat_id, 'Ась?')
		previous_update = update
		sleep(2)


if __name__ == '__main__':
    main()
