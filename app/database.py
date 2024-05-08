"""Contains functions to read the data from database"""

import time

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas import Message
from app.serializer import convert_doc_list
from app.utils import generate_random_user_name


async def get_channels_list(db: AsyncIOMotorDatabase):
	data = await db['channels'].find().to_list(100)
	return convert_doc_list(data)


def get_messages_mock() -> list[Message]:
	return [
		{
			"author": generate_random_user_name(),
			"content": "Hi guys, I'm back from my vacation",
			"timestamp": time.time()
		},
		{
			"author": generate_random_user_name(),
			"content": "Good to have you back! I hope you enjoyed your vacation.",
			"timestamp": time.time()
		},
		{
			"author": generate_random_user_name(),
			"content": "Yeah, I'd like to visit Italy someday.",
			"timestamp": time.time()
		}
	]