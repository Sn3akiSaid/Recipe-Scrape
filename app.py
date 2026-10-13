from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # /// - relative path
db = SQLAlchemy(app)


class Todo(db.Model):
    # initialize the object
    def __init__(self, content):
        self.content = content

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    # Every time a new element is made it will return Task and id of that task that's been created
    def __repr__(self):
        return f"<Task {self.id}>"


@app.route("/", methods=["POST", "GET"])
# python decorator - decorate or add functionality to function we will add
# Can also send data to db
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was an issue adding your task: {e}"
    else:
        # Looks at db contents in order of when they were created and return all
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
