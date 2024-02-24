from map import cities

def get_neighbors(city):
    return list(cities[city]['neighbors'].keys())

path = []
def find(vertex, end): # Recursive DFS
    path.append(vertex)

    if vertex == end : return vertex

    for neighbor in get_neighbors(vertex):
        if neighbor not in path:
            res = find(neighbor, end)
            if res : return res

    path.remove(vertex)


def find(start, end, way = []): # Simple Recursive DFS
    if not way : way = [start]

    if way[ -1 ] == end : return way

    for n in get_neighbors( way[-1] ):

        if n not in way :
            way.append(n)

            if find(n, end, way) : return way

            way.pop()


def find(start, end, way = []): # Stupid Recursive DFS
    if not way : way = [ start ]
    if way[ -1 ] == end : return [ way ]

    paths = []
    for n in get_neighbors( way[-1] ):

        if n not in way :
            way.append(n)

            new_ways = find(n, end, way.copy())
            if new_ways: [ paths.append( new_way ) for new_way in new_ways if new_way ]

            way.pop()

    res = sorted(paths, key= lambda x: len(x))[ 0 ] if paths else []
    print(res)
    return res