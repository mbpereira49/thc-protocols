from protocols import Word, Message, MessageList, Protocol
from wheel_protocols import WheelGraph, forward_others, forward_all
from typing import Dict

graph = WheelGraph(8)
protocol1 = Protocol(graph, forward_others)
protocol2 = Protocol(graph, forward_all)

from_center = [
    Message('center', '0', Word(['x0'])),
    Message('center', '1', Word(['x1'])),
    Message('center', '2', Word(['x2'])),
    Message('center', '3', Word(['x3'])),
    Message('center', '4', Word(['x4'])),
    Message('center', '5', Word(['x5'])),
    Message('center', '6', Word(['x6'])),
    Message('center', '7', Word(['x7'])),
]
from_0 = [
    Message('0', '1', Word(['a'])),
    Message('0', '4', Word(['b'])),
    Message('0', 'center', Word(['c'])),
]

initial_messages = MessageList(graph, from_center)

transcript1 = protocol1.simulate(initial_messages, 2)
transcript2 = protocol2.simulate(initial_messages, 2)

def aggregate(incoming: Dict[str, Word]) -> Word:
    return sum(incoming.values(), Word())

aggregates1 = {vertex: [aggregate(round.incoming[vertex]) for round in transcript1.rounds] for vertex in transcript1.graph.vertices}
aggregates2 = {vertex: [aggregate(round.incoming[vertex]) for round in transcript2.rounds] for vertex in transcript2.graph.vertices}

row_format = "{:7}: " + "{:<7}" * len(aggregates1['0'])
print(row_format.format("", *(range(len(aggregates1['0'])))))
for vertex, messages in aggregates1.items():
    words = [str(message) for message in messages]
    print(row_format.format(vertex, *words))

for vertex in graph.vertices:
    print(vertex, aggregates1[vertex][2], ',' , aggregates2[vertex][2])