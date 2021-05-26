import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from typing import Optional


class TreeNode:
    def __init__(self, value: float, less=None, more=None, parent=None):
        self.value = value
        self.less = less
        self.more = more
        self.parent = parent


class Tree:
    root: Optional[TreeNode] = None

    #                                (3)
    #                    (1)                        (4)
    #
    #                                 +
    #
    #                               (3.5)
    #
    #                                ||
    #                                ||
    #                              \   /
    #
    #                                (3)
    #                    (1)                          (4)
    #
    #                                           (3.5 *added*)
    #
    #
    #    Добавляет элемепнт *value* не баллансируя дерево
    #
    def add(self, value: float):
        if self.root is None:
            self.root = TreeNode(
                value=value
            )
        current_element = self.root
        while True:
            if current_element.value == value:
                return
            if current_element.value < value:
                if current_element.more is None:
                    break
                else:
                    current_element = current_element.more
                    continue
            if current_element.value > value:
                if current_element.less is None:
                    break
                else:
                    current_element = current_element.less
                    continue
        if current_element.value < value:
            current_element.more = TreeNode(
                value=value,
                parent=current_element
            )
        else:
            current_element.less = TreeNode(
                value=value,
                parent=current_element
            )


    #
    #    Выводит, содержится ли значение *value* в дереве
    #    @return True или False
    #
    def search(self, value: float):
        if self.root is None:
            return False
        return self.search_r(value) is not None


    #
    #    Поиск узла дерева с заданным значением
    #    @return TreeNode - узел дерева с заданным значением
    #
    def search_r(self, value: float):
        current_item = self.root
        while current_item.value != value:
            if current_item.value < value:
                current_item = current_item.more
            else:
                current_item = current_item.less
            if current_item is None:
                return None
        return current_item

    #                                            (3)
    #                          (2)                                  [6 *remove*]
    #               (1)                                      (5)                             (9)
    #                                                                              (7)                 (10)
    #                                                                        (6.5)      (8)        (11)   (12)
    #                                                                  (6.3)
    #
    #                                             ||
    #                                             ||
    #                                           \   /
    #
    #                                          (3 *root*)
    #                         (2)                                   (9 *successor*)
    #              (1)                                         (7)                 (10)
    #                                                    (6.5)      (8)        (11)   (12)
    #                                              (6.3)
    #                                          (5)
    #
    #
    #
    #    Удаляет элемент со значением value
    #    Причем *successor* - большая ветка удаленного элемента становится меньшей веткой родительского элемента *root*,
    #    который был удален
    #    Меньшая ветка удаленного элемента попадает в наименьшую сторону большей ветки
    #
    def remove(self, value: float):
        element_to_remove = self.search_r(value)
        if element_to_remove is None:
            return
        root = element_to_remove.parent
        if element_to_remove.more is None:
            successor = element_to_remove.less
            if successor is not None:
                successor.parent = root
            if root is not None:
                if self.is_right_branch(element_to_remove):
                    root.more = successor
                else:
                    root.less = successor
                return
            else:
                self.root = successor
                return




        right = element_to_remove.more
        right.parent = None

        left = element_to_remove.less

        while right.less is not None:
            right = right.less
        if left is not None:
            left.parent = right
        right.less = left

        successor = right
        while successor.parent is not None:
            successor = successor.parent
        if root is not None:
            successor.parent = None
            if root.value < element_to_remove.value:
                root.more = successor
            else:
                root.less = successor
        else:
            self.root = successor

    def is_right_branch(self, node: TreeNode):
        return node.parent.value < node.value

    # FIXME не работает еще
    def balance(self):
        self.root.right = self.balance_right(self.root.right)

    def balance_right(self, node: TreeNode):
        if node.less is None:
            if node.right is not None:
                return self.balance_right(node.right)
            else:
                return node
        successor = node
        while successor.left is not None:
            successor = successor.left

        node_parent = node.parent
        node_parent.right = None
        while successor.parent != node:
            parent = successor.parent.parent

            successor.parent.parent = None
            successor = self.small_right_rotate(successor)
            parent.less = None
            current_node = successor
            while current_node.right is not None:
                current_node = current_node.right
            current_node.right = parent

            successor.parent = node
            node.right = successor
        successor.parent = node_parent
        node_parent.right = successor
        node = node_parent
        print()
        return self.balance_right(successor.right)

    #                                              (9)
    #                           (7 *node*)                     (10)
    #                   (6.5)              (8)          (11)             (12)
    #              (6.3)   (6.8)
    #
    #                                        ||
    #                                        ||
    #                                      \   /
    #
    #
    #                                      (7 *node*)
    #                          (6.5)                     (8)
    #                     (6.3)   (6.8)                       (9)
    #                                                               (10)
    #                                                          (11)       (12)
    #
    #
    #    node - узел вращения
    #    Родительский элемент передвигается вниз к наибольшему дочернему элементу
    #
    def small_right_rotate(self, node: TreeNode):
        biggest = node
        parent = node.parent
        parent.less = None
        parent.parent = None
        biggest.parent = None
        while biggest.more is not None:
            biggest = biggest.more
        parent.parent = biggest
        biggest.more = parent
        node = biggest
        while node.parent is not None:
            node = node.parent
        return node

    #
    #                                       (0.7)
    #                               (0.6)             (0.8  *node*)
    #                           (0.55)           (0.75)    (0.9)
    #
    #                                        ||
    #                                        ||
    #                                      \   /
    #
    #                                  (0.8  *node*)
    #                             (0.75)           (0.9)
    #                           (0.7)
    #                        (0.6)
    #                     (0.55)
    #
    #    node - узел вращения
    #    Родительский элемент передвигается вниз к наименьшему дочернему элементу
    #
    def small_left_rotate(self, node: TreeNode):
        smallest = node
        parent = node.parent
        parent.more = None
        smallest.parent = None
        while smallest.less is not None:
            smallest = smallest.less
        parent.parent = smallest
        smallest.less = parent
        node = smallest
        while node.parent is not None:
            node = node.parent
        return node


