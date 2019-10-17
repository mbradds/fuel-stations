import math
import pickle

class Graph:
    '''
    class for a simple undirected graph. Nodes can contain descriptive data, and edges can contain weights.
    
    '''
    #TODO: add atatic methods that read and write to pickle
    def __init__(self):
        
        self.graph_dict={}
        self.edges = []
    
    @staticmethod
    def savePickle(G,file_name):
        outfile = open(file_name,'wb')
        pickle.dump(G.getGraph(),outfile)
        outfile.close()
    
    @staticmethod
    def readPickle(file_name):
        infile = open(file_name,'rb')
        G = pickle.load(infile)
        infile.close()
        new_graph = Graph()
        new_graph.graph_dict = G
        return(new_graph)
        
    def addNode(self,node,neighbor=None,attributes={}):        
        if node not in self.graph_dict:
            #self.graph_dict[node] = {'attributes':attributes,'connections':[]} #change connections to a dictioanry for fast hash lookup!
            self.graph_dict[node] = {'attributes':attributes,'connections':{}}
    
    def nodes(self):
        return(list(self.graph_dict.keys()))
    
    def node(self,n):
        return(self.graph_dict[n])

    # TODO: make sure that duplicate edges cant be added!
    def addEdge(self, node, neighbour, weight=None):
        if node not in self.graph_dict:
            self.addNode(node)
        elif neighbour not in self.graph_dict:
            self.addNode(neighbour)

        self.graph_dict[node]["connections"][neighbour] = weight
        self.graph_dict[neighbour]["connections"][node] = weight
        self.edges.append([node, neighbour])

    def is_connection(self, node, neighbour):
        """
        uses hashing to quickly check if there is a connection. The worst case run time is a double hash lookup (n=number of nodes)
        """

        try:
            self.graph_dict[node]["connections"][neighbour]
            connection = True
        except KeyError:

            try:
                self.graph_dict[neighbour]["connections"][node]
                connection = True
            except KeyError:
                connection = False

        return connection

    # gets all direct connections
    def node_neighbors(self, node):
        neighbors = []
        for key in self.graph_dict[node]["connections"]:
            neighbors.append(key)

        return neighbors

    def edge_weight(self, node, neighbour):
        return self.graph_dict[node]["connections"][neighbour]

    def show_edges(self):
        for node in self.graph_dict:
            for neighbour in self.graph_dict[node]:
                print("(", node, ", ", neighbour, ")")

    def remove_edges(self, edge_list):

        for edge in edge_list:
            del self.graph_dict[edge[0]]["connections"][edge[1]]
            del self.graph_dict[edge[1]]["connections"][edge[0]]

    def getGraph(self):
        return self.graph_dict

    def number_of_nodes(self):
        return len(self.graph_dict)

    def number_of_edges(self):
        return len(self.edges)

    def bfs(self, start_node, target=None):

        queue = []
        visited = {}
        queue.append(start_node)
        visited[start_node] = True
        level = {start_node: 0}
        parent = {start_node: None}
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
            i = i + 1

        shortest_path = []
        if target != None:
            x = target
            while x != start_node:
                x = parent[x]
                shortest_path.append(x)

            shortest_path.reverse()
            shortest_path.append(target)

        return (level, parent, shortest_path)

    def dijkstra(self, start):

        routes_from_city = {}
        visited_cities = []
        current_city = start

        for node in self.graph_dict:
            if node == start:
                routes_from_city[node] = [0, node]
            else:
                routes_from_city[node] = [math.inf, None]

        while current_city:
            visited_cities.append(current_city)

            neighbors = self.node_neighbors(current_city)

            for next_city in neighbors:
                price = self.edge_weight(current_city, next_city)

                if (
                    routes_from_city[next_city][0]
                    > price + routes_from_city[current_city][0]
                ):
                    routes_from_city[next_city] = [
                        price + routes_from_city[current_city][0],
                        current_city,
                    ]

            # find the cheapest unvisited neighbor

            current_city = None
            cheapest_route = math.inf
            for key, val in routes_from_city.items():
                price, previous_city = val[0], val[1]
                if price < cheapest_route and key not in visited_cities:
                    cheapest_route = price
                    current_city = key

        # shortest path can be found from routes_from_city
        # shortest path from Atlanta to Chicago:
        # 1) set start = atlanta
        # 2) routes_from_city['Chicago']

        return routes_from_city


if __name__ == "__main__":
    g= Graph()
    g.addNode(node = 'Atlanta',attributes={'lat':50,'long':100})
    g.addNode('Boston')
    g.addNode('Chicago')
    g.addNode('Denver')
    g.addNode('El Paso')
    g.addEdge('Atlanta','Boston',weight=100)
    g.addEdge('Atlanta','Denver',weight=160)
    g.addEdge('Boston','Chicago',weight=120)
    g.addEdge('Boston','Denver',weight=180)
    g.addEdge('Chicago','El Paso',weight=80)
    g.addEdge('Denver','Chicago',weight=40)
    g.addEdge('Denver','El Paso',weight=40)
    print(g.node('Atlanta')['attributes']['lat'])
    print(g.number_of_edges())
    #g.remove_edges([['Atlanta','Boston']])

    G = g.getGraph()

    d = g.dijkstra("Atlanta")

#%%
