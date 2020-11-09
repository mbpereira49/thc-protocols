from protocols import Vertex, Protocol, Message, MessageList, Graph
from protocols import aggregate
from typing import List, Tuple

class WheelGraph(Graph):
    def __init__(self, n):
        self.n = n
        vertices = {f'{i}': Vertex(f'{i}') for i in range(1, n+1)}
        vertices['center'] = Vertex('center')
        edges = {vertices[f'{i}'] : [vertices[f'{j}'] for j in self._neighbors(i)] for i in range(1, n + 1)}
        edges[vertices['center']] = [vertices[f'{j}'] for j in range(1, n+1)]

        super().__init__(list(vertices.values()), edges)

    def _neighbors(self, index):
        if index == 1:
            return [self.n, 2, 'center']
        elif index == self.n:
            return [self.n-1, 1, 'center']
        else:
            return [index - 1, index + 1, 'center']

def f(graph, vertex, messages) -> List[Tuple[Vertex, Vertex, Message]]:
    total = sum([message for message in messages.values()], Message([]))

    lst = []
    for neighbor in graph.edges[vertex]:
        message = total
        if neighbor in messages:
            message = message + messages[neighbor]
        lst.append((vertex, neighbor, message))
    
    return lst

graph = WheelGraph(5)

protocol = Protocol(graph, f)

from_center = [
    (graph.vertices['center'], graph.vertices['1'], Message(['a'])),
    (graph.vertices['center'], graph.vertices['2'], Message(['b'])),
    (graph.vertices['center'], graph.vertices['3'], Message(['c'])),
    (graph.vertices['center'], graph.vertices['4'], Message(['d'])),
    (graph.vertices['center'], graph.vertices['5'], Message(['a', 'b', 'c', 'd', 'm'])),
]

from_1 = [
    (graph.vertices['1'], graph.vertices['2'], Message(['x1'])),
    (graph.vertices['1'], graph.vertices['center'], Message(['y1'])),
    (graph.vertices['1'], graph.vertices['5'], Message(['x1', 'y1']))
]
from_2 = [
    (graph.vertices['2'], graph.vertices['3'], Message(['x2'])),
    (graph.vertices['2'], graph.vertices['center'], Message(['y2'])),
    (graph.vertices['2'], graph.vertices['1'], Message(['x2', 'y2']))
]
from_3 = [
    (graph.vertices['3'], graph.vertices['4'], Message(['x3'])),
    (graph.vertices['3'], graph.vertices['center'], Message(['y3'])),
    (graph.vertices['3'], graph.vertices['2'], Message(['x3', 'y3']))
]
from_4 = [
    (graph.vertices['4'], graph.vertices['5'], Message(['x4'])),
    (graph.vertices['4'], graph.vertices['center'], Message(['y4'])),
    (graph.vertices['4'], graph.vertices['3'], Message(['x4', 'y4']))
]
from_5 = [
    (graph.vertices['5'], graph.vertices['1'], Message(['x5'])),
    (graph.vertices['5'], graph.vertices['center'], Message(['y5'])),
    (graph.vertices['5'], graph.vertices['4'], Message(['x5', 'y5']))
]
initial_messages = MessageList(from_center + from_1 + from_2 + from_3 + from_4 + from_5)

transcript = protocol.simulate(initial_messages, 6)

aggregates = {vertex.name: 
                [aggregate(view) 
                for view in party_views] 
            for vertex, party_views in transcript.party_view.items()}
total_combined = {vertex: sum(messages, Message([])) for vertex, messages in aggregates.items()}
print(total_combined)
for vertex, messages in aggregates.items():
    print(vertex, messages)

## Maybe need to fix message list so it contains every vertex in the graph whether or not it was sending/receiving. Would need graph info