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
from app.helpers.decorators import token_required_student
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
            'id':student.id,
            'exp':datetime.utcnow()+timedelta(days=60)
        }, key=config_data.get('SECRET_KEY'))
        
        student_details={
                'id':student.id,
                'name':student.name,
                'clas':student.clas,
                'division':student.division,
                'email':student.email,
                'password':student.password
        }
        student.auth_token=token
        db.session.commit()
        
        response={'token':token,'student':student_details,'message':"Successfully login"}
        return response
    
    @staticmethod
    @api_time_logger
    def get_students():
        name = request.args.get('name')
        # StudentV1s_data=SMS.get_student()
        # data=SMS.serialize_student(details=StudentV1s_data)
        if name:
            students = Student.get_student(name)
        else:
            students=Student.get_student()
        return students
        # return StudentV1s_data


    @staticmethod
    @api_time_logger
    def add_students():
        
        try:
            data = request.json
            required_fields = ["name", "clas", "division", "email", "password"]

            for field in required_fields:
                if field not in data or not data[field]:
                    message=f'Missing or empty field :{field}'
                    return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value,response_status=False,
                                                    message_key=message,
                                                    data=None)
                    # print(f"Missing or empty field: {field}")
                    # return {'message': f'Missing or empty field: {field}'}, 400


            
            existing_student = Student.query.filter_by(email=data['email']).first()
            if existing_student:
                return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value,
                                        response_status=False,
                                        message_key=ResponseMessageKeys.EMAIL_ALREADY_EXISTS.value,data=None)

            

            student = Student(
                name=data['name'],
                clas=data['clas'],
                division=data['division'],
                email=data['email'],
                password=data['password']
            )
            db.session.add(student)
            db.session.commit()

            # Query the newly added student by email
            student_data = Student.query.filter_by(email=data['email']).first()
            # print("Newly added student data:", student_data)
            return send_json_response(http_status=HttpStatusCode.OK.value,
                                    response_status=True,
                                    message_key=ResponseMessageKeys.SUCCESS.value,
                                    data=dict(student_data))
        except Exception as e:
            error_message=str(e)
            return send_json_response(http_status=HttpStatusCode.INTERNAL_SERVER_ERROR.value,
                                      response_status=False,
                                      message_key=ResponseMessageKeys.FAILED.value,
                                      error=error_message)

    
    ## Get student by id
    @staticmethod
    @api_time_logger
    def get_student_by_id(id):
        

        StudentV1_data=Student.get_student_by_id(id)  
        return StudentV1_data
        # return Student_data
    
    
    @staticmethod
    @api_time_logger
    @token_required_student
    def update_student_by_id(current_student,id):
        data=request.json
        student = Student.query.filter_by(id=id).first()
        if not student:
            return {'message': 'Student not found'}, 404

        if current_student.id != student.id:
            return {'message': 'You can only update your own information'}, 403

        # Update the student information
        student=Student.update_student_by_id(student.id)
        if 'password' in data:
            student.password = data['password']

        db.session.commit()
        students=Student.get_student_by_id(id=id)
        return students
    
    @staticmethod
    @api_time_logger
    def delete_student_by_id(id):
        deleted_student=Student.delete_student_by_id(id)
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
        
            
    
    

        

        