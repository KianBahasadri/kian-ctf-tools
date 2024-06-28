#!/usr/bin/python3
import requests
import argparse
import html2text

parser = argparse.ArgumentParser(
  prog='kurl',
  description="""
  A curl-like wrapper for python-requests built by Kian Bahasadri
  
  python-requests deals with quite a lot of background features without every notifying you
  for example it automatically processes redirects, states, cookies, authentication, and more.
  Not to mention it makes minor things more convenient like url-encoding.
  """
)

parser.add_argument('hostname',       help='e.g. google.com')
parser.add_argument('resource',       help='e.g. /login',     default='/', nargs='?')
parser.add_argument('-p', '--port',   help='e.g. 8000',       default='80')
parser.add_argument('-m', '--method', help='e.g. GET',        default='GET')
parser.add_argument('-a', '--args',   help='e.g. key=value',  action='append')
parser.add_argument('-t', '--text',   help='change html to md', action='store_true')
parser.add_argument('-v', '--verbose',help='wont truncate output', action='store_true')

args = parser.parse_args()

if 'http' not in args.hostname:
  url = f'http://{args.hostname}:{args.port}{args.resource}'
else:
  url = f'{args.hostname}{args.resource}'

data = dict()
if args.args:
  for arg in args.args:
    key, value = arg.split('=', 1)
    data[key] = value

method = args.method.upper()
try:
  if method == 'GET':
    response = requests.get(url, params=data)
  elif method == 'POST':
    response = requests.post(url, data=data)
  else:
    req = requests.Request(method=custom_method, url=url, headers=headers)
    prepped = req.prepare()
    with requests.Session() as session:
        response = session.send(prepped)
except requests.exceptions.ConnectionError:
  print("Error: connection refused")
  print(f"URL: {url}")
  exit(1)

# Print the response
def displayResponse(response):
  if args.text:
   text = html2text.HTML2Text().handle(response.text)
  else:
    text = response.text
  print(f'-----STATUS CODE-----\n{response.status_code}')
  print('-----HEADERS-----')
  for header, value in response.headers.items():
    print(header, ':', value)
  if len(text) > 1000 and not args.verbose:
    print(f'-----BODY TRUNCATED-----\n{text[:1000]}')
  else:
    print(f'-----BODY-----\n{text}')


displayResponse(response)
if response.history:
  print(f'\n\n\n-----REDIRECT HISTORY-----\n {response.history}')
  for r in response.history:
    displayResponse(r)

