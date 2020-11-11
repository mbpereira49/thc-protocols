from protocols import Word, Message, MessageList, Protocol
from wheel_protocols import WheelGraph, forward_impl
from typing import Dict

graph = WheelGraph(5)
protocol = Protocol(graph, forward_impl)

initial_messages = graph.initial_messages()
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
# 15 -> ??