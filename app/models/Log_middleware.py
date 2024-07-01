# from app.models import base
from app import db
from datetime import datetime
class LogMiddleware(db.Model):
    
    id=db.Column(db.Integer,primary_key=True)
    request_url=db.Column(db.String)
    ip_address=db.Column(db.String)
    created_at=db.Column(db.DateTime,default=datetime.utcnow())
    
    
    