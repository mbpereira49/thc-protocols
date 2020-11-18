from protocols import Word, Message, MessageList, Protocol
from wheel_protocols import WheelGraph, forward_impl
from typing import Dict

graph = WheelGraph(6)
protocol = Protocol(graph, forward_impl)

from_center = [
    Message('center', '0', Word(['a'])),
    Message('center', '1', Word(['b'])),
    Message('center', '2', Word(['c'])),
    Message('center', '3', Word(['d'])),
    Message('center', '4', Word(['a', 'b', 'c', 'd'])),
]
from_0 = [
    Message('0', '1', Word(['a'])),
    #Message('0', '1', Word(['x1', 'z1'])),
    #Message('0', 'center', Word(['y1', 'z1'])),
]

initial_messages = MessageList(graph, from_0)
transcript = protocol.simulate(initial_messages, 7)

def aggregate(incoming: Dict[str, Word]) -> Word:
    return sum(incoming.values(), Word())

aggregates = {vertex: [aggregate(round.incoming[vertex]) for round in transcript.rounds] for vertex in transcript.graph.vertices}

row_format = "{:7}: " + "{:<7}" * len(aggregates['0'])
print(row_format.format("", *(range(len(aggregates['0'])))))
for vertex, messages in aggregates.items():
    words = [str(message) for message in messages]
    print(row_format.format(vertex, *words))

for vertex, messages in aggregates.items():
    print(vertex, messages[0] + messages[-1])

import numpy as np

matr = graph.adjacency_matrix
for row in matr:
    print(row)
print(np.matmul(matr, matr))