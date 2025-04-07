from flask import jsonify, request
from config import db, app
from models import *
from datetime import date, timedelta

@app.route("/users", methods=["POST", "OPTIONS"])
def user_handling():
    if request.method == "OPTIONS":
        response = jsonify({"message": "options"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorisation")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        
        return response, 200
        
    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")
        
        clean_input(password)
        
        new_user = Users(username=username, password=password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": str(e)}), 400
        
        return jsonify({"message": "Added new user successfully"}), 201
    
@app.route("/tasks/<int:user_id>", methods=["GET", "OPTIONS", "POST"])
def handle_tasks(user_id):
    if request.method == "OPTIONS":
        response = jsonify({"message": "options"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorisation")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        
        return response, 200
    
    if request.method == "POST":
        
        title = request.json.get("title")
        recurrance = request.json.get("recurrance")
        
        new_task = Recurring_Tasks(user_id=user_id, title=title, recurrance=recurrance, start_date=date.today())    
        
        try:
            db.session.add(new_task)
            db.session.commit()
            
            
        except Exception as e:
            return jsonify({"message": str(e)}), 400
        
        return jsonify({"message": "Task added successfully"}), 201
    
def assign_deadline(task_obj):
    task_recurrance = task_obj.recurrance
    task_start_date = task_obj.start_date
    
    if task_recurrance == "DAILY" or task_recurrance == "TEMP":
        return task_start_date + timedelta(days=1)

    if task_recurrance == "WEEKLY":
        return task_start_date + timedelta(days=7)
    
    if task_recurrance == "MONTHLY":
        return add_month(task_start_date)
        
    if task_recurrance == "PERMANENT":
        return add_120_years(task_start_date)
        
    
def clean_input(input):
    pass
# datetime doesn't support adding a month
def add_month(date):
    pass

# permanent deadline for the task
def add_120_years(date):
    pass

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)