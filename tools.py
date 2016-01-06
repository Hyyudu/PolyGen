#!/usr/local/python275/python.exe
# coding=utf-8

import re, os, csv, random, dicts
import urllib.request
from gspread import SpreadsheetNotFound


def right_end(x, v1,v2,v3, show_number=True) :
	if ((x%100>=11) and (x%100<=20) ): ret= v3
	elif (x%10==1): ret = v1
	elif (2 <= x%10 <= 4): ret = v2
	else: ret = v3
	if show_number:
		return str(x)+" "+ret
	else:
		return ret

def time_of_day(hour) :
	if hour in range(0, 10) : return "ночью"
	elif hour in range(11, 18) : return "днем"
	else : return "вечером"

def associate(arr, fields):
	if not isinstance(fields, list):
		fields = [fields]
	new_arr = {}
	for item in arr:
		var = new_arr
		for field in fields[:-1]:
			if not item[field] in var:
				var[item[field]] = {}
			var = var[item[field]]
		var[item[fields[-1]]] = item.copy()
	return new_arr;

def print_r(arr, retval = False, level = 0, pre = False):
	if arr == []:
		return "[],\n"
	if arr == {}:
		return "{},\n"
	if not arr:
		return ''
	ret = ''
	if pre:
		ret+='<pre>'
	ret += "{\n" if isinstance(arr, dict) else "[\n"
	level+=1
	if isinstance(arr, dict):
		iter = list(arr.keys())
		iter.sort()
	else:
		iter = arr[:]

	for i in iter:
		ret+="\t"*level
		if isinstance(arr, dict):
			val = arr[i]
			ret += str(i)+' => '
		else:
			val = i
		if (isinstance(val, (list, tuple, dict))):
			ret += print_r(val, True, level)
		elif isinstance(val, str):
			try:
				ret+= "'"+str(val)+"',\n"
			except:
				ret +=  "'"+val.encode('utf-8')+"',\n"
		else:
			ret += str(val)+",\n"

	level-=1
	ret+= "\t"*level+("},\n" if isinstance(arr, dict) else "],\n")
	if pre:
		ret+='</pre>'
	if retval:
		return ret
	else:
		print(ret)



def randomString(length = 10):
	ret = ''
	for i in range(length):
		ret += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
	return ret

def _decode_list(data):
	rv = []
	for item in data:
		if isinstance(item, unicode):
			item = item.encode('utf-8')
		elif isinstance(item, list):
			item = _decode_list(item)
		elif isinstance(item, dict):
			item = _decode_dict(item)
		rv.append(item)
	return rv

def _decode_dict(data):
	rv = {}
	for key, value in data.iteritems():
		if isinstance(key, unicode):
			key = key.encode('utf-8')
		if isinstance(value, unicode):
			value = value.encode('utf-8')
		elif isinstance(value, list):
			value = _decode_list(value)
		elif isinstance(value, dict):
			value = _decode_dict(value)
		rv[key] = value
	return rv

def recode(text, func):
	if isinstance(text, list):
		return map(func, text)
	if isinstance(text, dict):
		return {k: func(v) for k,v in text.items()}
	return func(text)



def cyr2utf(text):
	try:
		ret = recode(text, lambda text:text.decode('cp1251').encode('utf-8'))
		return ret
	except:
		print("ERROR! Cant recode ")
		print_r(text)

def utf2cyr(text):
	return recode(text, lambda text: text.decode('utf-8').encode('cp1251'))


def get_braced_structure(text, start):
	start_byte = text.find(start)
	openclose = {'[':']', '(':')', '{':'}'}
	stack = []
	for i in range(start_byte, len(text)):
		if text[i] in openclose.keys():
			stack.append(text[i])
		elif text[i] in openclose.values():
			if openclose[stack[-1][0]] == text[i]:
				stack.pop()
				if stack == []:
					return text[start_byte:i+1]
			else:
				raise Exception("Wrong brackets set - "+''.join(stack))
		elif len(stack)>0:
			stack[-1]+=text[i]
	return text

def cast_type(val):
	try:
		val = float(val)
		if int(val) == val:
			val = int(val)
	except:
		pass
	return val

def data2arr(data, assoc):
	output = []
	fields = []
	for r in data:
		if fields == []:
			fields = r
			continue
		if len(r) == 0: continue

		try:
			arr={fields[i]:cast_type(r[i]) for i in range(len(fields))}
		except:
			print_r(r)
			return
		output.append(arr)
	if assoc != '':
		output = associate(output, assoc)
	return output

def parse_csv(filename, assoc = ''):
	data = []
	with open(filename) as text:
		reader = csv.reader(text, delimiter = ';', quotechar ='"')
		for r in reader:
			data.append(r)
	return data2arr(data, assoc)

