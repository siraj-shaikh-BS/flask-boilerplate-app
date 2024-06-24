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



class SMS(db.Model):
    sid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    clas=db.Column(db.Integer,nullable=False)
    division=db.Column(db.String,nullable=False)

    def __repr__(self):
        return f"{self.name}:{self.clas}-{self.division}"
    
    
    
studentFields={
    'sid':fields.Integer,
    'name':fields.String,
    'clas':fields.Integer,
    'division':fields.String
}    


# Students class
class Students(Resource):
    @marshal_with(studentFields)
    def get():
        students=SMS.query.all()
        return students
    
    @marshal_with(studentFields)
    def post():
        data=request.json
        student=SMS(name=data['name'],clas=data['clas'],division=data['division'])
        db.session.add(student)
        db.session.commit()
        
        students=SMS.query.all()
        
        return students
    
class Student(Resource):
    
    @marshal_with(studentFields)
    def get(sid):
        student=SMS.query.filter_by(sid=sid).first()
        return student


    @marshal_with(studentFields)
    def put(sid):
        data=request.json
        student=SMS.query.filter_by(sid=sid).first()
        # student.id=data['sid']
        student.name=data['name']
        student.clas=data['clas']
        student.division=data['division']
        db.session.commit()
        
        return student
        
    
    
    @marshal_with(studentFields)
    def delete(sid):
        student=SMS.query.filter_by(sid=sid).first()
        db.session.delete(student)
        db.session.commit()
        students=SMS.query.all()
        
        return students