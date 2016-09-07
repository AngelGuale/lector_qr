import re

out2="12_28_1232342a"
patron=re.compile('[0-9]{2}_[0-9]{2}_[0-9]{6}')
res=re.match(patron, out2)
print res
