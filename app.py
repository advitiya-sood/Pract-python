from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)


class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    time_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id
     




@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="GET":
        tasks=Todo.query.order_by(Todo.time_created).all()
        return render_template('index.html',tasks=tasks)

    else:
        content_entered=request.form['content']
        new_task= Todo(content=content_entered)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return "There was an issue"






@app.route('/delete/<int:task_id>')
def delete(task_id):
    task_to_delete= Todo.query.get_or_404(task_id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return "there was an error "
    




@app.route('/update/<int:task_id>',methods=['GET','POST'])
def update(task_id):
    task_to_update= Todo.query.get_or_404(task_id)

    if request.method=="GET":
        return render_template('update.html',task=task_to_update)
    else:
        task_to_update.content=request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "some error occured updating"





if __name__=="__main__":
    app.run(debug=True)