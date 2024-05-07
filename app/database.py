"""Contains functions to read the data from database"""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.serializer import convert_doc_list


async def get_channels_list(db: AsyncIOMotorDatabase):
	data = await db['channels'].find().to_list(100)
	return convert_doc_list(data)
