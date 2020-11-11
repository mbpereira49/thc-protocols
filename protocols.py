from typing import List, Set, Dict, Tuple, Optional, Callable

class Graph:
    def __init__(self, vertices: List[str], edges : Dict[str, List[str]]):
        self.vertices = vertices
        self.edges = edges

# Class handling message content and its manipulation.
# A word consists of a list of strings, which we treat as 
# variables being XOR'ed.
# Example: Word(['a', 'b']) := a \oplus b
class Word:
    def __init__(self, message: List[str] = []):
        self.message = self.reduce(message)

    def __repr__(self):
        return str(self.message)
    
    # Defines the sum of two messages to be their XOR
    def __add__(self, other):
        message1 = self.message
        message2 = other.message
        union = message1 + message2
        return Word(union)
    
    # Simplify a message (consisting of XOR'ed variables) by reducing each 
    # variable to be included once or not based on the parity of its occurrences
    def reduce(self, expanded: List[str]):
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

# Wrapper class for a word (the content) and its sender/recipient
class Message:
    def __init__(self, sender: str, recipient: str, contents: Word):
        self.sender = sender
        self.recipient = recipient
        self.contents = contents

# Class to organize all the messages sent in a round.
# Contains dictionaries 'outgoing' and 'incoming' to index all 
# the messages being sent from or sent to a particular vertex
class MessageList:
    def __init__(self, graph: Graph, messages: List[Message] = []):
        self.outgoing = {vertex: {neighbor: Word() for neighbor in graph.edges[vertex]} for vertex in graph.vertices}
        self.incoming = {vertex: {neighbor: Word() for neighbor in graph.edges[vertex]} for vertex in graph.vertices}
        self.graph = graph
        self.process_messages(messages)

    def process_messages(self, messages: List[Message]):
        for message in messages:
            self.outgoing[message.sender][message.recipient] = message.contents
            self.incoming[message.recipient][message.sender] = message.contents

# Class to organize all communications sent over several rounds of a protocol
class Transcript:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.rounds: List[MessageList] = []

    def add_round(self, messages: MessageList):
        self.rounds.append(messages)

class Protocol:
    def __init__(self, graph: Graph, forward_func: Callable[[Graph, str, Dict[str, Word]], List[Message]]):
        self.graph = graph
        self.forward_func = forward_func

    # Forwards the messages for a single round using forward_func
    def _forward(self, messages: MessageList) -> MessageList:
        outgoing = MessageList(messages.graph)
        for vertex in messages.incoming:
            outgoing_messages = self.forward_func(self.graph, vertex, messages.incoming[vertex])
            outgoing.process_messages(outgoing_messages)
        
        return outgoing
    
    # Forward the messages num_rounds times
    def simulate(self, initial: MessageList, num_rounds: int) -> Transcript:
        transcript = Transcript(self.graph)
        transcript.add_round(initial)

        messages = initial
        for _ in range(num_rounds):
            messages = self._forward(messages)
            transcript.add_round(messages)
        
        return transcript