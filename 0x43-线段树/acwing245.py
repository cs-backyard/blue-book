def readToInt():
    return [int(n) for n in input().split()]

class TreeNode(object):
    def __init__(self, left, right, sum=0, lmax=0, rmax=0, max=0):
        self.left = left
        self.right = right
        self.sum = sum
        self.lmax = lmax
        self.rmax = rmax
        self.max = max

class SegementTree(object):
    def __init__(self, objects):
        self.nodes = [TreeNode(0, 0) for _ in range(4 * len(objects))]
        self.objects = objects

    def build(self, i, left, right):
        self.nodes[i].left = left
        self.nodes[i].right = right
        if left == right:
            self.nodes[i].sum = self.objects[left - 1]
            self.nodes[i].lmax, self.nodes[i].rmax, self.nodes[i].max = self.nodes[i].sum, self.nodes[i].sum, self.nodes[i].sum
            return
        mid = (left + right) // 2
        self.build(2 * i, left, mid)
        self.build(2 * i + 1, mid + 1, right)
        self.nodes[i].sum = self.nodes[2 * i].sum + self.nodes[2 * i + 1].sum
        self.nodes[i].lmax = max(self.nodes[2 * i].lmax, self.nodes[2 * i].sum + self.nodes[2 * i + 1].lmax)
        self.nodes[i].rmax = max(self.nodes[2 * i + 1].rmax, self.nodes[2 * i + 1].sum + self.nodes[2 * i].rmax)
        self.nodes[i].max = max(self.nodes[2 * i].max, self.nodes[2 * i + 1].max, self.nodes[2 * i].rmax + self.nodes[2 * i + 1].lmax)

    def change(self, i, x, y):
        if self.nodes[i].left == self.nodes[i].right:
            self.nodes[i].sum, self.nodes[i].lmax, self.nodes[i].rmax, self.nodes[i].max = y, y, y, y
            return
        mid = (self.nodes[i].left + self.nodes[i].right) // 2
        if x <= mid:
            self.change(2 * i, x, y)
        else:
            self.change(2 * i + 1, x, y)
        self.nodes[i].sum = self.nodes[2 * i].sum + self.nodes[2 * i + 1].sum
        self.nodes[i].lmax = max(self.nodes[2 * i].lmax, self.nodes[2 * i].sum + self.nodes[2 * i + 1].lmax)
        self.nodes[i].rmax = max(self.nodes[2 * i + 1].rmax, self.nodes[2 * i + 1].sum + self.nodes[2 * i].rmax)
        self.nodes[i].max = max(self.nodes[2 * i].max, self.nodes[2 * i + 1].max, self.nodes[2 * i].rmax + self.nodes[2 * i + 1].lmax)

    def ask(self, i, x, y):
        if x <= self.nodes[i].left and self.nodes[i].right <= y:
            return self.nodes[i]
        mid = (self.nodes[i].left + self.nodes[i].right) // 2
        ans = TreeNode(x, y)
        if mid < x:
            ans = self.ask(2 * i + 1, x, y)
        elif y <= mid:
            ans = self.ask(2 * i, x, y)
        else:
            left, right = self.ask(2 * i, x, y), self.ask(2 * i + 1, x, y)
            ans.sum = left.sum + right.sum
            ans.lmax = max(left.lmax, left.sum + right.lmax)
            ans.rmax = max(right.rmax, right.sum + left.rmax)
            ans.max = max(left.max, right.max, left.rmax + right.lmax)
        return ans

NM = readToInt()
nums = readToInt()
stree = SegementTree(nums)
stree.build(1, 1, len(nums))
for _ in range(NM[1]):
    query = readToInt()
    if query[0] == 1:
        print(stree.ask(1, min(query[1], query[2]), max(query[1], query[2])).max)
    else:
        stree.change(1, query[1], query[2])
