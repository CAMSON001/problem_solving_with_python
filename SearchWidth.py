from collections import deque
from copy import deepcopy

class Node:
    def __init__(self, name=0, values=None, parent=None):
        self.name = name  # Node identifier
        self.values = values if values else deque()  # State of the node (deque)
        self.parent = parent  # Parent of the node for path reconstruction

    def __repr__(self):
        return f"Node(name={self.name}, values={list(self.values)})"

    def is_goal(self, goal_state):
        """Check if the current state matches the goal state."""
        return self.values == goal_state

def read_state(state_name):
    """Read the initial or final state provided by the user."""
    state = deque()
    print(f"Choose the {state_name} state:")
    for i in range(3):
        stack = input(f"Give the elements of the {i + 1}th stack (comma-separated): ").split(",")
        state.append(deque(stack))  # Each stack is a deque for easier operations
    return state

def bfs(init_state, final_state):
    """Breadth-first search (BFS) algorithm to find a path to the final state."""
    border = deque([Node(name=0, values=init_state)])  # Queue for nodes to explore
    visited = set()  # Set of visited states (as tuples)

    while border:
        node = border.popleft()  # Get the first node in the queue
        state_tuple = tuple(map(tuple, node.values))  # Convert to tuple for comparison

        if state_tuple in visited:
            continue  # Ignore if the state has already been visited

        visited.add(state_tuple)  # Mark the state as visited

        # Check if the current state is the final state
        if node.is_goal(final_state):
            return node  # Return the final node

        # Generate neighbor states
        for i in range(3):
            for j in range(3):
                if i != j and node.values[j]:  # Check if we can move an element from j to i
                    # Create a deep copy of the current state
                    new_values = deepcopy(node.values)
                    element = new_values[j].pop()  # Remove element from stack j
                    new_values[i].append(element)  # Add element to stack i

                    new_node = Node(name=node.name + 1, values=new_values, parent=node)  # New node

                    new_state_tuple = tuple(map(tuple, new_values))  # Convert to tuple
                    if new_state_tuple not in visited:
                        border.append(new_node)  # Add new node to the border

    return None  # No solution found

def reconstruct_path(node):
    """Reconstruct the path to the final state."""
    path = []
    while node:
        path.append(node)
        node = node.parent  # Move to the parent node
    return path[::-1]  # Return the path in order

# Reading initial and final states
print("Welcome to the GAME !!!!!")
init_state = read_state("initial")
final_state = read_state("final")

# Searching for a solution using BFS
result = bfs(init_state, final_state)

# Displaying the result
if result:
    print("Success! Found the solution:")
    path = reconstruct_path(result)
    for step in path:
        print(step)
else:
    print("No solution found.")
