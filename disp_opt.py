import math

def makeCVRP():
    num_nodes = 32
    capacity = 100
    demand = [ 0, 19, 21, 6, 19,\
               7, 12, 16, 6, 16,\
               8, 14, 21, 16, 3,\
               22, 18, 19, 1, 24,\
               8, 12, 4, 8, 24,\
               24, 2, 20, 15, 2,\
               14, 9 ]
    coordinate = []
    coordinate.append( ( 82, 76 ) )
    coordinate.append( ( 96, 44 ) )
    coordinate.append( ( 50, 5 )  )
    coordinate.append( ( 49, 8 )  )
    coordinate.append( ( 13, 7 )  )
    coordinate.append( ( 29, 89 ) )
    coordinate.append( ( 58, 30 ) )
    coordinate.append( ( 84, 39 ) )
    coordinate.append( ( 14, 24 ) )
    coordinate.append( ( 2, 39 )  )
    coordinate.append( ( 3, 82 )  )
    coordinate.append( ( 5, 10 )  )
    coordinate.append( ( 98, 52 ) )
    coordinate.append( ( 84, 25 ) )
    coordinate.append( ( 61, 59 ) )
    coordinate.append( ( 1, 65 )  )
    coordinate.append( ( 88, 51 ) )
    coordinate.append( ( 91, 2 )  )
    coordinate.append( ( 19, 32 ) )
    coordinate.append( ( 93, 3 )  )
    coordinate.append( ( 50, 93 ) )
    coordinate.append( ( 98, 14 ) )
    coordinate.append( ( 5, 42 )  )
    coordinate.append( ( 42, 9 )  )
    coordinate.append( ( 61, 62 ) )
    coordinate.append( ( 9, 97 )  )
    coordinate.append( ( 80, 55 ) )
    coordinate.append( ( 57, 69 ) )
    coordinate.append( ( 23, 15 ) )
    coordinate.append( ( 20, 70 ) )
    coordinate.append( ( 85, 60 ) )
    coordinate.append( ( 98, 5 )  )

    def computeDistance( c1, c2 ):
        return math.sqrt( pow( c2[0] - c1[0], 2 ) + pow( c2[1] - c1[1], 2 ) )
    distance = [ [ round(computeDistance( c1, c2 )) for c1 in coordinate ] \
                    for c2 in coordinate ]
    return num_nodes, capacity, demand, distance, coordinate

# make problem
num_nodes, capacity, demand, distance, coordinate = makeCVRP()

r1 = [0, 27, 24, 0]
r2 = [0, 21, 31, 19, 17, 13, 7, 26, 0]
r3 = [0, 12, 1 , 16, 30, 0]
r4 = [0, 29, 18, 8, 9, 22, 15, 10, 25, 5, 20, 0]
r5 = [0, 14, 28, 11, 4, 23, 3, 2, 6, 0]

paths = [ r1, r2, r3, r4, r5 ]

edges = []

for p in paths:
    for i in range(len(p)-1):
        edges.append( (p[i], p[i+1] ) )

import networkx as nx
import matplotlib.pyplot as plt

# 有向グラフの作成
G = nx.DiGraph()
G.add_edges_from( edges )

color = [ "r", "g", "y", "m", "c" ]
edge_color = []

for i,j in G.edges:
    for t,path in enumerate(paths):
        if i in path and j in path:
            edge_color.append( color[t] )
            break
assert len(edges) == len(edge_color)

# グラフの描画
pos = { i : coordinate[i] for i in range(num_nodes) }

fig = plt.figure()
nx.draw_networkx( G, pos, edge_color=edge_color, alpha=0.5)

# 表示
plt.axis("off")
fig.savefig("opt.png")
