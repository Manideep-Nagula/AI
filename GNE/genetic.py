import heapq, argparse
from random import randint
import math
import numpy as np 
from collections import defaultdict
import copy
LOA = math.inf
map = defaultdict(dict)

# Function to calculate cost of a given path
def tsp_cost(graph):
    global map
    cost = 0
    for i in range(len(graph) - 1):
        if (graph[i]) in map and (graph[i + 1]) in map[graph[i]]:
            cost =cost + map[graph[i]][graph[i + 1]]
        else:
            cost = LOA
            break
    if (graph[0]) in map and (graph[-1]) in map[graph[0]]:
        cost =cost + map[graph[0]][graph[-1]]
    else:
        cost = LOA
    return cost
    
def generate_pop(V, pop_size):
    global map
    tsp = tuple([i for i in range(V)])
    pop = []
    heapq.heapify(pop)
    for _ in range(pop_size):
        permutate = np.random.permutation(tsp)
        cost = tsp_cost(permutate)
        if cost != LOA:
            heapq.heappush(pop, tuple([1/cost, tuple(permutate)])) # 1/cost - fitness
        else:
            heapq.heappush(pop, tuple([0, tuple(permutate)]))
    return pop

def mutate(populations, V): # Swapping the nodes between 2 random indexes
    childnodes = []
    heapq.heapify(childnodes)
    pop = copy.deepcopy(populations)
    for pop in pop:
        k = randint(0,V-1) 
        l = randint(0, V-1)
        while k == l:
            l = randint(0, V-1)
        if l < k:
            k,l = l,k
        p = list(pop[1]) 

        while k <= l:
            p[k], p[l] = p[l], p[k]
            k+=1
            l-=1
        c1 = tsp_cost(p)
        if c1 != LOA:
            heapq.heappush(childnodes, tuple([1/c1, tuple(p)]))
        else:
            heapq.heappush(childnodes, tuple([0, tuple(p)]))

    return childnodes

def basic_crossover(populations, V):
     # The first and second half of one parent is assigned to both the
     # offsprings and parent 2 is used to fill the remaining nodes 
    global map
    childnodes = []
    heapq.heapify(childnodes)

    pop = copy.deepcopy(populations)
    
    if(len(pop) % 2 == 1):
        heapq.heappop(pop)
    
    for _ in range(0,len(pop)//2):
        p1 = heapq.heappop(pop)
        parent1 = list(p1[1])
        p2 = heapq.heappop(pop)
        parent2 = list(p2[1])

        off1 = parent1[0:V//2]
        off2 = parent1[V//2:]
        for i in parent2:
            if i in parent1[V//2:]:
                off1.append(i)
            else:
                off2.append(i)

        for t in [off1, off2]:
            cost1 = tsp_cost(t)
        if cost1 != LOA:
            heapq.heappush(childnodes, tuple([1/cost1, tuple(t)]))
        else:
            heapq.heappush(childnodes, tuple([0, tuple(t)]))

    return childnodes

def pmx_crossover(populations, V): # Elements of the first half are exchanged between a random split
    global map
    childnodes = []
    heapq.heapify(childnodes)

    pop = copy.deepcopy(populations)
    if(len(pop) % 2 == 1):
        pop.pop()
    
    for _ in range(0,len(pop)//2):
        
        parent1 = heapq.heappop(pop)
        p1 = list(parent1[1])
        parent2 = heapq.heappop(pop)
        p2 = list(parent2[1])

        ind = randint(0, V-1)
        off1 = list(copy.deepcopy(p1))
        off2 = list(copy.deepcopy(p2))
        for j in range(0, ind+1):
            if p1[j] != p2[j]:
                ind1 = p1.index(p2[j])
                off1[j], off1[ind1] = off1[ind1], off1[j]
                ind2 = p2.index(p1[j])
                off2[j], off2[ind2] = off2[ind2], off2[j]
        
        for t in [off1, off2]:
            c1 = tsp_cost(t)
            if c1 != LOA:
                heapq.heappush(childnodes, tuple([1/c1, tuple(t)]))
            else:
                heapq.heappush(childnodes, tuple([0, tuple(t)]))

    return childnodes


def offsprings(pop, V, pop_size):
  # All functions generate childnodes equal to pop_size
  
    offspring1 = basic_crossover(pop, V)   
    offspring2 = pmx_crossover(pop, V)  
    mut_pop = mutate(pop, V)
    
    for i in offspring1:
        pop.append(i)
    for i in offspring2:
        pop.append(i)
    for i in mut_pop:
        pop.append(i)

    # Retaining the best k childnodes from all the ones created
    for _ in range(len(pop) - pop_size):
        heapq.heappop(pop)
    
    return pop

# function to calculate optimal path using genetic algorithm
def optimal_tsp_path(V, pop, pop_size=1000, no_gen = 100):
    global map
    cur_gen = 1
    optimal_tsp_path = list()
    optimal_tsp_cost = -1
    optimal_tsp_cost_array = []
    
    while cur_gen < no_gen:
            pop = list(item for item in pop)

            min_cost = 0
            tsp_path = []
            for i in pop:
                if i[0] >= min_cost:
                    min_cost = i[0]
                    tsp_path = i[1]

            # Checking optimal path and cost till now
            if optimal_tsp_cost <= min_cost:
                optimal_tsp_cost = min_cost
                optimal_tsp_path = tsp_path
                print("Generation:",cur_gen,"COST: ", int(1/optimal_tsp_cost))

            optimal_tsp_cost_array.append(1/optimal_tsp_cost)
    
            # generating population for next generation
            pop = offsprings(pop, V, pop_size)

            cur_gen += 1

    return optimal_tsp_cost_array, optimal_tsp_path, cur_gen

# Function to add edge to a map
def adding_new_edge_to_map(n1, n2, c):
    global map
    map[n1][n2] = c
    map[n2][n1] = c

# To check if map is connected
def dfs(visited, source):
    global map
    if visited[source] == True:
        return
    visited[source] = True
    for neighbours in map[source]:
        dfs(visited, neighbours)
        
def connected(source, V):
    global map
    visited = [False] * V
    dfs(visited, source)
    
    j = 0
    for i in visited:
        if i == False:
            return False
        j+=1
    return True

if __name__ == '__main__': 

    map_input = None
    path = []
    pop_size = 1000
    no_gen = 250
    inputFile = "50.txt"   
    f = open(inputFile,"r")
    lines = f.readline()
    V = int(lines)

    i = 0

    lines = f.readlines()
    count = 0 
    for line in lines:
        count+=1
        map_input = line.split(" ")
        map_input = map_input[0:len(map_input)-1]
        if map_input is not None:
            j = 0
            for c in map_input:
                if c != '-1':
                    adding_new_edge_to_map(i,j,float(c))
                j+=1
        i+=1

    if len(map) != V:
        i = len(map)-1

        while i < count:
            adding_new_edge_to_map(i,i,0)
            i+=1
    f.close
    if len(map) != 0:

        if connected(list(map.keys())[0], V):
          # Randomly generate initial pop
            pop = generate_pop(V, pop_size)
            
            # Find the path
            costs, path, gens = optimal_tsp_path( V, pop, pop_size, no_gen)
            final_cost = costs[-1]
        else:
            print("\nTSP Not possible as map not connected\n")
    else:
        print("\nGiven map is empty\n")

print(" FINAL OUTPUT :")
print("pop SIZE: ", pop_size, "\tTOTAL GENERATIONS: ", no_gen)
print("FINAL PATH: ", path)
print("FINAL COST: ", int(final_cost))
print("GENERATIONS: ", costs.index(final_cost), '\n')
