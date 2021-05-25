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
        return self.search_r(self.root, value) is not None


    #
    #    Рекурсивный поиск узла дерева с заданным значением
    #    @return TreeNode - узел дерева с заданным значением
    #
    def search_r(self, item: TreeNode, value: float):
        if item.value == value:
            return item
        if (item.more is None and item.value < value) or (item.less is None and item.value > value):
            return None
        if item.value < value:
            return self.search_r(item.more, value)
        else:
            return self.search_r(item.less, value)

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
        element_to_remove = self.search_r(self.root, value)
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


    # def remove(self, value: float):
    #     element_to_remove = self.search_r(self.root, value)
    #     successor = self.generate_successor(element_to_remove)
    #     successor.less = element_to_remove.less
    #     successor.parent = element_to_remove.parent

    # def generate_successor(self, node: TreeNode):
    #     if node.more is None:
    #         node.less.parent = None
    #         return node.less
    #     current_node = node.more
    #     current_node.parent = None
    #     while current_node.less is not None:
    #         current_node = current_node.less
    #     return self.rotate_subtree(current_node)

    def rotate_subtree(self, node: TreeNode):
        root = node
        while root.parent is not None:
            root = root.parent
        while True:
            root = self.small_right_rotate(root.less)
            if root == node:
                return root


    # FIXME не работает еще
    def balance(self):
        right = self.root.more
        # while right.less is not None:
        #     right = right.less

        left = self.root.less
        # while left.more is not None:
        #     left = left.more

        while True:
            right = self.small_right_rotate(right)
            if right == self:
                break
        while True:
            left = self.small_left_rotate(left)
            if left == self:
                break
        self.root.more = right
        self.root.less = left

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


if __name__ == "__main__":
    tree = Tree()
    tree.add(3)
    tree.add(4)
    tree.add(1)
    tree.add(2)
    tree.add(3.5)
    tree.add(5)
    tree.add(1.5)

    print(tree.search(3))
    tree.remove(3)
    tree.remove(4)
    print(tree.search(3))

    # tree.add(3)
    # tree.add(2)
    # tree.add(6)
    # tree.add(1)
    # tree.add(1.5)
    # tree.add(0.5)
    # tree.add(0.7)
    # tree.add(0.3)
    # tree.add(0.6)
    # tree.add(0.8)
    # tree.add(0.55)
    # tree.add(0.75)
    # tree.add(0.9)
    #
    # tree.add(9)
    # tree.add(7)
    # tree.add(10)
    # tree.add(5)
    # tree.add(8)
    # tree.add(6.5)
    # tree.add(6.3)
    # tree.add(6.8)
    # tree.add(11)
    # tree.add(12)
    # tree.balance()
    # a = tree.generate_successor(tree.search_r(tree.root, 6))
    # print(a)
