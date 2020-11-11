from protocols import Protocol, Word, Message, MessageList, Graph
from typing import List, Dict, Tuple

class WheelGraph(Graph):
    def __init__(self, n):
        self.n = n
        vertices = [f'{i}' for i in range(n)] + ['center']
        edges = {f'{i}' : [str(j) for j in self._neighbors(i)] for i in range(n)}
        edges['center'] = [str(j) for j in range(n)]

        super().__init__(vertices, edges)

    def _neighbors(self, index):
        return [(index - 1) % self.n, (index + 1) % self.n, 'center']
    
    # Constructs a list of initial messages corresponding to the center party secret sharing
    # some message among all its neighbors, and the outside parties secret sharing the zero message
    # to its three neighbors
    def initial_messages(self):
        message_list = MessageList(self)

        # Center sends a different letter of the alphabet to all its neighbors, except for one neighbor,
        # who receives the XOR of all the other messages plus the message
        from_center = [Message('center', str(i), Word([chr(ord('a') + i)])) for i in range(self.n - 1)]
        from_center += [Message('center', str(self.n - 1), Word([chr(ord('a') + i) for i in range(self.n - 1)] + ['message']))]

        message_list.process_messages(from_center)

        for i in range(self.n):
            # Each party sends to its three neighbors the messages 
            #   [x_i + y_i], [y_i + z_i], [x_i + z_i]
            # which add up to 0 
            messages = [
                Message(str(i), str((i - 1) % self.n), Word(['x' + str(i), 'y' + str(i)])),
                Message(str(i), str((i + 1) % self.n), Word(['y' + str(i), 'z' + str(i)])),
                Message(str(i), 'center', Word(['x' + str(i), 'z' + str(i)]))
            ]
            message_list.process_messages(messages)
        
        return message_list

# Implementation of a forwarding function, corresponding to the protocol
# where each party forwards to each neighbor the sum of the messages it received
# except for the message from that neighbor
def forward_impl(graph: Graph, vertex: str, messages: Dict[str, Word]) -> List[Message]:
    messages_sum = sum(messages.values(), Word())

    # Return list of messages where each message is the aggregate sum message
    # with the one it received from that neighbor subtracted
    return [Message(vertex, neighbor, messages_sum + messages[neighbor]) for neighbor in graph.edges[vertex]]