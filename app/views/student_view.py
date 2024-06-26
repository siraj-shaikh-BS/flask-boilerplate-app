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
from app.models.student import Student
from flask import request
from flask.views import View
import jwt
from werkzeug.security import check_password_hash


class StudentView(View):
    """
    Contains all student related functions
    """
    @staticmethod
    @api_time_logger
    def get_students():
        name = request.args.get('name')
        # Students_data=SMS.get_student()
        # data=SMS.serialize_student(details=Students_data)
        if name:
            students = Student.get_student(name)
        else:
            students=Student.get_student()
        return students
        # return Students_data

    @staticmethod
    @api_time_logger
    def add_students():
        
        students_add=Student.add_student()
        return students_add
    
    ## Get student by id
    @staticmethod
    @api_time_logger
    def get_student_by_id(sid):
        

        Student_data=Student.get_student_by_id(sid)  
        return Student_data
        # return Student_data
    
    
    @staticmethod
    @api_time_logger
    def update_student_by_id(sid):
        updated_student=Student.update_student_by_id(sid)
        return updated_student
    
    @staticmethod
    @api_time_logger
    def delete_student_by_id(sid):
        deleted_student=Student.delete_student_by_id(sid)
        Students_data=Student.get_student()
        return Students_data
    
    
    # @staticmethod
    # @api_time_logger
    # def search_student():
    #     data=request.args
    #     query=SMS.search_student_by_name(name=data['name'])
    #     data=SMS.serialize_student(details=query)
    #     return data

        

        