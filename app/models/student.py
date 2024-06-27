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

    # def __repr__(self):
    #     return f"{self.name}:{self.clas}-{self.division}-{self.email}-{self.password}"
    
    
    @staticmethod
    @marshal_with(studentFields)
    def get_student(name=None):
        
        if name:
            students=Student.query.filter(Student.name.ilike(f"%{name}%")).all()
        else:
            students=Student.query.all()
        return students
        # return students
    
    @staticmethod
    @marshal_with(studentFields)
    def add_student():
        
        try:
            response = Student.add_student()
    
            return send_json_response(http_status=HttpStatusCode.BAD_REQUEST.value, response_status=True,
                                  message_key=ResponseMessageKeys.SUCCESS.value, data=dict(response))
        except Exception as e:
            return send_json_response(http_status=500,response_status=False,message_key=ResponseMessageKeys.EMAIL_ALREADY_EXISTS.value,data=None, error=str(e))


    
    @classmethod
    def serialize_student(cls,details):
        data=[]
        for single_data in details:
            single_data=dict(single_data)
            single_data_obj={
                'id':single_data['id'],
                'name':single_data['name'],
                'clas':single_data['clas'],
                'division':single_data['division'],
                'email':single_data['email'],
                'password':single_data['password']
            }
            
            data.append(single_data_obj)
        return data
        
    
    @staticmethod
    @marshal_with(studentFields)
    def get_student_by_id(id):
        
        student=Student.query.filter_by(id=id).first()
        return student

    @staticmethod
    @marshal_with(studentFields)
    def update_student_by_id(id):
        data=request.json
        student=Student.query.filter_by(id=id).first()
        # student.id=data['id']
        student.name=data['name']
        student.clas=data['clas']
        student.division=data['division']
        student.email=data['email']
        student.password=data['password']
        db.session.commit()
        
        return student
        
    
    @staticmethod
    @marshal_with(studentFields)
    def delete_student_by_id(id):
        student=Student.query.filter_by(id=id).first()
        db.session.delete(student)
        db.session.commit()
        students=Student.query.all()
        
        return students

        
    
    
    



