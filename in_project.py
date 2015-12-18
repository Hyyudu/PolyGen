# coding=utf-8

from tools import *
import dicts

def get_aux_data(procedure_key):
	if procedure_key == 'telegram.courier':
		return {'courier_type': {'truck': 'Грузовик', 'ship': 'Корабль'}}
	return {}

def process_item_text(procedure_key, item, text, aux_data = {}):
	if procedure_key == 'telegram.courier':
		item['time'] = 'в первой половине часа' if item['phase'] == 1 else 'во второй половине часа'
	if procedure_key == 'telegram.delivery':
		item['trucks_text'] =''
		for i in range(1, item['trucks']+1):
			item['trucks_text']+= str(i)+'-й везет ящик ______ по адресу: ________________________<br>'
	if procedure_key == 'crysis':
		levels = ["Тривиально", "Легко", "Средне", "Сложно"]
		for i in range(len(levels)):
			val = 2*i+2
			word = levels[i]
			if item['difficulty1']<=val:
				item.setdefault('diff_text1', word)
			if item['difficulty2']<=val:
				item.setdefault('diff_text2', word)
		item.setdefault('diff_text1', 'Адово')
		item.setdefault('diff_text2', 'Адово')
	if procedure_key.startswith('telegram.'):
		for k, v in dicts.telegram_replacements.items():
			text=text.replace(k,v)
	if procedure_key.startswith('order'):
		for k, v in dicts.telegram_replacements.items():
			item['text']=item['text'].replace(k,v)
			item['price']=item['price'].replace(k,v)
	return item, text