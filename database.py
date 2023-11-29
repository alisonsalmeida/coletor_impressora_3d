from motor.motor_asyncio import AsyncIOMotorClient


class StorageInterface:
    def __init__(self):
        self.client = AsyncIOMotorClient(
            host="192.168.100.63",
            port=27018,
            username='shell-manager-user',
            password='743bce6144f65c117b7673bc6787db01'
        )

        self.database = self.client.database_collect

    async def init(self):
        pass

    async def _insert_data(self, collection: str, data: dict):
        await self.database[collection].insert_one(data)

    async def insert_data(self, data: dict):
        await self._insert_data('data_collects', data)

    async def create_collect(self, data: dict):
        await self._insert_data('collects', data)
