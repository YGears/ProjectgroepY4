import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.sparse import csr_matrix

# ==== OPGAVE 1 ====
def plot_number(nrVector):
    # Let op: de manier waarop de data is opgesteld vereist dat je gebruik maakt
    # van de Fortran index-volgorde – de eerste index verandert het snelst, de 
    # laatste index het langzaamst; als je dat niet doet, wordt het plaatje 
    # gespiegeld en geroteerd. Zie de documentatie op 
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html

    #vormen van een 2d array met de juiste ordening. Fortran, first index changing fastest last index changing slowest
    vectorArray = np.reshape(nrVector, (20, 20), 'F')
    #matshow aanmaken met juiste color scheme
    plt.matshow(vectorArray, cmap='gray')
    plt.show()

    pass

# ==== OPGAVE 2a ====
def sigmoid(z):
    # Maak de code die de sigmoid van de input z teruggeeft. Zorg er hierbij
    # voor dat de code zowel werkt wanneer z een getal is als wanneer z een
    # vector is.
    # Maak gebruik van de methode exp() in NumPy.


    # beide opties zijn mogelijk, in het voorbeeld 4.5...e-05 is dat uiteindlijk bijna 0 want 4.5X10**-5 =~0
    return 1 / (1 + (1 / np.exp(z)))
    # return 1 / (1 + np.exp(-z))

    pass


# ==== OPGAVE 2b ====
def get_y_matrix(y, m):
    # Gegeven een vector met waarden y_i van 1...x, retourneer een (ijle) matrix
    # van m×x met een 1 op positie y_i en een 0 op de overige posities.
    # Let op: de gegeven vector y is 1-based en de gevraagde matrix is 0-based,
    # dus als y_i=1, dan moet regel i in de matrix [1,0,0, ... 0] zijn, als
    # y_i=10, dan is regel i in de matrix [0,0,...1] (in dit geval is de breedte
    # van de matrix 10 (0-9), maar de methode moet werken voor elke waarde van 
    # y en m

    #in y^i is een 0 gerepresenteerd als een 10, dat wordt eerst aangepast
    y[y == 10] = 0

    #van vector 1 wordt één array gemaakt, met de bijbehorende waardes
    cols = np.array(np.ndarray.flatten(y))

    rows = [i for i in range(len(cols))]
    data = [1 for _ in range(len(cols))]

    #max is 9, ipv 10 door regel 51
    width = max(cols)+1

    #het maken van de matrix, op basis van gegeven code
    y_vec = csr_matrix((data, (rows, cols)), shape=(len(rows), width)).toarray()
    return y_vec
    pass

# ==== OPGAVE 2c ==== 
# ===== deel 1: =====
def predict_number(Theta1, Theta2, X):
    # Deze methode moet een matrix teruggeven met de output van het netwerk
    # gegeven de waarden van Theta1 en Theta2. Elke regel in deze matrix 
    # is de waarschijnlijkheid dat het sample op die positie (i) het getal
    # is dat met de kolom correspondeert.

    # De matrices Theta1 en Theta2 corresponderen met het gewicht tussen de
    # input-laag en de verborgen laag, en tussen de verborgen laag en de
    # output-laag, respectievelijk. 

    # Een mogelijk stappenplan kan zijn:

    #    1. voeg enen toe aan de gegeven matrix X; dit is de input-matrix a1
    #    2. roep de sigmoid-functie van hierboven aan met a1 als actuele
    #       parameter: dit is de variabele a2
    #    3. voeg enen toe aan de matrix a2, dit is de input voor de laatste
    #       laag in het netwerk
    #    4. roep de sigmoid-functie aan op deze a2; dit is het uiteindelijke
    #       resultaat: de output van het netwerk aan de buitenste laag.

    # Voeg enen toe aan het begin van elke stap en reshape de uiteindelijke
    # vector zodat deze dezelfde dimensionaliteit heeft als y in de exercise.


    #1. Voeg de enen toe
    a1 = np.insert(X, 0, 1, 1)
    Theta1 = Theta1.transpose()
    a1 = np.dot(a1, Theta1)
    #2. roep sigmoid aan a1
    a2 = sigmoid(a1)

    #3. voeg enen toe aan a2
    a2 = np.insert(a2, 0, 1, 1)
    Theta2 = Theta2.transpose()
    a2 = np.dot(a2, Theta2)
    #4. roep sigmoid aan voor a2
    output = sigmoid(a2)


    # print("Theta 1")
    # print(Theta1.shape)
    # print("Theta 2")
    # print(Theta2.shape)
    # print("a1")
    # print(a1.shape)
    # print("a2")
    # print(a2.shape)
    # print("output")
    # print(output.shape)

    return output

    pass



# ===== deel 2: =====
def compute_cost(Theta1, Theta2, X, y):
    # Deze methode maakt gebruik van de methode predictNumber() die je hierboven hebt
    # geïmplementeerd. Hier wordt het voorspelde getal vergeleken met de werkelijk 
    # waarde (die in de parameter y is meegegeven) en wordt de totale kost van deze
    # voorspelling (dus met de huidige waarden van Theta1 en Theta2) berekend en
    # geretourneerd.
    # Let op: de y die hier binnenkomt is de m×1-vector met waarden van 1...10. 
    # Maak gebruik van de methode get_y_matrix() die je in opgave 2a hebt gemaakt
    # om deze om te zetten naar een matrix.

    y_matrix = get_y_matrix(y, len(y))
    prediction = predict_number(Theta1, Theta2, X)

    print(np.sum(np.subtract(prediction, y_matrix))/5000)


    return 7

    pass



# ==== OPGAVE 3a ====
def sigmoid_gradient(z): 
    # Retourneer hier de waarde van de afgeleide van de sigmoïdefunctie.
    # Zie de opgave voor de exacte formule. Zorg ervoor dat deze werkt met
    # scalaire waarden en met vectoren.
    f = 1 / (1 + np.exp(-z))
    return f * (1 - f)

# ==== OPGAVE 3b ====
def nn_check_gradients(Theta1, Theta2, X, y): 
    # Retourneer de gradiënten van Theta1 en Theta2, gegeven de waarden van X en van y
    # Zie het stappenplan in de opgaven voor een mogelijke uitwerking.

    Delta2 = np.zeros(Theta1.shape)
    Delta3 = np.zeros(Theta2.shape)
    m = Delta2.shape[0] #voorbeeldwaarde; dit moet je natuurlijk aanpassen naar de echte waarde van m

    for i in range(m): 
        #YOUR CODE HERE
        pass

    Delta2_grad = Delta2 / m
    Delta3_grad = Delta3 / m
    
    return Delta2_grad, Delta3_grad
