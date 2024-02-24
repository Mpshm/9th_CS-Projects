from map import cities

def get_neighbors(city):
    return list(cities[city]['neighbors'].keys())

def get_geo_coordinates(city):
    info = cities[city]
    return info['x'], info['y']

def get_real_distance(city1, city2):
    return cities[city1]['neighbors'][city2]

def get_unreal_distance(p1, p2):
    return int(((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5)

def least_weighted(table): return min(table, key=lambda item: table[item]['weight'] )


def find(start, end): # A*
    checking_table, visited = { start : {'name' : start, 'weight' : 0, 'path' : [start] }}, set()

    while end != least_weighted( checking_table ):
        target = checking_table.pop( least_weighted(checking_table) )

        for n in get_neighbors( target['name'] ):
            new_weight = target['weight'] + get_real_distance(target['name'], n) + get_unreal_distance( get_geo_coordinates(n), get_geo_coordinates(end) )
            if n not in checking_table or checking_table[n]['weight'] > new_weight: 
                checking_table[n] = {
                    'name' : n,
                    'weight' : new_weight,
                    'path' : target['path'] + [ n ]
                }

        visited.add( target['name'] )

    return checking_table[end]['path']