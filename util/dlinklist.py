class Node:
    """节点类"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DLinkList:
    """
    双向列表类
    """
    def __init__(self):
        self._head = None

    @property
    def head(self):
        return self._head

    @property
    def is_empty(self):
        """
        是否为空
        :return:
        """
        return None == self._head

    @property
    def length(self):
        """
        链表长度
        :return:
        """
        if self.is_empty:
            return 0
        n = 1
        cur = self._head
        while None != cur.next:
            cur = cur.next
            n += 1
        return n

    @property
    def ergodic(self):
        """
        遍历链表
        :return:
        """
        if self.is_empty:
            return
            # raise ValueError('ERROR NULL')
        cur = self._head
        yield cur
        while cur.next:
            cur = cur.next
            yield cur

    def add(self, data):
        """
        在头部添加节点
        :param item:
        :return:
        """
        node = Node(data)
        if self.is_empty:
            self._head = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node

    def append(self, data):
        """
        在尾部添加节点
        :return:
        """
        if self.is_empty:
            self.add(data)
        else:
            node = Node(data)
            cur = self._head
            while None != cur.next:
                cur = cur.next
            cur.next = node
            node.prev = cur

    def insert(self, index, data):
        """
        在任意位置插入节点
        :param index:
        :param item:
        :return:
        """
        if index == 0:
            self.add(data)
        elif index+1 > self.length:
            self.append(data)
        else:
            node = Node(data)
            cur = self._head
            for i in range(index):
                pre = cur
                cur = cur.next
            pre.next = node
            node.prev = pre
            node.next = cur
            cur.prev = node

    def search(self, data):
        """
        查找节点是否存在
        :param item:
        :return:
        """
        if self.is_empty:
            raise ValueError("ERROR NULL")
        cur = self._head
        while None != cur:
            if cur.data == data:
                return True
            cur = cur.next
        return False

    def deltel(self, data):
        """删除节点元素"""
        if self.is_empty:
            raise ValueError('ERROR NULL')
        else:
            cur = self._head
            while None != cur:
                if cur.data == data:
                    if not cur.prev:  # 第一个节点
                        if None != cur.next:  # 不止一个节点
                            self._head = cur.next
                            cur.next.prev = None
                        else:  # 只有一个节点
                            self._head = None
                    else:  # 不是第一个节点
                        if cur.next == None:  # 最后一个节点
                            cur.prev.next = None
                        else:  # 中间节点
                            cur.prev.next = cur.next
                            cur.next.prev = cur.prev
                cur = cur.next

if __name__ == '__main__':
    car_list = DLinkList()
    car_list.add(4)
    car_list.add(3)
    car_list.add(2)
    car_list.add(1)
    car_list.insert(999, 35)
    print(car_list.ergodic)