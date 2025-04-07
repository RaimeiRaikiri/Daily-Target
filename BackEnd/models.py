from config import db

class Users(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=False)
    password = db.Column(db.String(120), nullable=False, unique=False)
    
    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }
        
class Recurring_Tasks(db.Model):
    __tablename__ = "recurring_tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("Users", backref=db.backref("users", uselist=False))
    title = db.Column(db.String(500), nullable=True, unique=True)
    recurrance = db.Column(db.Enum, nullable=False, unique=False)
    start_date = db.Column(db.DATE, nullable=False, unique=False)
    
    def to_json(self):
        return {
            "id": self.id,
            "userID": self.user_id,
            "title": self.title,
            "recurrance": self.recurrance,
            "startDate": self.start_date
        }
        
class Task_Completions(db.Model):
    __tablename__ = "task_completions"
    
    id =  db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForiegnKey("recurring_tasks.id"))
    recurring_tasks = db.relationship("Recurring_Tasks", backref=db.backref("recurring_tasks", uselist=False))
    deadline = db.Column(db.DATE, nullable=False, unique=False)
    completed = db.Column(db.Boolean, nullable=False, unqiue=False)
    
    def to_json(self):
        return {
            "id": self.id,
            "taskID": self.task_id,
            "deadline": self.deadline,
            "completed": self.completed
        }