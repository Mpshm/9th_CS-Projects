import requests

def search(kw): return requests.get(f'https://gw.jabama.com/api/v1/yoda/guest/search/suggestions/{ kw }').json()

cities = set()
alphabets = 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'

for alph in alphabets:
    res = search(alph)['result']['sections'][0]
    if res:
        for city in res['items']:
            kw = city['app']['keyword'] 
            if kw.split('-')[0] == 'city' : cities.add( f"{ kw }" )

cities = str( sorted(list(cities)) ).replace(',', ',\n')
with open('7 - Data Collection/Project/cities.py', 'w') as f: f.write( f'cities = { cities }' )