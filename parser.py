import pyperclip
import json

RequestHeaders = dict[str, str]
RequestInfo = (str, str, RequestHeaders)

def parse_js_clipboard() -> RequestInfo:
  code = pyperclip.paste().splitlines()
  return parse_js(code)

def parse_js(code: str) -> RequestInfo:
  url: str = code[0][8:-4]
  method: str = code[-4][13:-2]
  headers: RequestHeaders = {}

  for line in code[2:-7]:
    name, _, value = line.strip() \
                         .removesuffix(",") \
                         .partition(": ")

    headers[json.loads(name)] = json.loads(value)

  return (url, method, headers)
