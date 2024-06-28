"""Contains student table definitions."""
from __future__ import annotations

from typing import Any

from app import db
from app.helpers.constants import SortingOrder
from app.models.base import Base
from flask_restful import Resource,marshal_with,fields
from flask import request
from app.helpers.constants import HttpStatusCode,ResponseMessageKeys
from app.helpers.utility import send_json_response
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy.ext import hybrid

studentFields={
    'id':fields.Integer,
    'name':fields.String,
    'clas':fields.Integer,
    'email':fields.String,
    'division':fields.String
}    

class Student(Base):
    # __tablename__='Student Management System'
    __tablename__ = 'student'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name=db.Column(db.String,nullable=False)
    clas=db.Column(db.Integer,nullable=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=True)
    auth_token=db.Column(db.String,nullable=True)
    division=db.Column(db.String,nullable=False)


    
    
    @staticmethod
    @marshal_with(studentFields)
    def get_student(name=None):
        
        if name:
            students=Student.query.filter(Student.name.ilike(f"%{name}%")).all()
            # students=Student.to_dict(students)
        else:
            students=Student.query.all()
        return students
        # return students
    
    @staticmethod
    @marshal_with(studentFields)
    def add_student():
        
        try:
            response = Student.add_student()
    
            return send_json_response(http_status=HttpStatusCode.OK.value, response_status=True,
                                  message_key=ResponseMessageKeys.SUCCESS.value, data=dict(response))
        except Exception as e:
            return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value,response_status=False,message_key=ResponseMessageKeys.EMAIL_ALREADY_EXISTS.value,data=None, error=str(e))


        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'clas': self.clas,
            'division': self.division,
            'email': self.email,
            'password': self.password
        }    
    
    @staticmethod
    @marshal_with(studentFields)
    def get_student_by_id(id):
        
        student=Student.query.filter_by(id=id).first()
        return student

    @staticmethod
    @marshal_with(studentFields)
    def update_student_by_id(id):
        data=request.json
        updated_student = Student.query.filter_by(id=id).first()
        if not updated_student:
            return send_json_response(
            http_status=HttpStatusCode.BAD_REQUEST.value,
            response_status=False,
            message_key=ResponseMessageKeys.USER_NOT_EXIST.value,
            data=None
            )
        # student.id=data['id']
        updated_student.name=data.get('name',updated_student.name)
        updated_student.clas=data.get('clas',updated_student.clas)
        updated_student.division=data.get('division',updated_student.division)
        updated_student.email=data.get('email',updated_student.email)
        # updated_student.password=data['password']
        db.session.commit()
        
        return updated_student
        
    
    # @staticmethod
    # @marshal_with(studentFields)
    # def delete_student_by_id(id):
    #     student=Student.delete_student_by_id(id)
    #     return student

        
    
    
    



