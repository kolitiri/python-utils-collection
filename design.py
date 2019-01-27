# Message classes
class Message(object):
	def __init__(self, message):
		self.message = message

	def meets_condition(self):
		raise NotImplementedError("Please Implement this method")

class EventMgmtMessage(Message):
	@staticmethod
	def meets_condition(message):
		return message.label == "EventMgmtMessage"

class EventCreationMessage(Message):
	@staticmethod
	def meets_condition(message):
		return message.label == "EventCreationMessage"

class RacingPostMessage(Message):
	@staticmethod
	def meets_condition(message):
		return message.label == "RacingPostMessage"


# Streaming classes
class Streamer(object):
	def __init__(self, message_type):
		self.message_type = message_type

	def meets_condition(self):
		raise NotImplementedError("Please Implement this method")

	def stream(self):
		raise NotImplementedError("Please Implement this method")

class EventMgmtStreamer(Streamer):
	@staticmethod
	def meets_condition(message_type):
		return isinstance(message_type, EventMgmtMessage)

	@staticmethod
	def stream(message):
		print(f"Streaming: '{message}' to EventMgmt service")

class RacingPostStreamer(Streamer):
	@staticmethod
	def meets_condition(message_type):
		return isinstance(message_type, RacingPostMessage)

	@staticmethod
	def stream(message):
		print(f"Streaming: '{message}' to RacingPost service")

class EventCreationStreamer(Streamer):
	@staticmethod
	def meets_condition(message_type):
		return isinstance(message_type, EventCreationMessage)

	@staticmethod
	def stream(message):
		print(f"Streaming: '{message}' to EventCreation service")



# Worker classes
class Worker(object):
	def __init__(self):
		self.message = None
		self._pull_from_queue()
		self._stream()

	def _pull_from_queue(self):
		raise NotImplementedError("Please Implement this method")

	def _identify_msg(self, message):
		for msg_cls in Message.__subclasses__():
			try:
				if msg_cls.meets_condition(message):
					return msg_cls(message)
			except KeyError:
				continue

	def _stream(self):
		message_type = self._identify_msg(self.message)

		for streamer_cls in Streamer.__subclasses__():
			try:
				if streamer_cls.meets_condition(message_type):
					streamer_cls.stream(self.message.text)
			except KeyError:
				continue

class KafkaWorker(Worker):
	def _pull_from_queue(self):
		class RawMessage:
			pass
		raw_msg = RawMessage
		raw_msg.label = "RacingPostMessage"
		raw_msg.text = "I am the message"
		self.message = raw_msg




worker = KafkaWorker()





