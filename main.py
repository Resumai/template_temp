from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, NumberRange, Length
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oeivh098rewpoiervoiAH[roifnoviahfd]'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)