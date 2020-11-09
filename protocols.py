from typing import List, Set, Dict, Tuple, Optional, Callable

class Vertex:
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return f"Vertex('{self.name}')"
    
    def __hash__(self):
        return hash(self.name)

class Graph:
    def __init__(self, vertices: List[Vertex], edges : Dict[Vertex, List[Vertex]]):
        self.vertices = {vertex.name : vertex for vertex in vertices}
        self.edges = edges
        # reconcile vertices with vertex_dict

class Message:
    def __init__(self, message: List[str]):
        self.message = self.reduce(message)

    def __repr__(self):
        return str(self.message)
    
    def __add__(self, other):
        message1 = self.message
        message2 = other.message
        union = message1 + message2
        return Message(union)
    
    # Simplify a message (consisting of XOR'ed variables) by reducing each 
    # variable to be included once or not based on the parity of its occurrences
    def reduce(self, expanded):
        message = []
        counter = 0
        prev = ''
        for ch in sorted(expanded):
            if ch != prev:
                if counter % 2 != 0:
                    message.append(prev)
                counter = 0
            counter += 1
            prev = ch
        if counter % 2 != 0:
            message.append(prev)
        
        return message

def aggregate(messages: Dict[Vertex, Message]) -> Message:
    return sum(messages.values(), Message([]))
    
class MessageList:
    def __init__(self, messages: List[Tuple[Vertex, Vertex, Message]]):
        self.sending = dict()
        self.receiving = dict()
        self.process_messages(messages)

    def process_messages(self, messages: List[Tuple[Vertex, Vertex, Message]]):
        for sender, recipient, message in messages:
            self.add_message(self.sending, sender, recipient, message)
            self.add_message(self.receiving, recipient, sender, message)

    def add_message(self, d, index, other_party, message):
        if index not in d:
            d[index] = dict()
        d[index][other_party] = message
    
    def combine_receiving(self):
        combined = dict()
        for recipient in self.receiving:
            combined[recipient] = aggregate(self.receiving[recipient])
        
        return combined

class Transcript:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.rounds: List[MessageList] = []
        self.party_view = {vertex : [] for vertex in graph.vertices.values()}

    def add_round(self, outgoing: MessageList):
        self.rounds.append(outgoing)
        for vertex in self.graph.vertices.values():
            messages = {}
            if vertex in outgoing.receiving:
                messages = outgoing.receiving[vertex]
            self.party_view[vertex].append(messages)

class Protocol:
    def __init__(self, graph: Graph, forward_func: Callable[[Graph, Vertex, Dict[Vertex, Message]], List[Tuple[Vertex, Vertex, Message]]]):
        self.graph = graph
        self.forward_func = forward_func

    def _forward(self, incoming: MessageList) -> MessageList:
        outgoing = MessageList([])
        for vertex, messages in incoming.receiving.items():
            outgoing.process_messages(self.forward_func(self.graph, vertex, messages))
        
        return outgoing
    
    # Forward the messages num_rounds - 1 times (since the initial messages consitute a round)
    def simulate(self, initial: MessageList, num_rounds: int) -> Transcript:
        transcript = Transcript(self.graph)
        transcript.add_round(initial)

        messages = initial
        for _ in range(num_rounds - 1):
            messages = self._forward(messages)
            transcript.add_round(messages)
        
        return transcript