def googlesheet_data(url, assoc = ''):
	import requests, gspread
	from oauth2client.client import SignedJwtAssertionCredentials

	url_key = url.split('/')[-2]

	try:
		sh = googlesheet_data.sheets.get(url_key)
	except AttributeError:
		googlesheet_data.sheets = {}
		sh = None
	if sh == None:
		print("Accessing "+url)
		f = open(os.path.join('PolyGen-7d3d8b4db102.p12'), 'rb')
		SIGNED_KEY = f.read()
		f.close()
		scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
		credentials = SignedJwtAssertionCredentials('polygraph.gen@gmail.com', SIGNED_KEY, scope)

		data = {
			'refresh_token' : '1/qWH0W58yRQzlnsUc4mhsWaaa34_3AwoRJTWZXAPgrAQ',
			'client_id' :  '374210870301-m04qrnv2824ur59l07at476lg99qgsbl.apps.googleusercontent.com' ,
			'client_secret' : 'm1K6cykbP-bWDt0Q7RrCppIi',
			'grant_type' : 'refresh_token',
		}
		r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)

		credentials.access_token = eval(r.text)['access_token']
		gc = gspread.authorize(credentials)
		try:
			sh = gc.open_by_url(url)
		except SpreadsheetNotFound:
			print("No access to Google sheet. Please, share "+url+" to polygraph.gen@gmail.com!")
			return [{}]
		googlesheet_data.sheets[url_key] = sh
	else:
		print("Data found in cache")
	worksheet = sh.get_worksheet(0)
	data = worksheet.get_all_values()
	return data2arr(data, assoc)

# Парсит html гуглдока. Стабильность работы не гарантируется никак!
def parse_googlesheet(url, assoc = ''):
	res = urllib.request.urlopen(url)
	html = res.read().decode('utf-8')
	html = html[html.find('bootstrapData') : html.find('var mergedConfig')]
	print(html)
	html = get_braced_structure(html, 'changes')[9:]
	html = html.replace('null', 'None')
	exec("data="+html+"['firstchunk'][0][1]")
	column_count = data[1][-1]
	row_count = data[1][-3]
	data = data[4]
	out = []
	line = []
	for arr in data:
		if arr==[]:
			line.append('')
		else:
			item = arr[3]
			line.append(item[item[1]] if item!= None else '')
		if(len(line) >= column_count):
			out.append(line)
			line = []
	out.append(line)
	return data2arr(out, assoc)

# Заменяет конструкцию вида {crate:ящик:ящика:ящиков}
def replace_right_end(text, item, options={}):
	if text == '':
		return ''
	p= re.findall('(\{([^\}]*?):(.*?):(.*?):(.*?)\})', text)
	for arr in p:
		value = item.get(arr[1]) if item.get(arr[1]) != None else int(arr[1])
		tup = tuple((value, )+tuple(arr[2:]))
		end = right_end(*tup)
		if options.get('right_end_bold'):
			end = "<b>"+end+"</b>"
		text = text.replace(arr[0], end)
	return text

# Заменяет в тексте конструкцию типа {hit}на значение $dict['hit']
def replace_by_dict(text, dict):
	for k, v in dict.items():
		text = text.replace('{'+k+'}',str(v))
	return text

# Заменяет конструкцию вида {d~player_names:name} на dicts.player_names[item['name']]
def replace_dict_entries(text, item):
	if text== '':
		return ''
	p = re.findall('(\{d~(.*?):(.*?)\})', text)
	for arr in p:
		key = item.get[arr[2]] if item.get(arr[2]) != None else arr[2]
		text = text.replace(arr[0], dicts.__dict__[arr[1]].get(key))
	return text

# Заменяет конструкцию вида {if:item['profit']>0}Прибыль{else}Убыток{endif}
def replace_template_conditions(text, item):
	if text == '':
		return ''
	while 1:
		p = re.search(r"{if(.*?):(.*?)}(.*?){endif\1}", text, re.DOTALL + re.UNICODE)
		# print p
		if not p:
			break
		arr = p.groups()
		# print_r(p.groups())
		check = eval (arr[1])
		out = arr[2].split('{else'+arr[0]+'}')
		new_text = out[0] if check else out[1] if len(out) > 1 else ''
		text = text.replace(p.group(), new_text)
		# return 
	return text
	
# Заменяет конструкцию вида {blabla**item['count']}
def replace_str_repeat(text,item):
	if text == '':
		return ''
	while 1:
		if text == '':
			return ''
		p = re.search(r"\{(.*?)\*\*([^\{\}]*?)\}", text, re.DOTALL + re.UNICODE)
		# print p
		if not p:
			break
		arr = p.groups()
		# print_r(p.groups())
		try:
			value = int(item.get(arr[1]) if item.get(arr[1]) != None else arr[1])
			new_text = arr[0]*value
			text = text.replace(p.group(), new_text)
		except:
			raise Exception("Error in str_repeat template: "+p.group())
		# return 
	return text
