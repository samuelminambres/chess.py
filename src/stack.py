class Node:

    def __init__(self, value, next = None):
        self.value = value
        self.next = next

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        if not isinstance(node, Node) and node is not None:
            raise TypeError("Next must be Node")
        self._next = node

    def __str__(self):
        return str(self._value)
    
    def __repr__(self):
        return f"Node(value = {self._value}, next = {self._next})"
    

class LinkedList:

    def __init__(self, value = None):
        self.head = Node(value)
        self._length = 0 if value is None else 1

    @property
    def head(self):
        return self._head
    
    @head.setter
    def head(self, node: Node):
        if not isinstance(node, Node) and node is not None:
            raise TypeError("Every value in LinkedList must be Node")
        self._head = node

    @property
    def length(self):
        return self._length
    
    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def __getitem__(self, index):
        if index < 0:
            index = self.length + index
        counter = 0
        for node in self:
            if counter == index:
                return node
            counter += 1
        raise IndexError("Index out of range")

    def __str__(self):
        list = []
        for node in self:
            list.append(node)
        result = " -> ".join(list)
        return result

    def add_head(self, value):
        node = Node(value)
        if self.is_empty():
            self.head = node
        else:
            next = self.head
            self.head = Node(value, next)
        self._length += 1

    def add_end(self, value):
        node = Node(value)
        if self.is_empty():
            self.head = node
        else:
            self[-1].next = node
            self[-1] = node
        self._length += 1

    def remove_head(self):
        if self.is_empty():
            return False
        self.head = self.head.next if self.head.next is not None else Node(None)
        self._length -= 1
        return True
    
    def remove_end(self):
        if self.is_empty():
            return False
        if self.length == 1:
            self.head = None
        else:
            self[-2].next = None
        self._length -= 1
        return True
    
    def search_element(self, value):
        for node in self:
            if node.value == value:
                return node
        return False
    
    def remove_element(self, value):
        for node in self:
            if node.next.value == value:
                node.next = node.next.next
                return True
        return False

    
    def is_empty(self):
        return self.length == 0
    

class Stack(LinkedList):

    def __init__(self, value = None):
        super().__init__(value)

    def __str__(self):
        list = []
        for node in self:
            list.append(node)
        result = "\n".join(list)
        return result

    def push(self, value):
        return super().add_head(value)

    def top(self):
        return self.head

    def pop(self):
        if self.is_empty():
            return False
        head = self.head
        super().remove_head()
        return head