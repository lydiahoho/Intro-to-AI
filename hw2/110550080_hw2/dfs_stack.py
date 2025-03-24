import csv,collections
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    """
    1. Load the csv file into rows, and convert into adjacent list as above
    2. Use list to implement stack, .pop() return and delete the last element
       .append() push the element 
    4. parent{[,]} stores node's parent and their distance
    5. Run dfs
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
    stack =[start]
    visit.append(start)
    flag=1
    
    while (len(stack)!=0) & flag==1:
        node=stack.pop()
        visit.append(node)
        num_visited+=1
        for v in adj[node]:
            if(v[0]==end):
                parent[v[0]]=[node,0]
                flag=0
                break
            if v[0] not in visit:
                #num_visited += 1
                #visit.append(v[0])
                parent[v[0]] = [node, v[1]]
                stack.append(v[0])
                
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
    # End your code (Part 2)

if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
