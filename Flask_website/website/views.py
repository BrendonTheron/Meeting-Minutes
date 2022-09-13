from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/minutes', methods=['GET', 'POST'])
@login_required
def minutes():
    if request.method == 'POST':
        topic = request.form.get('topic')
        attendees = request.form.get('attendees')
        issue = request.form.get('issue')
        action = request.form.get('action')
        actionby = request.form.get('actionby')
        information = request.form.get('information')

        if len(topic) < 1:
            flash('Please enter the topic', category='error')
        if len(attendees) < 1:
           flash('Please enter the attendees', category='error')
        if len(issue) < 1:
           flash('Please enter who raised the issue', category='error')
        if len(action) < 1:
           flash('Please enter the action/s required', category='error')
        if len(actionby) < 1:
           flash('Please enter who actioned this', category='error')
        if len(information) < 1:
           flash('Please enter subsequent information', category='error')    
        
        else:
            new_note = Note(topic=topic, attendees=attendees, issue=issue, action=action, actionby=actionby, information=information, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Minutes added!', category='success')

    return render_template("minutes.html", user=current_user)