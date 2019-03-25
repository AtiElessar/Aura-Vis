# coding: utf-8
import networkx as nx
import matplotlib.pyplot as plt

def remove_all_edges_iter(u,G):  # Removes all edges from the nodes which have an in-edge from u iteratively (used for cascade revoke)
    edges = list(G.edges(u))
    while edges:
        e = edges[0]
        edges = edges[1:]
        G.remove_edge(e[0],e[1])
        G = remove_all_edges_iter(e[1],G)
    return G


def create_all_grant_diagrams(data):    # Creates the grant diagrams based on the SQL statements
    graph_list = {}

    for line in data:
        line = line.lower()
        line = line.replace(',', ' ')

        line = ' '.join(line.split())
        line = line.replace(' (','(')
        line_list = line.split()

        on = line_list.index('on')
        if 'to' in line_list:
            torF = line_list.index('to')
        else:
            torF = line_list.index('from')
        user1 = line_list[0]
        GorR = line_list[1]
        DB = line_list[on+1]
        user2_list = line_list[torF+1:]
        last = line_list[-1]
        temp = line_list[2:on]
        temp = ','.join(temp)

        while True:
            comma = temp.find(',')
            op = temp.find('(')
            if op > comma:
                priv = temp[:comma]
                graph_names = [DB+"("+priv+")"]
                end = comma

            elif op < comma:
                close = temp.find(')')
                end = close + 1
                cols = temp[op+1:close]
                cols = cols.split(',')
                priv = temp[:op]

                graph_names = []
                for c in cols:
                    graph_names.append(DB+"("+priv+"("+c+")"+")")


            else:
                graph_names = [DB+"("+temp+")"]
                end = len(temp)

            if GorR == 'grant':
                for graph_name in graph_names:
                    if graph_name not in graph_list:
                        graph_list[graph_name] = nx.DiGraph()
                    for u in user2_list:
                        if not graph_list[graph_name].has_edge(user1,u):
                            graph_list[graph_name].add_edges_from([(user1,u)])

            else:
                if last == 'restrict':
                    for graph_name in graph_names:
                        if graph_name not in graph_list:
                            continue
                        for u in user2_list:
                            if graph_list[graph_name].has_edge(user1,u):
                                graph_list[graph_name].remove_edge(user1,u)
                else:
                    for graph_name in graph_names:
                        if graph_name not in graph_list:
                            continue
                        for u in user2_list:
                            if graph_list[graph_name].has_edge(user1,u):
                                graph_list[graph_name].remove_edge(user1,u)
                                graph_list[graph_name] = remove_all_edges_iter(u,graph_list[graph_name])

            temp = temp[end+1:]
            if temp == '':
                break
                
    return graph_list





def draw_grant_diagram(G):  #Displays the required graph

    edges = [edge for edge in G.edges()]

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos,node_size = 500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=edges)
    plt.show()

# top level statements - taking input

filename = input("Input the file path where the SQL statements are stored (Read README to know the to know the input format): ")

f = open(filename)
s = f.read()
s = s.replace("\n", '')
s = s[:-1]
data = s.split(';')

graph_list = create_all_grant_diagrams(data)


print("Now enter the details of the grant diagram you want to visualize")
db = input("Database name (case insensitive): ")
priv = input("Priviledge type without mentioning column (eg- select, update): ")
col = input("Column(/attribute) names (if not relevant, just press enter): ")
if col == '':
    name = db + '('+ priv +')'
else:
    name = db + '('+ priv + '(' + col + ')'+')'

if name not in graph_list:
    print ("ERROR: Invalid table details. Terminating...")
else:
    Gr = graph_list[name]
    draw_grant_diagram(Gr)





