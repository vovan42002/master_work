from motor.motor_asyncio import AsyncIOMotorClient
from config import get_settings


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

app_schemas_collection = database["schemas"]
deployments_collection = database["deployments"]
