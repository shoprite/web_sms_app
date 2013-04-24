from models import Message, Model
from datetime import datetime
import random


class MessageFactory():
	def create(self):
		new_message = Message()
		new_message.customer_number = '1234567890'
		new_message.product_code = str(random.randrange(100, 999))
		new_message.shop_code = '123'
		new_message.timestamp = datetime.now()
		new_message.notified = False
		return new_message