class Graph:
    
    graph_dict={}
    
    def addNode(self,node,neighbor=None,attributes={}):        
        if node not in self.graph_dict:
            self.graph_dict[node] = {'attributes':attributes,'connections':[]}
    
    #TODO: make sure that duplicate edges cant be added!
    def addEdge(self,node,neighbour,weight=None):  
        if node not in self.graph_dict:
            self.addNode(node,neighbour)
        else:
            self.graph_dict[node]['connections'].append({neighbour:weight})
            self.graph_dict[neighbour]['connections'].append({node:weight})
    
    def edges(self):
        edges = []
        #go through all the nodes
        for node,value in self.graph_dict.items():
            #go throug all the nodes connections, there could be more than one
            for conn in value['connections']:
                #access each connections key
                for conn_node,weight in conn.items():
                    #add to the list if an edge does not already exist.
                    if [node,conn_node] not in edges and [conn_node,node] not in edges:
                        edges.append([node,conn_node])
                    
        return(edges)
    
    #gets
    def node_neighbors(self,node):
        neighbors = []
        for conn in self.graph_dict[node]['connections']:
            for n,weight in conn.items():
                neighbors.append(n)
                
        return(neighbors)
            
    def show_edges(self):
        for node in self.graph_dict:
            for neighbour in self.graph_dict[node]:
                print("(",node,", ",neighbour,")")
    
    def getGraph(self):
        return(self.graph_dict)
    
    def number_of_nodes(self):
        return(len(self.graph_dict))
    
    def number_of_edges(self):
        return(len(self.edges()))
    
    def bfs(self,start_node,target=None):

        queue = []
        visited = {}
        queue.append(start_node)
        visited[start_node] = True
        level = {start_node:0}
        parent = {start_node:None}
        i = 1
        
        while len(queue) != 0:
            node = queue.pop(0)
            node_neighbors = self.node_neighbors(node)
            for n in node_neighbors:
                if n not in visited:
                    queue.append(n)
                    visited[n] = True
                    level[n] = i
                    parent[n] = node
            i = i+1
        
        shortest_path = []
        if target != None:
            x = target
            while x != start_node:
                x = parent[x]
                shortest_path.append(x)
                
            shortest_path.reverse()
            shortest_path.append(target)
            
        return(level,parent,shortest_path)
    
#    def dfs(self,start_node):
#        parents = {start_node:None}
#        
#        
#        for n in self.node_neighbors(start_node):
#            if n not in parents:
#                parents[n] = start_node
#                dfs(n)


     

if __name__ == "__main__":
    g= Graph()
    g.addNode('A')
    g.addNode('B')
    g.addNode('C')
    g.addNode('D')
    g.addNode('E')
    g.addEdge('A','B')
    g.addEdge('A','C')
    g.addEdge('B','D')
    g.addEdge('B','E')
    g.addEdge('D','E')
    g.addEdge('C','D')
    G = g.getGraph()
    #print(G)
    #print(g.number_of_nodes())
    #print(g.number_of_edges())
    #print(g.edges())
    #print(g.node_neighbors('A'))
    
    path = g.dfs('A')

#%%


p = path[1]
x = 'E'
while x != 'A':
    x = p[x]
    #print(x)
    

#p['E']


