import csv,queue,collections
edgeFile = 'edges.csv'

def bfs(start, end):
    # Begin your code (Part 1)
    """
    1. Load the csv file into rows
    2. Store them into the list adj in the format:  
        adj[from]= {[to, distance],[ ],...}
    3. Use queue to implement bfs, visit store the isited nodes
    4. parent{[,]} stores node's parent and their distance
    5. Run bfs
    6. Trace back parent to compute distance and path
    7. Return
    """
    
    adj=collections.defaultdict(list)
    with open(edgeFile,newline='') as file:
        content=csv.reader(file)
        headers = next(content)
        for row in content:
            adj[int(row[0])].append([int(row[1]), float(row[2])])
            
    num_visited=0 
    parent={}   
    visit =[]
    q =queue.Queue()
    q.put(start)
    visit.append(start)
    flag=1
    
    while (not q.empty()) & flag==1:
        node=q.get()
        for v in adj[node]:
            if(v[0]==end):
                parent[v[0]]=[node,0]
                flag=0
                break
            if v[0] not in visit:
                num_visited += 1
                visit.append(v[0])
                parent[v[0]] = [node, v[1]]
                q.put(v[0])
                
    tmp=end
    dist=0.0 
    path=[]
              
    while (tmp!=start):
        path.insert(1,tmp)
        dist+=parent[tmp][1]
        tmp=parent[tmp][0]
    path.insert(1,start)                
   
    return path, dist, num_visited
    #raise NotImplementedError("To be implemented")
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
