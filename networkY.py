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
            

if __name__ == "__main__":
    g= Graph()
    g.addNode('1')
    g.addNode('2')
    g.addNode('3')
    g.addNode('4')
    g.addEdge('1','2')
    g.addEdge('1','3')
    g.addEdge('2','3')
    g.addEdge('3','4')
    g.addEdge('2','4')
    G = g.getGraph()
    print(G)
    print(g.number_of_nodes())
    print(g.number_of_edges())
    print(g.edges())
    print(g.node_neighbors('1'))

#%%
