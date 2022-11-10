from flask import Flask, request , jsonify;
from flask_cors import CORS
from pymongo import MongoClient
 
from flask_pymongo import PyMongo ,ObjectId
mongo = PyMongo
app=Flask(__name__)



# app.config['MONGO_URI']='mongodb+srv://kaustubh:kaustubh@cluster0.ulbupfv.mongodb.net/Frejun?retryWrites=true&w=majority'
app.config['MONGO_URI']="mongodb+srv://kaustubh:kaustubh@cluster0.j82pcow.mongodb.net/packtolus?retryWrites=true&w=majority"
mongo=PyMongo(app)

CORS(app)
db= mongo.db.users

# @app.route("/")
# def index():
#     return '<h1>Hello world</h1>'

@app.route("/api/blog/addblog",methods=["POST"])
def createPost():
   
    id = db.insert_one({
        "userName":request.json['userName'], 
        'message':request.json['message'],
        'comment':{}
    })
    print(id.inserted_id)
    return jsonify({'id':str(id.inserted_id),'msg':'message added successful'})




@app.route("/api/allBlogs",methods=["GET"])
def getPosts():
    Posts=[]
    for doc in db.find():
        Posts.append({
            "_id":str(ObjectId(doc['_id'])),
            'userName':doc['userName'],
            'message':doc['message'],
            'comment':doc['comment']
        })
    return jsonify(Posts)

@app.route("/api/Blogs",methods=["GET"])
def getPostss():
    Posts=[]
    for doc in db.find():
        Posts.append({
            "_id":str(ObjectId(doc['_id'])),
            'userName':doc['userName'],
            'message':doc['message'],
            'comment':doc['comment']
        })
    return jsonify(Posts)

@app.route('/api/blogs/<id>',methods=['GET'])
def getPost(id):
   
    post=db.find_one({'_id':ObjectId(id)})
    
    return jsonify({
             "_id":str(ObjectId(post['_id'])),
            'userName':post['userName'],
            'message':post['message'],
            'comment':post['comment']})



@app.route('/api/blog/<id>',methods=['PUT'])
def updatepost(id):

    post1=db.find_one({'_id':ObjectId(id)})
    print(len(post1['comment']))
    post1['comment'][str(len(post1['comment']))]=request.json['comment']
    post=db.update_one({'_id':ObjectId(id)},{'$set':{'comment':post1['comment']}})
    if(post):
        return jsonify({
            'posts':post1['comment'],
            'msg':'data updated'})
    else:
        return jsonify({
            'msg':'post not fond'
        })



@app.route('/blogs/<id>',methods=['DELETE'])
def deletepost(id):
   
    db.delete_one({'_id':ObjectId(id)})
    
    return jsonify({
             'msg':'delete post successfully'
             })


if __name__=='__main__':
    app.run(debug=True)
    