# Import all the models, so that Base has them before being
# Database base class
from app.db.base_class import Base
from app.models.user import User
from app.models.item import Item
from app.models.partner import Partner
from app.models.message import ReceivedMessage, SentMessage 