from collections import Counter
from collections import OrderedDict

text = input().split() 
len_words = [len(s) for s in text]
counter = Counter(len_words)
sort_counter = OrderedDict(sorted(counter.items()))
for e in sort_counter:
	print("{}: {}".format(e, counter[e]))
