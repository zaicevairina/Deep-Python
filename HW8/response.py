import json


class Response:

	def __init__(self, json_data):
		try:
			data = json.loads(json_data)
			self.code = data['code']
			self.text = data['text']
			self.error = data['error']
			self.th = data['th']
		except json.decoder.JSONDecodeError:
			self.code = 500
			self.text = None
			self.error = 'Server send invalid data'

	@staticmethod
	def create(code, text=None, error=None, th=None):
		request_dict = {}
		request_dict['code'] = code
		request_dict['text'] = text
		request_dict['error'] = error
		request_dict['th'] = th
		return json.dumps(request_dict) 

