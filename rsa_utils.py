# this script might be useful when imported into an interactive terminal
from math import lcm, gcd

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
  attack1(M, e, n, _range, plaintext) - when m ** e is not much bigger than n
      - this may happen if the plaintext is short, lacks padding, and e is small
  attack1_multithread(M, e, n, _range, plaintext) -- multithreaded attack1()
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
    elif i % 1000 == 0:
      print(i)
      #print(dec[:32])
    

