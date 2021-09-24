from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Notes
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        note = request.form['note']

        if len(note) < 1:
            flash("The note length can't less then 1 character", category='error')
        else:
            new_note = Notes(
                note = note,
                usr_id = current_user.user_id
            )
            db.session.add(new_note)
            db.session.commit()
            flash('Note created', category='success')

    return render_template('index.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteid']
    note = Notes.query.get(int(note_id))

    if note:
        if note.usr_id == current_user.user_id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})