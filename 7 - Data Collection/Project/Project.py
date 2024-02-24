import requests
import json

def get_json(PageNum=1, PageSize=16, Capacity=3, StartDate=..., EndDate=..., City='city-ramsar'):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://www.jabama.com',
        'Referer': 'https://www.jabama.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'X-User-Experiments': '1706603592491000-TEST_EXPERIMENT,DUMMY_EXPERIMENT,CANCELLATION_RESELL',
        'ab-channel': 'GuestDesktop,2.32.2,Windows Server 2008 R2 / 7,7,undefined,2f6b692b-39e0-4c54-b199-83947232f9c8',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'allowEmptyCity': 'true',
        'hasUnitRoom': 'true',
        'guarantees': 'false',
        'platform': 'desktop',
    }

    json_data = {
        'page-size': PageSize,
        'capacity': Capacity,
        'page-number': PageNum,
        'date': {
            'start': 20240219,
            'end': 20240220,
        },
    }

    return requests.post(f'https://gw.jabama.com/api/v4/keyword/{ City }', headers=headers, params=params, json=json_data).json()


def get_accommodation_dict(accomm, accomm_dict = {}): # Structure of keys : (our_dict_key_name, api_parent_key_name, api_key_name) or (key_name, parent_key_name)
    keys_list = [('areaSize', 'accommodationMetrics'), ('bathroomsCount', 'accommodationMetrics'), ('bedroomsCount', 'accommodationMetrics'), ('buildingSize', 'accommodationMetrics'), ('iranianToiletsCount', 'accommodationMetrics'), ('toiletsCount', 'accommodationMetrics'), ('name', None), ('kind', None), ('min_night', None), ('min_price', None), ('payment_type', None), ('region', None), ('reservation_type', None), ('city', 'location'), ('province', 'location'), ('geo', 'location'), ('rate_count', 'rate_review', 'count'), ('rate_score', 'rate_review', 'score'), ('type', None), ('status', None), ('verified', None), ('mainPrice', 'price'), ('discountedPrice', 'price'), ('price_perNight', 'price', 'perNight'), ('placeType', None), ('capacity_base', 'capacity', 'base'), ('capacity_extra', 'capacity', 'extra')]
    for key in keys_list : accomm_dict[ key[0] ] = accomm[ key[1] ][ key[2] ] if len(key) == 3 else accomm[ key[1] ][ key[0] ] if key[1] else accomm[ key[0] ]

    accomm_dict['amenities'] = [ item['name'] for item in accomm['amenities'] ]
    accomm_dict['url'] = f"https://www.jabama.com/stay/villa-{ accomm['code'] }"

    return accomm_dict


def write_data(accomm_list): 
    with open(f'accommodations_data.json', 'w') as f : json.dump(accomm_list, f)

def col_city(city_keyword):
    data, PageNum, accommodations_list = get_json(PageNum=1, City=city_keyword), 1, []
    print(city_keyword)
    
    total = data['result']['total']

    while data['result']['items']:
        print(f"Collecting page { PageNum } of city { city_keyword.split('-')[1] }...")

        for accomm in data['result']['items']: 
            accommodations_list.append( get_accommodation_dict(accomm) )

        print(f'Collected { len( accommodations_list ) } / { total }')

        PageNum += 1
        data = get_json(PageNum=PageNum, City=city_keyword)

    return accommodations_list

def get_cities(): 
    with open('cities.txt', 'r') as f : return f.read().split('\n')

accom_list = []
for city in get_cities():
    accom_list += col_city(city)

write_data( accom_list )