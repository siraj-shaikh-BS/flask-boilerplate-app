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
# from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash


class StudentView(View):
    """
    Contains all student related functions
    """
    
    def create_auth_response(self,student:Student):
        """Returns student details and access token
        """
        
        token=jwt.encode({
            'id':student.sid,
            'exp':datetime.utcnow()+timedelta(days=60)
        }, key=config_data.get('SECRET_KEY'))
        
        student_details={
                'sid':student.sid,
                'name':student.name,
                'clas':student.clas,
                'division':student.division,
                'email':student.email,
                'password':student.password
        }
        student.auth_token=token
        db.session.commit()
        
        response={'token':token,'details':student_details,'message':"Successfully login"}
        return response
    
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
    
    @staticmethod
    @api_time_logger
    def login_student():
        data=request.json
        email=data['email']
        password=data['password']
        
        
        if not email or not password:
            return {'message':'Missing email or password'}
        student=Student.query.filter_by(email=email).first()
        
        if student and student.password==password:
            return StudentView().create_auth_response(student=student)
        else:
            return {'message':"Invalid email or password"}
        
            
    
    

        

        