from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt,current_user
from extensions import db
from models.task_model import Task
from datetime import datetime


task_bp=Blueprint('task_bp',__name__)


#  create a new task

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()

    required_fields = ['title', 'due_datetime', 'assigned_to']
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    try:
        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            due_datetime=datetime.strptime(data['due_datetime'], "%Y-%m-%dT%H:%M"),
            priority=data.get('priority', 'Medium'),
            status=data.get('status', 'To Do'),
            assigned_to=data['assigned_to'],
            assigned_by=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task created successfully"}), 201

    except ValueError as ve:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DDTHH:MM"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400






# delete a task
@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.assigned_by != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    




#  update tasksss
@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if task.assigned_by != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'due_datetime' in data:
            try:
                task.due_datetime = datetime.strptime(data['due_datetime'], "%Y-%m-%dT%H:%M")
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DDTHH:MM"}), 400
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'assigned_to' in data:
            task.assigned_to = data['assigned_to']

        db.session.commit()
        return jsonify({"message": "Task updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    




#  get alll taskssss
@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_all_tasks():
    tasks = Task.query.all()
    result = [task.to_dict() for task in tasks]
    return jsonify(result), 200




# get task by id
@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200


# get tasks assigned to current user
@task_bp.route('/tasks/assigned', methods=['GET'])
@jwt_required()
def get_assigned_tasks():
    tasks = Task.query.filter_by(assigned_to=current_user.id).all()
    result = [task.to_dict() for task in tasks]
    return jsonify(result), 200




