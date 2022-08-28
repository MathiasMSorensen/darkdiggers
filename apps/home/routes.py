# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
# from flask_login import login_required
from jinja2 import TemplateNotFound
from utils.azure_data_utils.azure_table_utils import get_dasboard_data
from wtforms import SelectField, StringField, PasswordField, BooleanField, IntegerField, validators
from wtforms.validators import InputRequired , Email, Length, NumberRange
from flask_wtf import FlaskForm

table_name = "czlhjpfh3vckarxvmaa8"

class Form(FlaskForm):
    Budget = IntegerField('How Many?', 
                          validators=[NumberRange(min=0, max=150, message='bla')],
                          )

# @login_required
@blueprint.route('/index')
def index():
    preds_labels, preds, writeback_labels,\
    writeback, total_predictions, total_writebacks, \
    accurazy_labels, accurazy, last_call, last_writeback, total_accurazy = get_dasboard_data(table_name)

    return render_template('home/index.html', 
                            preds_labels = preds_labels, preds = preds, writeback_labels = writeback_labels,
                            writeback = writeback, total_predictions = total_predictions, total_writebacks = total_writebacks, 
                            accurazy_labels = accurazy_labels, accurazy = accurazy, last_call = last_call, last_writeback =last_writeback,
                            total_accurazy = total_accurazy, 
                            segment='index')


@blueprint.route('tables')
def tables():
    form = Form()

    return render_template("home/tables.html", form=form, segment='tables')



@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
