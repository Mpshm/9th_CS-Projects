from cities import cities
import requests
import json


def get_json(json_data, city_kw): 
    return requests.post(f'https://gw.jabama.com/api/v4/keyword/{ city_kw }', json=json_data).json()


price_range, bathroom_range, bedroom_range = (float('inf'), 0), (float('inf'), 0), (float('inf'), 0) # (min, max)
def set_range(accomm_dict):
    price_range = ( min(price_range[0], accomm_dict['price_perNight']), max(price_range[1], accomm_dict['price_perNight']) )
    bathroom_range = ( min(bathroom_range[0], accomm_dict['toiletsCount']), max(bathroom_range[1], accomm_dict['toiletsCount']) )
    bedroom_range = ( min(bedroom_range[0], accomm_dict['bedroomsCount']), max(bedroom_range[1], accomm_dict['bedroomsCount']) )


def get_accommodation_dict(accomm, accomm_dict = {}): # Structure of keys : (our_dict_key_name, api_parent_key_name, api_key_name) or (key_name, parent_key_name)
    keys_list = [('areaSize', 'accommodationMetrics'), ('bathroomsCount', 'accommodationMetrics'), ('bedroomsCount', 'accommodationMetrics'), ('buildingSize', 'accommodationMetrics'), ('iranianToiletsCount', 'accommodationMetrics'), ('toiletsCount', 'accommodationMetrics'), ('name', None), ('kind', None), ('min_night', None), ('min_price', None), ('payment_type', None), ('region', None), ('reservation_type', None), ('city', 'location'), ('province', 'location'), ('geo', 'location'), ('rate_count', 'rate_review', 'count'), ('rate_score', 'rate_review', 'score'), ('type', None), ('status', None), ('verified', None), ('mainPrice', 'price'), ('discountedPrice', 'price'), ('price_perNight', 'price', 'perNight'), ('placeType', None), ('capacity_base', 'capacity', 'base'), ('capacity_extra', 'capacity', 'extra')]
    for key in keys_list : accomm_dict[ key[0] ] = accomm[ key[1] ][ key[2] ] if len(key) == 3 else accomm[ key[1] ][ key[0] ] if key[1] else accomm[ key[0] ]

    accomm_dict['amenities'] = [ item['name'] for item in accomm['amenities'] ]
    accomm_dict['url'] = f"https://www.jabama.com/stay/{ accomm_dict['type'] }-{ accomm['code'] }"

    set_range( accomm_dict )
    return accomm_dict


def write_data(accomm_list): 
    with open(f'accommodations_data.json', 'w') as f : json.dump(accomm_list, f)


def col_city(city_kw, json_data):
    data, accommodations_list = get_json(json_data, city_kw=city_kw), []
    total = data['result']['total']

    while data['result']['items']:
        print(f"Collecting page { json_data['page-number'] } of city { city_kw.split('-')[1] }...")

        for accomm in data['result']['items']: 
            accommodations_list.append( get_accommodation_dict(accomm) )

        print(f'Collected { len( accommodations_list ) } / { total }')

        json_data['page-number'] += 1
        data = get_json(json_data, city_kw=city_kw)

    return accommodations_list


def col_all(json_data):
    accom_list = []
    for city in cities:
        accom_list += col_city(city, json_data)
        json_data['page-num']

    write_data( accom_list )


def get_score(accomm):
    pass


def init(): 
    global inputs, json_data
    inputs = {
        'primary inputs': {
            'city': input(),
            'start_date': input(),
            'end_date': input(),
            'capacity': int(input())
        },

        'secondary inputs': {
            'bedroomsCount': {'value': 0, 'importance': 0},
            'toiletsCount': {'value': 0, 'importance': 0},
            'amentities': [ {'value': 0, 'importance': 0} ],
            'types': [ {'value': 0, 'importance': 0} ],
            'price': {'value': 0, 'importance': 0}
        }
    }

    json_data = {
        'page-size': 16,
        'capacity': inputs['primary inputs']['capacity'],
        'page-number': 1,
        'date': {
            'start': inputs['primary inputs']['start_date'],
            'end': inputs['primary inputs']['start_date'],
        },
    }


def main():
    init()
    scores = {}
    for accomm in col_city(inputs['city'], json_data):
        scores[ accomm['url'] ] = get_score(accomm)

    return sorted(scores, key=lambda k: scores[k])

main()