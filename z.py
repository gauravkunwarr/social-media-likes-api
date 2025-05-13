from flask import Flask, request, jsonify
import flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite://social.db'
db=SQLAlchemy(app)

class Post(db.Model):
    id=db.Column(db.Integer, Primary_key=True)
    post_str_id=db.Column(db.String,unique=True,nullable=False)
    content=db.Column(db.String,nullable=False)
    create_at=db.Column(db.DateTime,default=datetime.utcnow)

class Like(db.Model):
    id=id.Column(db.Integer,primary_key=True)
    post_id=db.Column(db.Integer, db.foreignKey('post.id'),nullable=False)
    used_id=db.Column(db.String,nullable=False)
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__=(db.UniqueConstraint('post_id','user_id'),)

with app.app_context():
    db.create_all()




@app.route("/posts",methods=["POST"])
def create_post():
    data=request.json
    post=Post(post_str_id=data["post-str_id"],content=data["content"])
    db.session.add(post)
    db.session.commit()
    return jsonify({"post_str_id":post.post_str_id,"status":"created"})

@app.route("/posts/<poststr_id>/like",methods=["POST"])
def like_post(post_str_id):
    data=request.json
    post=Post.query.filter_by(post_str_id=post_str_id).first()
    if not post:
        return "Post not found",404
    if Like.query.filter_by(post_id=post.id,user_id=data["user_id_str"]).first():
        return jsonify({"status":"already_liked"})
    like=Like(post_id=post.id, user_id=data["user_id_str"])
    db.session.add(like)
    db.session.commit()
    return jsonify({"status":"liked"})

@app.route("/posts/<post_str_id>/like",methods=[DELETE])
def unlike_post(post_str_id):
    data=request.json
    post=Post.query.filter_by(post_str_id=post_str_id).first()
    if not post:
        return "Post not found",404
    like=Like.query.filter_by(post_id=post.id,user_id=data["user_id_str"]).first()
    if not like:
        return jsonify({"status":"not_liked_previously"})
    db.session.delete(like)
    db.session.commit()
    return jsonify({"status":"unliked"})

@app.route("/post/top",methods=["GET"])
def top

