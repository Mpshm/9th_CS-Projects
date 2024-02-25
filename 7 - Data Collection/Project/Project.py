from cities import cities
import requests
import json


def get_json(PageNum=1, PageSize=16, Capacity=3, StartDate=..., EndDate=..., City='city-ramsar'):
    json_data = {
        'page-size': PageSize,
        'capacity': Capacity,
        'page-number': PageNum,
        'date': {
            'start': 20240219,
            'end': 20240220,
        },
    }

    return requests.post(f'https://gw.jabama.com/api/v4/keyword/{ City }', json=json_data).json()


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
    total = data['result']['total']

    while data['result']['items']:
        print(f"Collecting page { PageNum } of city { city_keyword.split('-')[1] }...")

        for accomm in data['result']['items']: 
            accommodations_list.append( get_accommodation_dict(accomm) )

        print(f'Collected { len( accommodations_list ) } / { total }')

        PageNum += 1
        data = get_json(PageNum=PageNum, City=city_keyword)

    return accommodations_list


accom_list = []
for city in cities:
    accom_list += col_city(city)

write_data( accom_list )