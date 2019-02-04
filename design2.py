import re

# Data type classes
class DataTypeHandler(object):
	def __init__(self, source_id, root, feeddoc):
		self.source_id = source_id
		self.feeddoc = feeddoc
		self.root = root
		self.parent_identifier = None

	def meets_condition(self):
		raise NotImplementedError("Please Implement this method")

	def get_feeddoc_id(self):
		return source_id.split(':')[-1]

	def get_parent(self):
		if not self.parent_identifier:
			return

		parent_node = self.feeddoc[self.root]['parent']
		for m in parent_node.split(','):
			if re.match(self.parent_identifier, m):
				return m.split(':')[-1]


class EventHandler(DataTypeHandler):
	def __init__(self, source_id, root, feeddoc):
		super(EventHandler, self).__init__(source_id, root, feeddoc)
		self.parent_identifier = 't:'

	@staticmethod
	def meets_condition(root):
		return root == "event"


class MarketHandler(DataTypeHandler):
	def __init__(self, source_id, root, feeddoc):
		super(MarketHandler, self).__init__(source_id, root, feeddoc)
		self.parent_identifier = 'e:'

	@staticmethod
	def meets_condition(root):
		return root == "market"


class SelectionHandler(DataTypeHandler):
	def __init__(self, source_id, root, feeddoc):
		super(SelectionHandler, self).__init__(source_id, root, feeddoc)
		self.parent_identifier = 'm:'

	@staticmethod
	def meets_condition(root):
		return root == "selection"


class Consumer(object):
	def __init__(self):
		self.root = None

	def _preprocess_message(self, root, source_id, feeddoc):
		for handler_cls in DataTypeHandler.__subclasses__():
			try:
				if handler_cls.meets_condition(root):
					handler = handler_cls(source_id, root, feeddoc)

					parent = handler.get_parent()
					if parent:
						print("Handler: {}, parent: {}".format(handler, handler.get_parent()))
					else:
						print("Parent not found")
			except KeyError:
				continue


eventfeeddoc = {
	'event': {
		'parent': 'c:1,cl:2,t:3',
		'id': 4
	},
	'_id': 4
}
marketfeeddoc = {
	'market': {
		'parent': 'c:1,cl:2,t:3,e:4',
		'id': 5
	},
	'_id': 4
}
selectionfeeddoc = {
	'selection': {
		'parent': 'c:1,cl:2,t:3,e:4,m:5',
		'id': 6
	},
	'_id': 4
}
root = "event"
source_id = "LCF:12345"
consumer = Consumer()
consumer._preprocess_message(root, source_id, eventfeeddoc)