def test_random():
    # Random fill tree
    print("Start insertion")
    start_time_seconds = time.time()
    iteration_time = start_time_seconds
    random_fill_tree = Tree()

    element_addition = []
    # Insertion elements part
    n = 0
    while iteration_time - start_time_seconds < 60:
        random_fill_tree.add(np.random.randint(1000))
        current_time = time.time()
        element_addition.append(np.round((current_time - iteration_time) * 1000, 4))
        iteration_time = current_time
        n += 1
    print("Start searching. {0} elements added".format(n))
    start_searching_time = time.time()
    # Searching part
    for i in range(int(n / 10)):
        search = np.random.randint(1000)
        random_fill_tree.search(search)
    search_time = np.round((time.time() - start_searching_time) * 1000, 4)

    print("Start remove")
    start_remove_time = time.time()
    for i in range(int(n / 10)):
        search = np.random.randint(1000)
        random_fill_tree.remove(search)
    remove_time = np.round((time.time() - start_remove_time) * 1000, 4)

    # output
    for i in range(n - 1):
        print("Addition {0} took {1} ms".format(i, element_addition[i]))
    print("Search took: {0} ms".format(search_time))
    print("Removement took: {0} ms".format(remove_time))

    add_data = np.squeeze(element_addition)
    plt.plot(add_data)
    plt.xlabel("Addition count")
    plt.ylabel("Addition time")
    plt.show()

def test_linear_increase():
    print("Start insertion")
    start_time_seconds = time.time()
    iteration_time = start_time_seconds
    tree = Tree()

    element_addition = []
    # Insertion elements part
    n = 0
    while iteration_time - start_time_seconds < 60:
        tree.add(n)
        current_time = time.time()
        element_addition.append(np.round((current_time - iteration_time) * 1000, 4))
        iteration_time = current_time
        n += 1
    print("Start searching. {0} elements added".format(n))

    start_searching_time = time.time()
    # Searching part
    for i in range(int(n / 10)):
        search = np.random.randint(1000)
        tree.search(search)
    search_time = np.round((time.time() - start_searching_time) * 1000, 4)

    print("Start remove")
    start_remove_time = time.time()
    for i in range(int(n / 10)):
        search = np.random.randint(1000)
        tree.remove(search)
    remove_time = np.round((time.time() - start_remove_time) * 1000, 4)


    # output
    for i in range(n - 1):
        print("Addition {0} took {1} ms".format(i, element_addition[i]))

    print("Search took: {0} ms".format(search_time))
    print("Removement took: {0} ms".format(remove_time))
    add_data = np.squeeze(element_addition)
    plt.plot(add_data)
    plt.xlabel("Addition count")
    plt.ylabel("Addition time")
    plt.show()

if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    test_linear_increase()



