from math import lcm, gcd
def print_function_list():
  print("""-----------------------------------------------------------------
encrypt(m, e, n): Encrypts a message.
          Params:   m: str   e: int   n: int
          Returns: int
decrypt(m, d, n): Decrypts a message.
          Params:   m: int   d: int   n: int
          Returns: str
get_edn_from_pq(p, q): Generates e, d, n.
          Params:   p: int   q: int
          Returns: tuple
nth_int_root(x, n): Calculates nth root.
          Params:   x: int   n: int
          Returns: int
-----------------------------------------------------------------""")

def encrypt(m, e, n):
  number = int.from_bytes(m.encode('utf-8'))
  if (number >= n):
    print(f'WARNING: m > n, overflow occured ({number} >= {n})')
  elif (number ** e <= n):
    print(f'NOTICE: encryption is weak (m ** e < n)')
  return pow(number, e, n)

def decrypt(m, d, n):
  number = pow(m, d, n)
  return int.to_bytes(number, (number.bit_length() + 7) // 8).decode('utf-8')

def get_edn_from_pq(p, q):
  CMTF = lcm(p-1, q-1) # https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Example
  for e in range(3, CMTF):
    if (gcd(e, CMTF) == 1):
      break
  d = pow(e, -1, CMTF) # https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
  print(f'e:{e}\nd:{d}\nn:{p*q}')
  return (e, d, p * q)

def nth_int_root(x, n):
  low, high = 0, x
  new_result = x+1
  old_result = x+2
  while old_result != new_result:
    mid = (high + low) // 2
    if new_result > x:
      high = mid
    elif new_result < x:
      low = mid
    root = (high + low) // 2
    old_result = new_result
    new_result = root ** n
  return root

def print_attack_list():
  print("""-----------------------------------------------------------------
attack1(M, e, n, _range, plaintext):
        Performs an attack on RSA encryption when m ** e is not much bigger than n.
        This may happen if the plaintext is short, lacks padding, and e is small.
          M (int, optional): The integer message. Default is False (will prompt for input).
          e (int, optional): The public exponent. Default is False (will prompt for input).
          n (int, optional): The modulus. Default is False (will prompt for input).
          _range (int, optional): The number of iterations for the attack. Default is False (will prompt for input).
          plaintext (str, optional): The plaintext message. Default is False (will prompt for input).
          Returns:
              None
factor(n):
        Attempts to factor the given integer n
        Uses factordb and then attempts to manually factor
        Warning: kind of shit
factorDB(n):
        requests the factorization from http://factordb.com/api
        checks if its valid and returns it if it is

weiner_attack(M, e, n):
        Performs an attack where it finds d if its too small

-----------------------------------------------------------------""")

def attack1(M=False, e=False, n=False, _range=False, plaintext=False):
  if not M:
    M = int(input("give integer M\n"))
  if not e:
    e = int(input("give integer e\n"))
  if not n:
    n = int(input("give integer n\n"))
  if not _range:
    _range = int(input("give number of iterations\n"))
  if not plaintext:
    plaintext = input("give plaintext\n")
  plaintext = plaintext.encode('utf-8')
  
  for i in range(_range):
    x = M + (i * n)
    number = nth_int_root(x, e)
    dec = int.to_bytes(number, (number.bit_length() + 7) // 8)
    if plaintext in dec:
      print(i, '--', int.to_bytes(number, (number.bit_length() + 7) // 8))
    elif i % 10 == 0:
      print(i)
      #print(dec[:32])

def factor(n):
  db = factorDB(n)
  if db:
    print(db)
  else:
    if n > 10**20:
      print("WARNING: if n is made up of large primes this is gonna take a long time")
      print("Reccomend to use https://gitlab.inria.fr/cado-nfs instead")
    print("Factor DB failed factorization, continuing manually")
    from sympy import factorint
    print(factorint(n))

def factorDB(n):
  import json
  import requests
  response = requests.get(f"http://factordb.com/api?query={n}")
  datadict = json.loads(response.content)
  if datadict['status'] in ('C', 'U', 'C*', 'U*'):
    return None
  else:
    return datadict['factors']

def weiner_attack(M, e, n):
  import sys
  # caution: path[0] is reserved for script path (or '' in REPL)
  sys.path.insert(1, './rsa-wiener-attack/')
  from RSAwienerHacker import hack_RSA
  d = hack_RSA(e, n)
  print(decrypt(M, d, n))

#-----------------------------------------------------------------
print_function_list()
print_attack_list()
