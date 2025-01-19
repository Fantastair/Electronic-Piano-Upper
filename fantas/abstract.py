from functools import cache


class NodeBase:
	# 这是一个抽象的树节点类，仅实现了对节点间的结构操作(即指针域)
	# 如何定义数据域由继承它的子类决定

	__slots__ = ['kidgroup', 'father']

	def __init__(self):
		self.kidgroup = None  # 存储孩子节点，有序，默认为None以节省空间
		self.father = None  # 存储父节点

	def append(self, node):
		# 添加node节点至最后
		if self.kidgroup is None:
			self.kidgroup = []
		if not node.is_root():
			node.leave()
		node.father = self
		self.kidgroup.append(node)

	def insert(self, node, index):
		# 插入node至index位置
		if self.kidgroup is None:
			self.kidgroup = []
		if not node.is_root():
			node.leave()
		node.father = self
		self.kidgroup.insert(index, node)

	def remove(self, node):
		# 从自己的子节点中移除node
		if self.kidgroup is None:
			self.kidgroup = []
		if node in self.kidgroup:
			self.kidgroup.remove(node)
			node.father = None

	def remove_index(self, index):
		# 移除index位置的node
		self.kidgroup.pop(index).father = None

	def join(self, node):
		# 将自己作为子节点添加至node中
		node.append(self)

	def join_to(self, node, index):
		# 添加至index位置
		node.insert(self, index)

	def leave(self):
		# 从父节点中移除
		self.father.remove(self)

	def move_to(self, n):
		# 移至位置n
		self.father.kidgroup.remove(self)
		self.father.kidgroup.insert(n, self)

	def move_up(self, n=1):
		# 上移n层(默认为1)
		self.move_to(self.get_index() + n)

	def move_down(self, n=1):
		# 下移n层(默认为1)
		self.move_to(self.get_index() - n)

	def move_top(self):
		# 移至顶部
		self.move_to(len(self.father.kidgroup))

	def move_bottom(self):
		# 移至底部
		self.move_to(0)

	def exchange(self, node):
		# 与node节点交换位置
		if self.father is not None:
			self.father.kidgroup[self.get_index()] = node
		if node.father is not None:
			node.father.kidgroup[node.get_index()] = self
		self.father, node.father = node.father, self.father
		self.kidgroup, node.kidgroup = node.kidgroup, self.kidgroup

	def get_index(self):
		# 查询自己在父节点中的位置
		return self.father.kidgroup.index(self)

	def get_degree(self):
		# 查询自己的度
		return len(self.kidgroup) if self.kidgroup is not None else 0

	def is_root(self):
		# 是否为根节点
		return self.father is None

	def is_leaf(self):
		# 是否为叶子节点
		return not self.kidgroup

	def is_branch(self):
		# 是否为分支节点(不包括根节点)
		return not self.is_root() and not self.is_leaf()

	def is_top(self):
		# 是否在顶层
		return self.father.kidgroup[-1] is self

	def is_bottom(self):
		# 是否在底层
		return self.father.kidgroup[0] is self

	def is_brother(self, node):
		# node是否为自己的兄弟节点
		return self.father is node.father

	def get_father(self, n):
		# 向上查询父节点，n层
		for s in range(n):
			self = self.father
		return self

	def get_root(self):
		# 查询根节点
		while not self.is_root():
			self = self.father
		return self

	def get_floor(self):
		# 查询当前层数
		floor = 1
		while not self.is_root():
			self = self.father
			floor += 1
		return floor

	def get_distance(self, node):
		# 查询与node的距离(层数之差)
		return abs(self.get_floor()-node.get_floor())

	def is_fathers(self, node):
		# 是否为node的父系节点(node在自己的子树上)
		# 特别的，自己也是自己的父系节点
		while node is not self:
			node = node.father
			if node is None:
				return False
		return True

	def is_kids(self, node):
		# 是否是node的子系节点(即node是否是自己的父系节点)
		return node.is_fathers(self)

	def get_depth(self):
		# 查询自己子树(包含自己)的深度
		# 注意！使用递归算法，可能会消耗较多资源
		if self.is_leaf():
			return 1
		else:
			return max([n.get_depth() for n in self.kidgroup]) + 1


class Curve:
	# 这是一个抽象的曲线基类，提供了缓存方法，也可作为y=x使用
	__slots__ = tuple()

	def calc_(self, x):
		# 用x求出y
		# 在子类里需要重写此方法以实现不同的曲线
		return x

	@cache
	def calc(self, x):
		# 启用缓存求解y
		# 外部接口
		return self.calc_(x)


import math
class FormulaCurve(Curve):
	# 单公式曲线

	__slots__ = ['formula']

	def __init__(self, formula: str):
		super().__init__()
		self.formula = formula  # formula是关于x的数学表达式，可以使用math库的函数

	def calc_(self, x):
		return eval(self.formula)


class BezierCurve(Curve):
	# 贝塞尔曲线，3阶，1段
	__slots__ = ('points', )

	def __init__(self, points):
		self.points = points

	def calc_(self, k):
		p1, p2, p3, p4 = self.points
		return p1[0]*(1-k)**3 + 3*p2[0]*k*(1-k)**2 + 3*p3[0]*k**2*(1-k) + p4[0]*k**3, p1[1]*(1-k)**3 + 3*p2[1]*k*(1-k)**2 + 3*p3[1]*k**2*(1-k) + p4[1]*k**3

'''
class SuperCurve(Curve):
	# 超级曲线(分段曲线)，可实现一系列曲线的分段整合

	__slots__ = ['curves', 'splits']

	def __init__(self, curves, splits):
		super().__init__()
		self.curves = curves  # 存储曲线
		self.splits = (0,) + splits + (1,)  # 划分定义域

	def calc_(self, x):
		# 基于二分查找快速确定定义域并求值
		i, j = 0, len(self.splits)-1
		while i != j-1:
			m = (i+j)//2
			if x < self.splits[m]:
				j = m
			else:
				i = m
		return self.curves[i].calc(x)
'''


# 数字运算函数
add = lambda a,b:a+b
sub = lambda a,b:a-b
mul = lambda a,b:a*b
div = lambda a,b:a/b
mod = lambda a,b:a%b
fld = lambda a,b:a//b

# 元组运算，operation是数字运算的函数
def tuple_operate(t1, t2, operation):
	return tuple(map(operation, t1, t2))

def tuple_int_operate(t, i, operation):
	return tuple([operation(s,i) for s in t])
