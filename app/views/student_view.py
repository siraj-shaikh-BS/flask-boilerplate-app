"""Contains user related API definitions."""
from datetime import datetime
from datetime import timedelta
from typing import Any

from app import config_data
from app import db
from app import logger
from app.helpers.constants import HttpStatusCode
from app.helpers.constants import ResponseMessageKeys
from app.helpers.decorators import api_time_logger
from app.helpers.decorators import token_required
from app.helpers.utility import field_type_validator
from app.helpers.utility import get_pagination_meta
from app.helpers.utility import required_validator
from app.helpers.utility import send_json_response
from app.models.student import Students,SMS,Student
from flask import request
from flask.views import View
import jwt
from werkzeug.security import check_password_hash


class StudentsView(View):
    """Contains all user related functions"""
    
    @staticmethod
    @api_time_logger
    def get_students():
        """
        
        
        """

        # print(request)
        Students_data=Students.get()
        
        
        # import pdb;pdb.set_trace()
        
        return Students_data

    @staticmethod
    @api_time_logger
    def add_student():
        
        students_add=Students.post()
        return students_add
    
    ## Get student by id
    @staticmethod
    @api_time_logger
    def get_student_by_id(sid):

        Student_data=Student.get(sid)        
        return Student_data
    
    @staticmethod
    @api_time_logger
    def update_student_by_id(sid):
        updated_student=Student.put(sid)
        return updated_student
    
    @staticmethod
    @api_time_logger
    def delete_student_by_id(sid):
        deleted_student=Student.delete(sid)
        return deleted_student

class StudentView(View):
    """Contains all user related functions"""

    @staticmethod
    @api_time_logger
    def add_student():
        
        student_add=Student.put()
        return student_add
        
        
    
    
# api.add_resource('/')
        