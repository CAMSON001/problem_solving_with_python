from collections import deque

class State:
    def __init__(self, boxes):
        self.boxes = boxes  # boxes est une liste de listes représentant les cubes dans chaque boîte

    def is_goal(self, goal_state):
        return self.boxes == goal_state

    def get_neighbors(self):
        neighbors = []
        # Boucle à travers les boîtes pour effectuer des mouvements
        for i in range(len(self.boxes)):
            if self.boxes[i]:  # Vérifier si la boîte i n'est pas vide
                # Prendre le cube du haut de la boîte i
                cube_to_move = self.boxes[i][-1]  # Le cube du haut

                for j in range(len(self.boxes)):
                    if i != j:  # Ne pas se déplacer dans la même boîte
                        # Créer un nouvel état en déplaçant le cube
                        new_boxes = [box[:] for box in self.boxes]  # Copier l'état actuel des boîtes
                        new_boxes[i].pop()  # Retirer le cube du haut de la boîte i
                        new_boxes[j].append(cube_to_move)  # Ajouter le cube au haut de la boîte j
                        neighbors.append(State(new_boxes))
        
        return neighbors

def bfs(initial_state, goal_state):
    queue = deque([initial_state])
    visited = set()
    
    """ final_queu = list()
    for state in queue :
        state_boxes = tuple(tuple(boxq)for boxq in state.boxes)
        final_queu.append(state_boxes)
    final_queu = tuple(final_queu)   """

    while queue:
        current_state = queue.popleft()
        print(current_state.boxes)
        if current_state.is_goal(goal_state):
            return current_state.boxes  # Retourner l'état final trouvé

        for neighbor in current_state.get_neighbors():
            # Convertir la liste de boîtes en un tuple pour l'ajouter à visited
            state_tuple = tuple(tuple(box) for box in neighbor.boxes)
            if state_tuple not in visited :
                visited.add(state_tuple)
                queue.append(neighbor)
            """  if state_tuple not in final_queu : """
               
                

    return None  # Aucune solution trouvée

# Exemple d'utilisation
initial_state = State([['B', 'A'], ['C'], []])  # 3 cubes dans la première boîte
goal_state = [[], [], ['B','C','A']]  # État final souhaité

result = bfs(initial_state, goal_state)
if result:
    print(f"État final atteint: {result}")
else:
    print("Aucune solution trouvée.")
