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


def make_cities(n, width=1000, height=1000, seed =None):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities
    # random.seed()
    random.seed(seed if seed is not None else time.time())
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

# Versie 1A
# unvisited = set(cities)
# start = unvisited.pop()
# tour = [start]

# Opdracht 1A
def nearest_neighbour(cities):
    start = next(iter(cities))                  # determine the starting point
    tour = [start]                              # list of to store the tour/route
    unvisited = set(cities - {start})           # set that keeps track of any unvisited cities

    while unvisited:
        # for every city in unvisited check if the distance  between exp AB is shorter than AC
        # by looping all cities for city A we now what the closest city to A is.
        # than we add it to the tour and move on with the next city

        # create a nearest city using dummy values
        closest_city = City(x=math.inf, y=math.inf)
        for city in unvisited:
            if distance(start, city) < distance(start, closest_city):
                closest_city = city

        tour.append(closest_city)       # this is the closest city add it to the tour
        start = closest_city            # the closest city while now be your next starting point
        unvisited.remove(closest_city)  # removes the city from the unvisited list since it is now visited
    return tour

'''
# Opdracht 1C/D
def two_opt_swap(route, i, k):
    # 1. take route[0] to route[i-1] and add them in order to new_route
    # 2. take route[i] to route[k] and add them in reverse order to new_route
    # 3. take route[k+1] to end and add them in order to new_route
    new_route = route[:i] + list(reversed(route[i:k])) + route[k:]
    return new_route


# Opdracht 1D
def nearest_neighbour_2opt(cities):
    # Function that applies the 2opt swap in order to improve its tour length
    # returns tour when no improvements can be made
    tour = nearest_neighbour(cities)        # use a existing tour
    improved = True

    while improved:
        # While there is an improvement to be made ......
        best_tour_length = tour_length(tour)
        improved = False

        # number of cities/nodes eligible to be swapped
        for i in range(len(tour)-1):        # het aantal nodes gaat elke mogelijke node bij langs daarom is de tijd nog te hoog
            for k in range(i+1, len(tour)):
                # Try a new tour using the 2opt swap
                new_tour = two_opt_swap(tour, i, k)
                # Calculate the distance of this new tour
                new_tour_length = tour_length(new_tour)

                # if improvement can be made, improve and try again
                if new_tour_length < best_tour_length:
                    # The existing tour becomes the improved tour
                    tour = new_tour
                    best_tour_length = new_tour_length
                    improved = True
    return tour
'''


def nearest_neighbour_2opt(cities):
    return improve_tour(nearest_neighbour(cities))

def improve_tour(tour):
    # Function to improve the tour by shorting the length of segments using two opt
    original_length = tour_length(tour)
    # For every segment(start, end) in all combinations of segments of tour length
    # Do the two opt
    for (start, end) in all_segments(len(tour)):
        two_opt_segment_swap(tour, start, end)
    # If we made an improvement, then try again; else stop and return tour
    if tour_length(tour) < original_length:
        return improve_tour(tour)
    return tour

def all_segments(tour_size):
    # Return (start, end) pairs of indexes that form segments of tour of length N
    # print([(start, start + length) for length in range(tour_size, 1, -1) for start in range(tour_size - length + 1)])
    return [(start, start + length) for length in range(tour_size, 1, -1) for start in range(tour_size - length + 1)]

def two_opt_segment_swap(tour, start, end):
    # Take 4 cities, consider that AB and CD are connect try swap one city for another
    A, B, C, D = tour[start-1], tour[start], tour[end-1], tour[end % len(tour)]
    # If old links (AB + CD) are longer than new ones (AC + BD) then reverse segment
    if distance(A, B) + distance(C, D) > distance(A, C) + distance(B, D):
        tour[start:end] = reversed(tour[start:end])
        return True


generate_cities = make_cities(500, seed=2)
# 1A
plot_tsp(nearest_neighbour, generate_cities)
# 1D
plot_tsp(nearest_neighbour_2opt, generate_cities)



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

Is het noodzakleijk om te controleren of de nieuwe route korter is dan de oude? 
(volgensmij niet want in de colleges werd benoemd dat als een route niet meer kruist dat hij dan altijd korter is. 

Maar wij hebben geimpliceerd dat het bewerken van een connectie lijd tot een kortere route.
Om deze door te voeren vergelijken wij hem wel doormiddel van de afstand

'''

'''
Opdracht 1 D

Bij seed 22 met 500 steden
in 2,31250 s een lengte van 17500,6 ten opzichte van Nearest Neigbour met 20883,4
Dit is ongv 19%
Probeer je meerdere seeds zie je ongv een verbetering van 10% +/-

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
https://en.wikipedia.org/wiki/2-opt
'''
