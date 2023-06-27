#  Import all the necessary libraries for the algorithm
from typing import List, Tuple
import heapq

class Contact:
    """
    We create a Contact class to represent each and every contact point in our graph.
    This is usefuly in creating multiple contact that all have the same attributes.

    The Contact class has these attributes:
    - id: an integer that represents the id of the contact between a src node and a dst node
    - start - a float that represents the start time of the node
    - end - a float that represents the end time of the node
    - src - an integer that represents the source node (the current node)
    - dst - an integer that represents the destination node
    - owlt - a float that represents the 'one way light time of the node' approximate distance between nodes A and B during a contact
    - visited_n - a list to check if the neighbours of a node are visited
    - pred - a type that stores the information about the predecessor of that node
    - visited - a boolean flag that represents the information if a particular node has been visited or not
    - next - next node selected in the graph to explore
    """
    def __init__(self, id: int, start: float, end: float, src: int, dst: int, owlt: float):
        self.id = id
        self.start = start
        self.end = end
        self.src = src
        self.dst = dst
        self.owlt = owlt
        self.arr_time = float("Inf")
        self.visited_n = []
        self.pred = None
        self.visited = False
        self.next = None

def read_contacts(filename: str) -> dict:
    """
    Reads the input file one by one and stores each of the contact as a vertex in the graph.

    Args:
        input file (string): The input file for the contact plan.

    Returns:
        dict: The graph to work on the problem.
    """
    contacts = {}
    with open(filename, 'r') as f:
        for line in f:
            id, start, end, src, dst, owlt = map(float, line.strip().split())
            id = int(id)
            src = int(src)
            dst = int(dst)
            if src not in contacts:
                contacts[src] = []
            contacts[src].append(Contact(id, start, end, src, dst, owlt))
    return contacts

def dijkstra(contacts: dict, src: int, dst: int) -> Tuple[List[int], float, List[int], List[int]]:
    """
    Performs the Dijkstra algorithm on the provided graph by traversing between the src and dst in an efficient manner.

    Args:
        contacts (dictionary): The graph containing the contacts (vertices).
        src (int): The starting point (start node) of our path
        dst (int): The ending point (end node) of our path

    Returns:
        All the values are return together as a tuple

        List(int): The path from the source to destination of the individual ids of the contact between the nodes.
        float: The best arrival time of the path
        List(int): The path from the source to destination of the individual source nodes. Used to visualize the path.
        List(int): The path from the source to destination of the individual destination nodes. Used to visualize the path.
    """
    
    #  Initializing the graph. Taking the first node in the graph.
    contacts[src][0].arr_time = contacts[src][0].start

    #  Creating a heap and using the arrival times as the priority factor
    heap = [(contacts[src][0].arr_time, src)]
    
    #  Iterating until the heap is empty
    #  Here we club the procedures of both the Contact Review and Contact Selection in to a single while loop
    #  choose contact points based on min priority
    while heap:
        curr_arr_time, curr = heapq.heappop(heap)  # Taking the first element for the heap based on min priority queue
        
        
        # explore neighbours of the current node
        for contact in contacts[curr]:
            neighbour = contact.dst
            neighbour_arr_time = curr_arr_time + contact.owlt
            
            #  Choosing only the respective nodes in the neighbour and adding it to the heap
            if neighbour_arr_time < contacts[neighbour][0].arr_time:
                contacts[neighbour][0].arr_time = neighbour_arr_time
                contacts[neighbour][0].pred = contact
                contacts[neighbour][0].visited_n = contacts[curr][0].visited_n + [curr]
                heapq.heappush(heap, (neighbour_arr_time, neighbour))
            
            #  Selecting the appropriate neighbour as the next node
            if curr_arr_time < neighbour_arr_time:
                neighbour_arr_time = curr_arr_time
                contacts[neighbour][0].next = contact
        
            #  If the last node is reached, break the loop
            if curr == dst:
                break
            if curr_arr_time > contacts[curr][0].arr_time:
                continue
            contacts[curr][0].visited = True
    
    
    #  Choosing the last destination node's predecessor as the final contact
    C_fin = contacts[dst][0].pred
    
    # backtrack to find route from the source to destination
    if C_fin is None:
        return [], None, [], [] # no valid path from src to dst
    
    route = [] # to save the ids
    route_src = [] # to save the source nodes
    route_dst = [] # to save the destination nodes
    curr = dst
    while curr != src:
        pred = contacts[curr][0].pred
        route.append(pred.id)
        route_src.append(pred.src)
        route_dst.append(pred.dst)
        curr = pred.src
    route.reverse() # reversing the list to get the path
    route_src.reverse() # reversing the list to get the path
    route_dst.reverse() # reversing the list to get the path
    arr_time = contacts[dst][0].arr_time # Finding the best arrival time
    
    return route, arr_time, route_src, route_dst

def printing_path(route: List[int], route_src: List[int], route_dst: List[int], arr_time: float):
        if route:
            print("\n")
            print("----------------------------------------------------------")
            print("------------ The path of the Contact Graph is ------------")
            print("Optimal path ids:", route)
            print("--------------------------------------------- ------------")
            print("The traversal of the nodes in the path is as follows:")
            for src, dst in zip(route_src, route_dst):
                print(f"{src} -> {dst}")
            print("----------------------------------------------------------")
            print("Best arrival time:", arr_time)
            print("----------------------------------------------------------")
        else:
            print("Destination is unreachable from the source")

def main():
    """
    Calls the main algorithm which inturn calls the appron the provided graph by traversing between the src and dst in an efficient manner.

    Args:
        contacts (dictionary): The graph containing the contacts (vertices).
        src (int): The starting point (start node) of our path
        dst (int): The ending point (end node) of our path

    Returns:
        All the values are return together as a tuple

        List(int): The path from the source to destination of the individual ids of the contact between the nodes.
        float: The best arrival time of the path
        List(int): The path from the source to destination of the individual source nodes. Used to visualize the path.
        List(int): The path from the source to destination of the individual destination nodes. Used to visualize the path.
    """

    # Call the function to read the Contact plan and build a graph
    contacts = read_contacts('ContactList.txt')

    # Run the Dijkstra algorithm to find the path between the source and destination
    route, arr_time, route_src, route_dst = dijkstra(contacts, 1, 12)

    # print results of the path
    printing_path(route, route_src, route_dst, arr_time)

if __name__ == '__main__':
    main()