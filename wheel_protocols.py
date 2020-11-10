from protocols import Protocol, Word, Message, MessageList, Graph
from typing import List, Dict, Tuple

class WheelGraph(Graph):
    def __init__(self, n):
        self.n = n
        vertices = [f'{i}' for i in range(1, n+1)] + ['center']
        edges = {f'{i}' : [f'{j}' for j in self._neighbors(i)] for i in range(1, n + 1)}
        edges['center'] = [f'{j}' for j in range(1, n+1)]

        super().__init__(vertices, edges)

    def _neighbors(self, index):
        if index == 1:
            return [self.n, 2, 'center']
        elif index == self.n:
            return [self.n-1, 1, 'center']
        else:
            return [index - 1, index + 1, 'center']

def f(graph: Graph, vertex: str, messages: Dict[str, Word]) -> List[Message]:
    messages_sum = sum(messages.values(), Word())
    
    # Return list of messages where each message is the aggregate sum message
    # except with the one it received from that neighbor subtracted
    return [Message(vertex, neighbor, messages_sum + messages[neighbor]) for neighbor in graph.edges[vertex]]

graph = WheelGraph(5)

protocol = Protocol(graph, f)

from_center = [
    Message('center', '1', Word(['a'])),
    Message('center', '2', Word(['b'])),
    Message('center', '3', Word(['c'])),
    Message('center', '4', Word(['d'])),
    Message('center', '5', Word(['a', 'b', 'c', 'd', 'm'])),
]
from_1 = [
    Message('1', '2', Word(['x1'])),
    Message('1', 'center', Word(['y1'])),
    Message('1', '5', Word(['x1', 'y1']))
]
from_2 = [
    Message('2', '3', Word(['x2'])),
    Message('2', 'center', Word(['y2'])),
    Message('2', '1', Word(['x2', 'y2']))
]
from_3 = [
    Message('3', '4', Word(['x3'])),
    Message('3', 'center', Word(['y3'])),
    Message('3', '2', Word(['x3', 'y3']))
]
from_4 = [
    Message('4', '5', Word(['x4'])),
    Message('4', 'center', Word(['y4'])),
    Message('4', '3', Word(['x4', 'y4']))
]
from_5 = [
    Message('5', '1', Word(['x5'])),
    Message('5', 'center', Word(['y5'])),
    Message('5', '4', Word(['x5', 'y5']))
]
initial_messages = MessageList(from_center + from_1 + from_2 + from_3 + from_4 + from_5, graph)

transcript = protocol.simulate(initial_messages, 6)

def aggregate(incoming: Dict[str, Word]) -> Word:
    return sum(incoming.values(), Word())

aggregates = {vertex: [aggregate(round.incoming[vertex]) for round in transcript.rounds] for vertex in transcript.graph.vertices}
total_combined = {vertex: sum(messages, Word()) for vertex, messages in aggregates.items()}
print(total_combined)
for vertex, messages in aggregates.items():
    print(vertex, messages)