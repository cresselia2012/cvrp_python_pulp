import math
import pulp

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

# formulate CVRP as integer programming problem
# V = { 0, 1, ..., num_nodes - 1 }, where 0 means the depot
problem = pulp.LpProblem( "CVRP", pulp.LpMinimize )

## variables
x = [ [ pulp.LpVariable( 'x_{}_{}'.format( i, j ), cat="Binary" ) \
        if i != j else None for j in range(num_nodes) ] \
        for i in range(num_nodes) ]
u = [ pulp.LpVariable( 'u_{}'.format( i ), demand[i], capacity, cat="Integer" ) \
        for i in range(1,num_nodes) ]

## objective function: \sum_{i \in V}\sum_{j \in V, i!=j} c_ij x_ij
problem += pulp.lpSum( distance[i][j] * x[i][j] for i in range(num_nodes) \
                        for j in range(num_nodes) if i != j )

## constraints:
### \sum_{i \in V\{j}} x_ij = 1 for all j \in V\{0}
for j in range(1,num_nodes):
    problem += pulp.lpSum( x[i][j] for i in range(num_nodes) if i != j ) == 1

### \sum_{j \in V\{i}} x_ij = 1 for all i \in V\{0}
for i in range(1,num_nodes):
    problem += pulp.lpSum( x[i][j] for j in range(num_nodes) if i != j ) == 1

### u_i - u_j + C x_ij <= C - d_j for i, j \in V\{0} i != j such that d_i  + d_j <= C
for i in range(1,num_nodes):
    for j in range(1,num_nodes):
        if i != j and demand[i] + demand[j] <= capacity:
            problem += u[i-1] - u[j-1] + capacity * x[i][j] <= capacity - demand[j]

#print( problem )

# solve
threads = 8
maxSeconds = 60
result = problem.solve(pulp.PULP_CBC_CMD(threads=threads, maxSeconds=maxSeconds))

print("objective value = {}".format(pulp.value(problem.objective)))

# get edges
edges = [ ( i, j ) for i in range(num_nodes) for j in range(num_nodes)
            if i != j and pulp.value(x[i][j]) == 1 ]

# get paths
paths = []
for i,j in edges:
    if i == 0:
        path = [ i, j ]
        while path[-1] != 0:
            for v, u in edges:
                if v == path[-1]:
                    path.append(u)
                    break
        paths.append(path)

for p in paths:
    print(p)

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
fig.savefig("test.png")

