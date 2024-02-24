from map import cities

def get_neighbors(city):
    return list(cities[city]['neighbors'].keys())

def find(start, end): # Recursive BFS
    if start == end : return end
    queue = [start]
    neighbors = get_neighbors( queue[0] )
    while end not in neighbors:
        for n in neighbors: 
            if n not in queue : queue.append(n)
        queue.pop(0)
        neighbors = get_neighbors( queue[0] )

    path = find(start, queue[0] )
    if type(path) == str : path = [ path ]
    return path + [ end ]

def find(start, end): # BFS
    queue = [[start]]
    while queue[0][-1] != end:
        path = queue.pop(0)
        for n in get_neighbors(path[-1]): 
            if n not in path : queue.append( path + [ n ] )

    return queue[0]