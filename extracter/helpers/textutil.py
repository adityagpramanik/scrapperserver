import re

def cleanText(text):
    pattern = r'[^a-zA-Z0-9\s!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]'
    text = re.sub(pattern, '', text)
    text = re.sub(r'\s+', ' ', text)
    return text