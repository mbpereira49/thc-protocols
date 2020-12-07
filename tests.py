from protocols import Word, Message, MessageList, Protocol
from wheel_protocols import WheelGraph, forward_others, forward_all
from typing import Dict

graph = WheelGraph(5)
protocol1 = Protocol(graph, forward_others)
protocol2 = Protocol(graph, forward_all)

initial_messages = graph.initial_messages()
transcript1 = protocol1.simulate(initial_messages, 2)
transcript2 = protocol2.simulate(initial_messages, 2)

def aggregate(incoming: Dict[str, Word]) -> Word:
    return sum(incoming.values(), Word())

# Add up all the messages received in a single round for a single vertex
aggregates1 = [{vertex: aggregate(round.incoming[vertex]) for vertex in round.incoming} for round in transcript1.rounds]
aggregates2 = [{vertex: aggregate(round.incoming[vertex]) for vertex in round.incoming} for round in transcript2.rounds]

for vertex in graph.vertices:
    print(vertex, aggregates1[2][vertex], ', ', aggregates2[2][vertex])

for i, round in enumerate(transcript2.rounds):
    print(f"\nRound {i}")
    for recipient in round.incoming:
        for sender in round.incoming[recipient]:
            if round.incoming[recipient][sender].message != []:
                print("{:7} -> {:7}: {}".format(sender, recipient, round.incoming[recipient][sender]))