# this script might be useful when imported into an interactive terminal
from math import lcm, gcd

def encrypt(m, e, n):
  number = int.from_bytes(m.encode('utf-8'))
  if (number >= n) :
    print(f'WARNING: m > n, overflow occured ({number} >= {n})')
  return (number ** e) % n

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




