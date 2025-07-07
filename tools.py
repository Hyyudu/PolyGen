import re, os, csv, random, dicts
import urllib.request


def right_end(x, v1, v2, v3, show_number=True):
    if ((x % 100 >= 11) and (x % 100 <= 20)):
        ret = v3
    elif (x % 10 == 1):
        ret = v1
    elif (2 <= x % 10 <= 4):
        ret = v2
    else:
        ret = v3
    if show_number:
        return str(x) + " " + ret
    else:
        return ret


def time_of_day(hour):
    if hour in range(0, 10):
        return "ночью"
    elif hour in range(11, 18):
        return "днем"
    else:
        return "вечером"


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


def print_r(arr, retval=False, level=0, pre=False):
    if arr == []:
        return "[],\n"
    if arr == {}:
        return "{},\n"
    if not arr:
        return ''
    ret = ''
    if pre:
        ret += '<pre>'
    ret += "{\n" if isinstance(arr, dict) else "[\n"
    level += 1
    if isinstance(arr, dict):
        iter = list(arr.keys())
        iter.sort()
    else:
        iter = arr[:]

    for i in iter:
        ret += "\t" * level
        if isinstance(arr, dict):
            val = arr[i]
            ret += str(i) + ' => '
        else:
            val = i
        if (isinstance(val, (list, tuple, dict))):
            ret += print_r(val, True, level)
        elif isinstance(val, str):
            try:
                ret += "'" + str(val) + "',\n"
            except:
                ret += "'" + val.encode('utf-8') + "',\n"
        else:
            ret += str(val) + ",\n"

    level -= 1
    ret += "\t" * level + ("},\n" if isinstance(arr, dict) else "],\n")
    if pre:
        ret += '</pre>'
    if retval:
        return ret
    else:
        print(ret)


def randomString(length=10):
    ret = ''
    for i in range(length):
        ret += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    return ret


def recode(text, func):
    if isinstance(text, list):
        return map(func, text)
    if isinstance(text, dict):
        return {k: func(v) for k, v in text.items()}
    return func(text)


def cyr2utf(text):
    try:
        ret = recode(text, lambda text: text.decode('cp1251').encode('utf-8'))
        return ret
    except:
        print("ERROR! Cant recode ")
        print_r(text)


def utf2cyr(text):
    return recode(text, lambda text: text.decode('utf-8').encode('cp1251'))


def get_braced_structure(text, start):
    start_byte = text.find(start)
    openclose = {'[': ']', '(': ')', '{': '}'}
    stack = []
    for i in range(start_byte, len(text)):
        if text[i] in openclose.keys():
            stack.append(text[i])
        elif text[i] in openclose.values():
            if openclose[stack[-1][0]] == text[i]:
                stack.pop()
                if stack == []:
                    return text[start_byte:i + 1]
            else:
                raise Exception("Wrong brackets set - " + ''.join(stack))
        elif len(stack) > 0:
            stack[-1] += text[i]
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
            arr = {fields[i]: cast_type(r[i]) for i in range(len(fields))}
        except:
            print_r(r)
            return
        output.append(arr)
    if assoc != '':
        output = associate(output, assoc)
    return output


def parse_csv(filename, assoc=''):
    data = []
    print('Getting data from '+filename)
    with open(filename) as text:
        reader = csv.reader(text, delimiter=';', quotechar='"')
        for r in reader:
            data.append(r)
    return data2arr(data, assoc)


def process_csv_value(value: str) -> str | int | float:
    if not value.isnumeric():
        return value
    result = float(value)
    if not result % 1:
        result = int(result)
    return result


def googlesheet_data(*, sheet_id: str, page: str | None = None):
    page = page or 'Лист1'
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sh = service.spreadsheets()
        print(f'Accessing google sheet at {sheet_id}!{page}')
        result = (
            sh.values()
            .get(spreadsheetId=sheet_id, range=page)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        data = [
            dict(zip(values[0], [process_csv_value(val) for val in row]))
            for row in values[1:]
        ]
        for item in data:
            item['print'] = int(item['print'])
        return data
    except HttpError as err:
        print(err)


# Заменяет конструкцию вида {crate:ящик:ящика:ящиков}
def replace_right_end(text, item, options={}):
    if text == '':
        return ''
    p = re.findall(r'(\{([^\}]*?):(.*?):(.*?):(.*?)\})', text)
    for arr in p:
        value = item.get(arr[1]) if item.get(arr[1]) != None else int(arr[1])
        tup = tuple((value,) + tuple(arr[2:]))
        end = right_end(*tup)
        if options.get('right_end_bold'):
            end = "<b>" + end + "</b>"
        text = text.replace(arr[0], end)
    return text


# Заменяет в тексте конструкцию типа {hit}на значение $dict['hit']
def replace_by_dict(text, dict):
    for k, v in dict.items():
        text = text.replace('{' + k + '}', str(v))
    return text


# Заменяет конструкцию вида {d~player_names:name} на dicts.player_names[item['name']],
# или dicts.player_names['name'], если в item нет поля name
def replace_dict_entries(text, item):
    if text == '':
        return ''
    p = re.findall(r'(\{d~(.*?):(.*?)\})', text)
    for arr in p:
        key = item.get[arr[2]] if item.get(arr[2]) != None else arr[2]
        text = text.replace(arr[0], dicts.__dict__[arr[1]].get(key))
    return text



# Заменяет конструкцию вида {blabla**item['count']}
def replace_str_repeat(text, item):
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
            new_text = arr[0] * value
            text = text.replace(p.group(), new_text)
        except:
            raise Exception("Error in str_repeat template: " + p.group() + print_r(item, True))
    # return
    return text
