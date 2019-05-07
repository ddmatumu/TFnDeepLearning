import numpy as np
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def dataset_lm():
    text_file = """All good so far. I was incredibly hesitant to buy a refurbished phone on Amazon after reading so many negative reviews on various products. I spent a lot of time researching my options and figured this one was probably my safest bet. Phone came in perfect condition (seriously, it looks brand new) and so far all the functions seem great. Set up was easy, unlocked, ready to set my fingerprint and everything. It's fast, sleek, and beautiful. Camera and audio are also great.
1. DEFECTIVE BATTERY - The phone was defective the day it arrived. The battery does not hold a charge consistently or indicate how long it will actually last. This defect is sporadic—so sometimes it works and sometimes it doesn't. I thought I was doing something wrong at first so, after a few weeks of frustration, I did a test to see: tracking how long I charged and how long it lasted. This confirmed it was not my fault or a defective charger and that the phone I purchased from Electonic Deals was the problem."""

    text_io = StringIO(text_file)
            
    def read_data(text_io):
        content = text_io.readlines()
        content = [x.strip() for x in content]
        content = [word for i in range(len(content)) for word in content[i].split()]
        content = np.array(content)
        return content
    
    return read_data(text_io)


def dataset_sentiment_doc():
    text_file = """All good so far. I was incredibly hesitant to buy a refurbished phone on Amazon after reading so many negative reviews on various products. I spent a lot of time researching my options and figured this one was probably my safest bet. Phone came in perfect condition (seriously, it looks brand new) and so far all the functions seem great. Set up was easy, unlocked, ready to set my fingerprint and everything. It's fast, sleek, and beautiful. Camera and audio are also great.
DEFECTIVE BATTERY - The phone was defective the day it arrived. The battery does not hold a charge consistently or indicate how long it will actually last. This defect is sporadic—so sometimes it works and sometimes it doesn't. I thought I was doing something wrong at first so, after a few weeks of frustration, I did a test to see: tracking how long I charged and how long it lasted. This confirmed it was not my fault or a defective charger and that the phone I purchased from Electonic Deals was the problem."""

    
    
    return text_file