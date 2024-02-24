from map import cities

def get_neighbors(city):
    return list(cities[city]['neighbors'].keys())

def get_real_distance(city1, city2):
    return cities[city1]['neighbors'][city2]

def least_weighted(table): 
    checking = { element : table[ element ] for element in table if type( table[element]['weight'] ) == int and not table[element]['is_visited'] }
    return table[ min(checking, key=lambda item: table[item]['weight'] ) ]


def find(start, end): # Dijkstra
    cities_table = { city : {'name' : city, 'weight' : float('inf'), 'path' : [], 'is_visited' : False } if city != start else {'name' : city, 'weight' : 0, 'path' : [ start ], 'is_visited' : False } for city in cities }

    while not cities_table[end]['is_visited']:
        target = least_weighted( cities_table )
        for n in get_neighbors( target['name'] ):
            new_weight = target['weight'] + get_real_distance(target['name'], n)
            if cities_table[n]['weight'] > new_weight:
                cities_table[n]['weight'] = new_weight
                cities_table[n]['path'] = target['path'] + [ n ]

        target['is_visited'] = True

    return cities_table[end]['path']