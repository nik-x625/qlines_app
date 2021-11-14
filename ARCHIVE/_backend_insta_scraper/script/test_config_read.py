import time
import configparser

configParser = configparser.RawConfigParser()   
configParser.read('./test_config.cfg')

res = configParser.get('test_section', 'do_sleep')
res = int(res)
print(res)

if res:
    print ('yes')
else:
    print ('no')

time.sleep(6)

configParser.read('./test_config.cfg')
res = configParser.get('test_section', 'do_sleep')
print(res)

res = int(res)

if res:
    print ('yes')
else:
    print ('no')
