from protocols import Word, Message, MessageList, Protocol
from wheel_protocols import WheelGraph, forward_impl
from typing import Dict

graph = WheelGraph(5)
protocol = Protocol(graph, forward_impl)

initial_messages = graph.initial_messages()
transcript = protocol.simulate(initial_messages, 3)

def aggregate(incoming: Dict[str, Word]) -> Word:
    return sum(incoming.values(), Word())

# Add up all the messages received in a single round for a single vertex
aggregates = {vertex: [aggregate(round.incoming[vertex]) for round in transcript.rounds] for vertex in transcript.graph.vertices}

#for round in aggregates['0']:
#    print(round)

print({vertex: messages[0] + messages[-1] for vertex, messages in aggregates.items()})


# For a wheel graph with n nodes on the outside, how
# many rounds does it take for the messages passed to cancel 
# out? For k >= 1:
#       3 -> 1*k
#       5 -> 3*k
#       7 -> 7*k
#       9 -> 7*k
#       11 -> 31*k
#       13 -> 63*k
#       15 -> 15*k

# Pattern seems to follow https://oeis.org/A086839