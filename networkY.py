class Graph:
    
    graph_dict={}
    
    def addNode(self,node,attributes={},neighbor=None):        
        if node not in self.graph_dict:
            self.graph_dict[node] = {'attributes':attributes,'connections':[]}
    
    def addEdge(self,node,neighbour):  
        if node not in self.graph_dict:
            self.addNode(node,neighbour)
        else:
            self.graph_dict[node]['connections'].append(neighbour)
            
    def show_edges(self):
        for node in self.graph_dict:
            for neighbour in self.graph_dict[node]:
                print("(",node,", ",neighbour,")")
    
    def getGraph(self):
        return(self.graph_dict)
            

if __name__ == "__main__":
    g= Graph()
    g.addNode("1")
    g.addNode("2")
    g.addEdge("1","2")
    G = g.getGraph()

#%%
