from protocols import Word, Message, MessageList, Protocol
from wheel_protocols import WheelGraph, forward_impl
from typing import Dict

graph = WheelGraph(17)
protocol = Protocol(graph, forward_impl)

initial_messages = graph.initial_messages()
transcript = protocol.simulate(initial_messages, 16)

def aggregate(incoming: Dict[str, Word]) -> Word:
    return sum(incoming.values(), Word())

aggregates = {vertex: [aggregate(round.incoming[vertex]) for round in transcript.rounds] for vertex in transcript.graph.vertices}
#for vertex, messages in aggregates.items():
#    print(vertex, messages)

#for round in aggregates['0']:
#    print(round)

print({vertex: messages[0] + messages[-1] for vertex, messages in aggregates.items()})

# 3 -> 2 + 1*k
# 5 -> 4 + 3*k
# 7 -> 8 + 7*k
# 9 -> 8 + 7*k
# 11 -> 32 + 31*k
# 13 -> 64 + 63*k
# 15 -> 16 + 15*k
# 17 -> 256?
# 21 -> 64?