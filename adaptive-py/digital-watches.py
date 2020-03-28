"""
n = int(input())

n = n % (3600 * 24)
h = n // 3600
m = (n % 3600) // 60
s = (n % 3600) % 60

sh = str(h)
sm = str(m)
ss = str(s)

if m // 10 < 1:
	sm = '0' + sm

if s // 10 < 1:
	ss = '0' + ss

print(sh + ":" + sm  + ":" + ss)
"""
from datetime import timedelta as td
print(td(seconds = int(input()) % 86400))
