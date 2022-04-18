NB_ROT = 0
REPLACE_VALUE = "r"


def reset_nb_rot():
    global NB_ROT
    NB_ROT = 0


class AVL_Node:

    def __init__(self, value: int):
        self._value: int = value
        self._right: 'AVL_Node' = None
        self._left: 'AVL_Node' = None
        self._balance = 0

    # *************** GETTERS ***************

    def get_min(self) -> int:
        if self._left is None:
            return self._value
        return self._left.get_min()

    def get_max(self) -> int:
        if self._right is None:
            return self._value
        return self._right.get_max()

    def get_value(self) -> int:
        return self._value

    def get_left(self) -> 'AVL_Node':
        return self._left

    def get_right(self) -> 'AVL_Node':
        return self._right

    def get_the_only_sub_avl(self) -> 'AVL_Node':
        if self._left is None:
            return self._right
        return self._left

    # *************** ISERS ***************

    def is_leaf(self) -> bool:
        return self._left is None and self._right is None

    def as_only_one_sub_avl(self) -> 'AVL_Node':
        return self._right is None and self._left is not None or self._left is None and self._right is not None

    # *************** SETTERS ***************

    def set_child(self, side: str, value: 'AVL_Node') -> None:
        if side == "l":
            self._left = value
        else:
            self._right = value

    # *************** ROTATION ***************

    def rot_left(self) -> 'AVL_Node':
        # update counter rotation
        global NB_ROT
        NB_ROT += 1

        # init variables
        head: 'AVL_Node' = self._right
        tmp: 'AVL_Node' = head._left

        # swap
        head._left = self
        self._right = tmp

        # update balances
        head._left._balance = 0
        head._balance = 0
        return head

    def rot_right(self) -> 'AVL_Node':
        # update counter rotation
        global NB_ROT
        NB_ROT += 1

        # init variables
        head: 'AVL_Node' = self._left
        tmp: 'AVL_Node' = head._right

        head._right = self
        self._left = tmp

        # update balances
        head._right._balance = 0
        head._balance = 0
        return head

    # *************** BALANCE ***************

    def balance(self):
        if self._balance > 1:
            left: AVL_Node = self.get_left()

            if left._balance >= 0:
                return self.rot_right()

            self._left = left.rot_left()
            return self.rot_right()

        elif self._balance < -1:
            right: AVL_Node = self.get_right()

            if right._balance <= 0:
                return self.rot_left()

            self._right = right.rot_right()
            return self.rot_left()
        else:
            return self

    def update_balance(self, inc: int) -> 'AVL_Node':
        self._balance += inc
        if -1 <= self._balance <= 1:
            return self
        return self.balance()

    def update_balance_parent(self, child: 'AVL_Node', prev_bl: int, inc: int) -> 'AVL_Node':
        if prev_bl == 0 and prev_bl != child._balance:
            return self.update_balance(inc)
        return self

    # *************** INSERT ***************

    def insert_rec(self, value: int) -> 'AVL_Node':
        if self._value == value:
            return None

        side: str = "r"
        inc: int = -1
        child: 'AVL_Node' = self._right
        nn: 'AVL_Node'
        if value < self._value:
            side = "l"
            child = self._left
            inc = 1

        if child is None:
            self.set_child(side, AVL_Node(value))
            nn = self.update_balance(inc)
        else:
            prev_bl = child._balance
            nn = child.insert_rec(value)
            if nn is not None:
                self.set_child(side, nn)
                nn = self.update_balance_parent(child, prev_bl, inc)
        return nn

    def insert(self, value: int) -> 'AVL_Node':
        head: 'AVL_Node' = self.insert_rec(value)
        return self if head is None else head

    # *************** DELETE ***************

    def delete_the_node(self) -> 'AVL_Node':
        global REPLACE_VALUE
        nn: 'AVL_Node' = self

        if self.is_leaf():
            nn = None
        elif self.as_only_one_sub_avl():
            nn = self.get_the_only_sub_avl()
        else:
            if REPLACE_VALUE == "l":
                self._value = self._left.get_max()
                self._left = self._left.delete(self._value)
            else:
                self._value = self._right.get_min()
                self._right = self._right.delete(self._value)
        return nn

    def delete(self, value: int):

        nn: 'AVL_Node' = self
        prev_bl: int = self._balance
        if self._value == value:
            nn = self.delete_the_node()

        elif value < self._value:
            if self._left is not None:
                self._left = self._left.delete(value)
                if self._left is None:
                    self.update_balance(-1)
        else:
            if self._right is not None:
                self._right = self._right.delete(value)
                if self._left is None:
                    self.update_balance(+1)
        return nn
