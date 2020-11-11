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

# for k >= 1:
# 3 -> 1*k
# 5 -> 3*k
# 7 -> 7*k
# 9 -> 7*k
# 11 -> 31*k
# 13 -> 63*k
# 15 -> 15*k