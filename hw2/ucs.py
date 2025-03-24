import csv,collections
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    """
    1. Load the csv file into rows, and convert into adjacent list as above
    2. pre store the[diatance, start, end] of each roads 
    3. parent stores node's parent 
    4. Run ucs: add all road can reached from start to pre
                sort pre and choose the shortest one as next road
                add that road's destination(node[2]) to visit 
                add all roads adjacent to node[2] to pre
                run the loop till find end
    6. Trace back parent to compute distance and path
    7. Return
    """
    adj=collections.defaultdict(list)
    with open(edgeFile,newline='') as file:
        content=csv.reader(file)
        headers = next(content)
        for row in content:
            adj[int(row[0])].append([int(row[1]), float(row[2])])
            
    num_visited=1 
    pre=[] # dis ,from, to
    parent={}  
    visit =[start]
    
    for v in adj[start]:
        if v[0] not in visit:
            pre.append([v[1], start, v[0]])
            
    while pre:
        pre=sorted(pre) #get top element(smallest dist)
        node=pre[0]
        del pre[0]
        
        if(node[2]==end):
            parent[node[2]]=node[1]
            dist=node[0]
            break
        
        if node[2] not in visit:
            visit.append(node[2])
            num_visited+=1
            parent[node[2]]=node[1]
            for v in adj[node[2]]:
                pre.append([node[0]+v[1], node[2], v[0]])
             
    tmp=end
    path=[]
              
    while (tmp!=start):
        path.insert(1,tmp)
        tmp=parent[tmp]
    path.insert(1,start)
    
    return path, dist, num_visited 
    raise NotImplementedError("To be implemented")
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
