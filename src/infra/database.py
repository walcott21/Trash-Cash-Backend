from src.common.models.base.singleton import Singleton
import motor.motor_tornado

# needs to be singleton to create only one DB connection
class Database(metaclass=Singleton):
    def __init__(self):
        port = 27017
        url = "localhost"
        # url = "mongodb+srv://a54190:pZ53SDOQpSxiOo7a@cluster.xaqe80g.mongodb.net/"
        self.client = motor.motor_tornado.MotorClient(url, port)