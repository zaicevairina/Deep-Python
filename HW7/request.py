import json


class Request:

	def __init__(self, json_data):
		try:
			data = json.loads(json_data)
			self.method = data['method']
			self.url = data['url']
		except json.decoder.JSONDecodeError:
			self.url = None
			self.method = None

	@staticmethod
	def create(method, url):
		request_dict = {}
		request_dict['method'] = method
		request_dict['url'] = url
		return json.dumps(request_dict) 


