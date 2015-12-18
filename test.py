# coding=utf-8

cred_email = 'polygraph.gen@gmai.com'
cred_pass = '123qwe456rty'

from tools import *
import urllib.request

import requests, gspread
from oauth2client.client import SignedJwtAssertionCredentials
import ssl
from OpenSSL import crypto

def authenticate_google_docs():
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
	return gc

url = "https://docs.google.com/spreadsheets/d/1hqpNl4enWsEOLmgiuZ4o1u3VoL7vUZKVLuggsJlHOEM/edit#gid=52511974&vpid=B1"
# url = "https://docs.google.com/spreadsheets/d/1Q7GwhfqO59PM4BK6RtHoNVeyNxmBZwPDFmNMYrgAYXE/edit#gid=0&vpid=A1"
# url = "https://docs.google.com/spreadsheets/d/13klWXk1V5MycLN7Ox63SuFc75JGTg6FlN2orBBriX3k/edit#gid=0&vpid=A1"
gc = authenticate_google_docs()
sh = gc.open_by_url(url)
worksheet = sh.get_worksheet(0)
data = worksheet.get_all_values()
print_r(data)