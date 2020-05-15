import json


class Response:

	def __init__(self, json_data):
		try:
			data = json.loads(json_data)
			self.code = data['code']
			self.answer = data['answer']
			self.error = data['error']
		except json.decoder.JSONDecodeError:
			self.code = 500
			self.answer = None
			self.error = 'Server send invalid data'

	@staticmethod
	def create(code, answer=None, error=None):
		request_dict = {}
		request_dict['code'] = code
		request_dict['answer'] = answer
		request_dict['error'] = error
		return json.dumps(request_dict) 

