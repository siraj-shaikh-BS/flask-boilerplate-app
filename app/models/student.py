"""Contains student table definitions."""
from __future__ import annotations

from typing import Any

from app import db
from app.helpers.constants import SortingOrder
from app.models.base import Base
from flask_restful import Resource,marshal_with,fields
from flask import request
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy.ext import hybrid

studentFields={
    'sid':fields.Integer,
    'name':fields.String,
    'clas':fields.Integer,
    'email':fields.String,
    'division':fields.String
}    

class Student(db.Model):
    # __tablename__='Student Management System'
    sid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    clas=db.Column(db.Integer,nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=True)
    auth_token=db.Column(db.String,nullable=True)
    division=db.Column(db.String,nullable=False)

    def __repr__(self):
        return f"{self.name}:{self.clas}-{self.division}-{self.email}-{self.password}"
    
    
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
        data=request.json
        student=Student(name=data['name'],clas=data['clas'],division=data['division'],email=data['email'],password=data['password'])
        db.session.add(student)
        db.session.commit()
        
        students=Student.query.all()
        
        return students
    
    @classmethod
    def serialize_student(cls,details):
        data=[]
        for single_data in details:
            single_data=dict(single_data)
            single_data_obj={
                'sid':single_data['sid'],
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
    def get_student_by_id(sid):
        
        student=Student.query.filter_by(sid=sid).first()
        return student

    @staticmethod
    @marshal_with(studentFields)
    def update_student_by_id(sid):
        data=request.json
        student=Student.query.filter_by(sid=sid).first()
        # student.id=data['sid']
        student.name=data['name']
        student.clas=data['clas']
        student.division=data['division']
        student.email=data['email']
        student.password=data['password']
        db.session.commit()
        
        return student
        
    
    @staticmethod
    @marshal_with(studentFields)
    def delete_student_by_id(sid):
        student=Student.query.filter_by(sid=sid).first()
        db.session.delete(student)
        db.session.commit()
        students=Student.query.all()
        
        return students

        
    
    
    



