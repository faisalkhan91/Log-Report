import re

response_code = re.compile(r"([^\w./-]([0-9]{3})[^.\w/-:])")

code = response_code.search('124.115.0.171 - - [02/Aug/2009:01:08:30 -0400] "HEAD / HTTP/1.1" 200 0')
print(code.group())
