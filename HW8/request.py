import json


class Request:

	def __init__(self, json_data):
		try:
			data = json.loads(json_data)
			self.method = data['method']
			self.text = data['text']
		except json.decoder.JSONDecodeError:
			self.url = None
			self.method = None

	@staticmethod
	def create(method, text):
		request_dict = {}
		request_dict['method'] = method
		request_dict['text'] = text
		return json.dumps(request_dict) 


