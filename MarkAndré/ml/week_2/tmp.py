import numpy as np
from random import randint
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import sys
import pickle
from scipy.sparse import csr_matrix

with open ('week2_data.pkl','rb') as f:
    data = pickle.load(f)

X, y = data['X'], data['y']

m, n = X.shape
input_layer_size = 400
hidden_layer_size = 25
num_labels = 10

def get_y_matrix(y, m):
    # Gegeven een vector met waarden y_i van 1...x, retourneer een (ijle) matrix
    # van m×x met een 1 op positie y_i en een 0 op de overige posities.
    # Let op: de gegeven vector y is 1-based en de gevraagde matrix is 0-based,
    # dus als y_i=1, dan moet regel i in de matrix [1,0,0, ... 0] zijn, als
    # y_i=10, dan is regel i in de matrix [0,0,...1] (in dit geval is de breedte
    # van de matrix 10 (0-9), maar de methode moet werken voor elke waarde van
    # y en m

    #YOUR CODE HERE
    for i in range(m): #0-4999 is dit okey?
        if y[i] == 10:
            y[i] = 0

    # Transpose
    cols = y.T[0]
    # Lijst (size=m) met index nummers
    rows = [i for i in range(m)]
    # Lijst met alleen 1'en
    data = [1 for _ in range(m)]
    # arrays zijn zero-based
    width = max(cols) + 1
    # compressed sparse row-matrix
    y_vec = csr_matrix((data, (rows, cols)), shape=(m, width)).toarray()
    # print(y[4999])
    # print(y_vec[4999])
    return y_vec

matr = get_y_matrix(y, m)
print (matr.shape)