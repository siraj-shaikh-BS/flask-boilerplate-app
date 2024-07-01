from typing import Any
from flask import Flask,Request
import logging
from app.models.Log_middleware import LogMiddleware
from logging.handlers import RotatingFileHandler
from datetime import datetime
from app import db


class Log_Middleware:
    
    def __init__(self,app):
        self.app=app
        # self.logger=logging.getLogger('request_logger')
        # self.logger.setLevel(logging.INFO)
        # handler=RotatingFileHandler("request.log",maxBytes=10000,backupCount=1)
        # self.logger.addHandler(handler)
    
    def __call__(self, environment, start_response):
        request=Request(environment)
        
        request_data={
            'request_url':request.url,
            'ip_address':request.remote_addr,
            'created_at':datetime.utcnow()
        }
        log_entry=LogMiddleware(**request_data)
        db.session.add(log_entry)
        db.session.commit()
        
        return self.app(environment,start_response)
    
        
        