from protocols import Word, Message, MessageList, Protocol
from wheel_protocols import WheelGraph, forward_impl
from typing import Dict


graph = WheelGraph(5)
protocol = Protocol(graph, forward_impl)

from_center = [
    Message('center', '0', Word(['a'])),
    Message('center', '1', Word(['b'])),
    Message('center', '2', Word(['c'])),
    Message('center', '3', Word(['d'])),
    Message('center', '4', Word(['a', 'b', 'c', 'd', 'm'])),
]
from_0 = [
    Message('0', '4', Word(['x1', 'y1'])),
    Message('0', '1', Word(['x1', 'z1'])),
    Message('0', 'center', Word(['y1', 'z1'])),
]

initial_messages = MessageList(graph, from_center + from_0)
transcript = protocol.simulate(initial_messages, 4)

def aggregate(incoming: Dict[str, Word]) -> Word:
    return sum(incoming.values(), Word())

aggregates = {vertex: [aggregate(round.incoming[vertex]) for round in transcript.rounds] for vertex in transcript.graph.vertices}
for vertex, messages in aggregates.items():
    print(vertex, messages)

print({vertex: messages[0] + messages[-1] for vertex, messages in aggregates.items()})

# 5 -> 4
# 7 -> 8
# 9 -> 8, 15
# 11 -> 32
# 13 -> 64