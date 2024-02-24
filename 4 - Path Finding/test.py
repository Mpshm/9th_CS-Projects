from map import cities

def least_weighted(table): 
  checking = [ { element : table[ element ] } for element in table if table[element]['weight'] and not table[element]['is_visited'] ]
  return min(checking, key=lambda item: table[item]['weight'] ) if checking else None

start = 'Bam'
cities_table = { city : {'weight' : None, 'path' : [], 'is_visited' : False } if city != start else {'weight' : 0, 'path' : [start], 'is_visited' : True } for city in cities}

print( least_weighted(cities_table) )