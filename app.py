from flask import Flask, request, jsonify
from models import db, Note
from schemas import NoteSchema
from datetime import datetime

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_database_user:flask_database_password@db:5432/flask_database'
db.init_app(app)

# Create tables before the first request is handled
with app.app_context():
    db.create_all()

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


# Create a new note
@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    errors = note_schema.validate(data)

    if errors:
        return jsonify({'message': 'Validation error', 'errors': errors}), 400

    new_note = Note(text=data['text'], due_date=data.get('due_date'))
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note created successfully'}), 201


# Get all notes
@app.route('/notes', methods=['GET'])
def get_all_notes():
    notes = Note.query.all()
    result = notes_schema.dump(notes)
    return jsonify(result)


# Get a specific note by ID
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get(note_id)
    if note:
        result = note_schema.dump(note)
        return jsonify(result)
    return jsonify({'message': 'Note not found'}), 404


# Update a note by ID
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    if note:
        data = request.get_json()
        errors = note_schema.validate(data)
        if errors:
            return jsonify({'message': 'Validation error', 'errors': errors}), 400

        note.text = data['text']
        note.due_date = data.get('due_date')
        db.session.commit()
        return jsonify({'message': 'Note updated successfully'})
    return jsonify({'message': 'Note not found'}), 404


# Delete a note by ID
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted successfully'})
    return jsonify({'message': 'Note not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
