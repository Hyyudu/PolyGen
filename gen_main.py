# coding=utf-8

from tools import *
from gen_config import config
import replacements, in_project, math

def generate():

	# Дополнительные данные, нужные для генерации (другие файлы и т.д.) - определяются в in_project.py
	aux_data = {}
	total_cards_count = {}

	for config_key, config_item in config.items():
		if config_item.get('pass', False):
			continue
		output_filename = 'results/'+config_key+'s.html'
		templates = {}
		output_start = config_item.get('output_start')
		if output_start == None:	# Все как у людей
			output = open('templates/output_start.htm').read()
			for change in ('extra_head', 'extra_body'):
				if config_item.get(change) == None:
					change_val = ''
				else:
					change_val = open('templates/'+config_item.get(change)).read()
				output = output.replace('{'+change+'}', change_val)

			if ('css' in config_item):
				for style in config_item['css']:
					output += '<link rel=stylesheet type="text/css" href="../styles/'+style+'">'+"\n"
			else:
				output += '<link rel=stylesheet type="text/css" href="../styles/'+config_key+'.css">'+"\n"
		else:	# Вообще свой output_start, маргиналы чертовы!
			output = open('templates/'+output_start).read()

		template_file = config_item.get('template_file', config_key+'.main.htm')
			
		try:
			main_stub = open('templates/'+template_file, 'r', encoding='utf-8').read()
		except:
			print(config_key)
			raise
		cnt = 0
		if 'types' in config_item:
			iterator = config_item['types']
		else:
			iterator = ['']
		for datatype in iterator:
			procedure_key = config_key
			if 'datafile' in config_item:
				procedure_key = config_item['datafile']
			if datatype:
				procedure_key +='.'+datatype
			aux_data.update(in_project.get_aux_data(procedure_key))

			#try:
			if 'googlesheet_url' in config_item:
				# gamedata = parse_googlesheet(config_item['googlesheet_url'])
				print("Getting data for "+config_key)
				gamedata = googlesheet_data(config_item['googlesheet_url'])
			else:
				gamedata = parse_csv('content/'+procedure_key+'.csv')
			#except:
				# print "Error parsing "+procedure_key;
				# exit();
			for item in gamedata:
				
			
				if item.setdefault('print',1) == 0:
					continue

				if datatype:
					if not (procedure_key in templates):
						templates[procedure_key] = open('templates/'+procedure_key+'.htm', encoding='utf-8').read()
					text = templates[procedure_key]
				else:
					text = ''

				text = main_stub.replace('{main_part}', text)
				# Начиная отсюда  замены идут для всех, а не только для внутренних подтипов

				item,text = in_project.process_item_text(procedure_key, item, text, aux_data)
				# Основной цикл замен
				tmp,text = in_project.process_item_text(procedure_key, item, text, aux_data)
				while (True):
					old_text = text[:]
					
					text = replace_template_conditions(text, item)
					text = replace_dict_entries(text, item)
					text = replace_by_dict(text, item)
					text = replace_by_dict(text, replacements.rep)
					text = replace_right_end(text, item)
					text = replace_str_repeat(text, item)
					if (old_text == text):
						break



				if item['print']:
					for i in range(item['print']):
						last_item = item == gamedata[-1] and i == item['print'] - 1;
						text1 = text
						output += text1
						cnt+=1
						if cnt%config_item['items_per_page']==0 or last_item:
							output+="</div>\n"
							if not last_item:
								output +="<div class='wrapper {wrapper_class}'>\n\n"
					total_cards_count.setdefault(config_item['items_per_page'],0)
					total_cards_count[config_item['items_per_page']] += item['print']
			print(config_key+" generated")
		output += open('templates/output_end.htm').read()
		
		config_item.setdefault('wrapper_class', 'a4_vert')
		output = output.replace('{wrapper_class}', config_item['wrapper_class'])
		
		open(output_filename, 'w', encoding='utf-8').write(output)

		qty_text = ""
		for ipp, qty in total_cards_count.items():
			qty_text+=str(ipp)+" items per page: "+str(qty)+" cards ("+str(math.ceil(qty/ipp))+" pages total)\n"
		f=open("pages_count.txt", "w")
		f.write(qty_text)
		f.close()