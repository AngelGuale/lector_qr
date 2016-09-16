import re

out2="12_28_1232342a"
out1="alskal"
patron=re.compile('[0-9]{2}_[0-9]{2}_[0-9]{6}')
print patron.match(out2)
print patron.match(out1)
