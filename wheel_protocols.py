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
    
    def initial_messages(self):
        ORD_A = ord('a')
        message_list = MessageList(self)
        from_center = [Message('center', str(i), Word([chr(ORD_A + i)])) for i in range(self.n - 1)]
        from_center += [Message('center', str(self.n - 1), Word([chr(ORD_A + i) for i in range(self.n - 1)] + ['message']))]

        message_list.process_messages(from_center)

        for i in range(self.n):
            messages = [
                Message(str(i), str((i - 1) % self.n), Word(['x' + str(i), 'y' + str(i)])),
                Message(str(i), str((i + 1) % self.n), Word(['y' + str(i), 'z' + str(i)])),
                Message(str(i), 'center', Word(['x' + str(i), 'z' + str(i)]))
            ]
            message_list.process_messages(messages)
        
        return message_list


def forward_impl(graph: Graph, vertex: str, messages: Dict[str, Word]) -> List[Message]:
    messages_sum = sum(messages.values(), Word())

    # Return list of messages where each message is the aggregate sum message
    # except with the one it received from that neighbor subtracted
    return [Message(vertex, neighbor, messages_sum + messages[neighbor]) for neighbor in graph.edges[vertex]]