import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')


def shortest_tour(tours): return min(tours, key=tour_length)


def improve_nn_tsp(cities): return improve_tour(nn_tsp(cities))


def first(collection): return next(iter(collection))


def nearest_neighbor(A, cities): return min(cities, key=lambda C: distance(C, A))


def distance(A, B): return math.hypot(A.x - B.x, A.y - B.y)


def reverse_segment_if_improvement(tour, i, j):
    # Given tour [...A,B...C,D...], consider reversing B...C to get [...A,C...B,D...]
    A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
    # Are old links (AB + CD) longer than new ones (AC + BD)? If so, reverse segment.
    if distance(A, B) + distance(C, D) > distance(A, C) + distance(B, D):
        tour[i:j] = reversed(tour[i:j])
        return True


def improve_tour(tour):
    while True:
        improvements = {reverse_segment_if_improvement(tour, i, j)
                        for (i, j) in subsegments(len(tour))}
        if improvements == {None}:
            return tour


def subsegments(N):
    return [(i, i + length)
            for length in reversed(range(2, N))
            for i in reversed(range(N - length + 1))]


def nn_tsp(cities, start=None):
    C = start or first(cities)
    tour = [C]
    unvisited = set(cities - {C})
    while unvisited:
        C = nearest_neighbor(C, unvisited)
        tour.append(C)
        unvisited.remove(C)
    return tour


def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = all_tours(cities)
    return min(tours, key=tour_length)


def all_tours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities))
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]


def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i - 1]) for i in range(len(tour)))


def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(n)  # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))


def plot_tour(tour):
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')  # blue circle markers, solid line style
    plt.axis('scaled')  # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()


def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)


# Normal nn algorithm
plot_tsp(nn_tsp, make_cities(500))

# Improved nn algorithm
plot_tsp(improve_nn_tsp, make_cities(500))
