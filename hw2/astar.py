import csv,collections
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    """
    1. Load the csv file, and convert into adjacent list and heuristic function
    2. parent store parent, dis store distance from start to the node 
    3. open_list is a list of nodes which have been visited, but their neighbors
       haven't all been inspected, starts off with the start node
       closed_list is a list of nodes which have been visited
       and who's neighbors have been inspected
    4. Run astar:
    5. Find a node with the lowest value of f()
    6. If the current node isn't in both open_list and closed_list
       add it to open_list and note n as it's parent
       Otherwise, check if it's closer to first visit n, then m
    7. Remove n from the open_list, and add it to closed_list
    8. Return
    """
    adj=collections.defaultdict(list)
    with open(edgeFile,newline='') as file:
        content=csv.reader(file)
        headers = next(content)
        for row in content:
            adj[int(row[0])].append([int(row[1]), float(row[2])])
            
    h={}
    with open(heuristicFile,newline='') as file:
        content=csv.reader(file)
        headers = next(content)
        for row in content:
            h[int(row[0])]=(float(row[1]))
            
    opened= set([start])
    closed= set([])
    dis = {}
    dis[start] = 0
    parent={}
    parent[start]= 0
    num_visited=0
    

    while opened:
        n=None
        num_visited+=1
        for v in opened:
            if n==None or dis[v]+h[v] < dis[n]+h[n]:
                n=v
        
        if n==end:
            dist=dis[n]
            path=[]
            tmp=end
            while tmp!=start:
                path.append(tmp)
                tmp=parent[tmp]
            path.append(start)

        for m in adj[n]:
            if m[0] not in opened and m[0] not in closed:
                opened.add(m[0])
                parent[m[0]]=n
                dis[m[0]]=dis[n]+m[1]
            else:
                if dis[m[0]]>dis[n]+m[1]:
                    dis[m[0]]=dis[n]+m[1]
                    parent[m[0]]=n
                    if m[0] in closed:
                        closed.remove(m[0])
                        opened.add(m[0])

        opened.remove(n)
        closed.add(n)
    return path, dist, num_visited  
      
    raise NotImplementedError("To be implemented")
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
