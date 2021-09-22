# A Function that returns successor(s) of a state
# gets the possible next states from a certain state, only gives valid states
def get_next_states(state):
    retstates = []
    possible = ['G', 'W', 'C']  # List of possible moves
    west_side = 0
    east_side = 1
    # West_side --> {'F', 'G', 'C', 'W'} (left)
    # East_side --> Empty set (right)
    if 'F' in state[1]:
        west_side = 1
        east_side = 0
    #
    for i in possible:
        if i in state[west_side]:
            # .....
            newstate = copy_state(state)
            # Farmer and Object leave from the West_side
            newstate[west_side].remove('F')
            newstate[west_side].remove(i)
            # Farmer and Object arrive at the East_side
            newstate[east_side].add('F')
            newstate[east_side].add(i)
            # .....
            retstates.append(newstate)

    newstate = copy_state(state)
    newstate[west_side].remove('F')
    newstate[east_side].add('F')
    retstates.append(newstate)
    return retstates


# Copy of current state
def copy_state(state):
    return (state[0].copy(), state[1].copy())


# A Function that checks if state is valid
def is_valid(state):
    for i in range(2):
        # Check if the Goat and the cabbage are together without the Farmer
        if 'G' in state[i] and 'C' in state[i] and not 'F' in state[i]:
            return False
        # Check if the Wolf and the Goat are together without the Farmer
        if 'W' in state[i] and 'G' in state[i] and not 'F' in state[i]:
            return False
    return True


# prints the given state
def print_state(state):
    for s in state[0]:
        print(s, end='')  # Print object in the set of the Left_side
    print(" | ", end='')  # Seperator CLI between sides
    for s in state[1]:
        print(s, end='')  # Print object in the set of the East_side
    print()               # Break


# check if a state is a goal-state/solution
def is_goal_state(state):
    # state[0] = West needs to be empty all object need to be at state[1] East
    if state[0] == set() and state[1] == {'F', 'G', 'C', 'W'}:
        return True
    return False


# A Function that returns the solution
def dfs(state, visited, final_state):
    # if the current state is the final state, print it and return, else, go through each further possible state
    visited.append(copy_state(state))
    # visited? python functie append , call functie copy state en stop daar state in
    if is_goal_state(state):
        print("Solution found using DFS:")
        for s in visited:
            print_state(s)
        print("")
    else:
        for s in get_next_states(state):
            if is_valid(s):
                if s not in visited:
                    dfs(s, visited.copy(), final_state)
    return final_state


""" 
Start state, tuple with 2 sets one of west_side and one of east_side
All objects/props start on the west_side
"""
state = ({'F', 'G', 'C', 'W'}, set())

# call the function solve
solutions = dfs(state, [], [])
#print(type([]))


"""
Sources used :
AI Les 1 --> https://www.youtube.com/watch?v=F3RIW0AV8co
AI Les 2 --> https://www.youtube.com/watch?v=KdQBEukytGY
https://www.nighthour.sg/articles/2017/farmer-wolf-cabbage-sheep-river-crossing-puzzle.html
https://github.com/ethanbeaver/Wolf-Goat-Cabbage-Problem/blob/master/main.py
https://favtutor.com/blogs/depth-first-search-python
https://www.educative.io/edpresso/how-to-implement-depth-first-search-in-python
"""