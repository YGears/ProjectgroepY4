import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')


def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)


def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)


def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]


def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))


def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed() # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))


def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()


def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.5f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)


# Opdracht 1A
def nearest_neighbour(cities):
    # Versie 1
    # unvisited = set(cities)
    # start = unvisited.pop()
    # tour = [start]
    start = next(iter(cities))                  # determine the starting point
    tour = [start]                              # list of to store the tour/route
    unvisited = set(cities - {start})           # set that keeps track of any unvisited cities
    while unvisited:
        closest_city = City(x=math.inf, y=math.inf)  # create a nearest city using dummy values
        for city in unvisited:
            if distance(start, city) < distance(start, closest_city):
                # for every city in unvisited check if the distance  between exp AB is shorter than AC
                # by looping all cities for city A we now what the closest city to A is.
                # than we add it to the tour and move on with the next city
                closest_city = city

        tour.append(closest_city)               # this is the closest city add it to the tour
        start = closest_city                    # the closest city while now be your next starting point
        unvisited.remove(closest_city)          # removes the city from the unvisited list since it is now visited
    return tour


def reverse_segment_if_better(tour, i, j):
    # Given Tour from Nearest Neigbour or any other tour will do
    # I = J=
    # Given tour [...A,B...C,D...], consider reversing B...C to get [...A,C...B,D...]

    A = tour[i-1]
    B = tour[i]
    C = tour[j-1]
    D = tour[j % len(tour)]

    # Are old links (AB + CD) longer than new ones (AC + BD)? If so, reverse segment.
    if distance(A, B) + distance(C, D) > distance(A, C) + distance(B, D):
        tour[i:j] = reversed(tour[i:j])
    return tour


def alter_tour(tour):
    "Try to alter tour for the better by reversing segments."
    original_length = tour_length(tour)
    for (start, end) in all_segments(len(tour)):
        reverse_segment_if_better(tour, start, end)
    # If we made an improvement, then try again; else stop and return tour.
    if tour_length(tour) < original_length:
        return alter_tour(tour)
    return tour


def all_segments(N):
    return [(i, i + length)
            for length in reversed(range(2, N))
            for i in reversed(range(N - length + 1))]

def improve_nn_tsp(cities): return alter_tour(nearest_neighbour(cities))

generate_cities = make_cities(10)

# 1A
plot_tsp(nearest_neighbour, generate_cities)
plot_tsp(improve_nn_tsp, generate_cities)
# Standaard
# give a demo with 10 cities using brute force
#plot_tsp(try_all_tours, generate_cities)

'''
Opdracht 1 A
5 Test runs, using 10 cities
NN = print(3323 +2709.4 + 2828.9 + 2976 +3731.8) 
result : 15569,0999
Optimal = print(3013.15+2470.4+2732.9+2757.1+3581.5)
result = 14555.050000000001
--> 15569,099/14555,05
Antwoord : ongv 7%
'''

'''
Opdracht 1 B
5 Test runs, using 500 cities (using mark's pc)
500 city tour with length 20591.3 in 0.18750 secs for nearest_neighbour
500 city tour with length 21193.6 in 0.15625 secs for nearest_neighbour
500 city tour with length 21380.9 in 0.15625 secs for nearest_neighbour
500 city tour with length 20827.7 in 0.17188 secs for nearest_neighbour
500 city tour with length 21137.0 in 0.15625 secs for nearest_neighbour
Lengte --> 21026
Tijd --> 0,164 secs
'''

'''
Opdracht 1 C

def check_if_inbound()
    Pak van stad A x en y
    Pak van stad B x en y
    
    If stad a = stad B
        dan is er overlap en voeren we een volgende functie uit
    else
        none
'''

'''
Opdracht 1 D

'''

'''
Opdracht 1 E
Normaal Tijdcomplexiteit van 2-opt-algoritme
O(n3)
Waarom is mij nog niet duidelijk ws N * N^2
2 opt maakt gebruik van NN
NN = O(n^2) want de while loopt triggerd steeds een nieuwe for loop
'''

'''
Bronnen : 
https://jupyter.brynmawr.edu/services/public/dblank/jupyter.cs/FLAIRS-2015/TSPv3.ipynb
https://nbviewer.jupyter.org/url/norvig.com/ipython/TSP.ipynb
https://stackoverflow.com/questions/7781260/how-can-i-represent-an-infinite-number-in-python

'''
