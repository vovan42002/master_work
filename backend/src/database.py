from motor.motor_asyncio import AsyncIOMotorClient
from config import get_settings
from beanie import init_beanie
from models import Deployment, Application


async def init_db():

    connection_string = "mongodb://{user}:{password}@{host}:{port}/{db_name}?authSource={auth_db_name}".format(
        user=get_settings().mongodb.USER,
        password=get_settings().mongodb.PASSWORD,
        host=get_settings().mongodb.HOST,
        port=get_settings().mongodb.PORT,
        db_name=get_settings().mongodb.DB_NAME,
        auth_db_name=get_settings().mongodb.AUTH_DB_NAME,
    )
    client = AsyncIOMotorClient(connection_string)
    database = client[get_settings().mongodb.DB_NAME]

    await init_beanie(
        database=database,
        document_models=[Deployment, Application],
    )
