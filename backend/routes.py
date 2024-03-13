from flask import request,jsonify
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,get_jwt,verify_jwt_in_request
from functools import wraps
import json

import models,app_constants
from app_instance import app,cache

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"]==app_constants.ADMIN_ID:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper

def manager_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"]==app_constants.MANAGER_ID and claims["approved"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="managers only!"), 403

        return decorator

    return wrapper

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p><p>Hello, World!</p><p>Hello, World!</p>"

@app.post("/login")
def login():
    mail = request.json.get("mail", None)
    password = request.json.get("password", None)
    user = models.User.get(mail,password)
    if user:
        claims = {"role": user.role,"approved": user.manager_approved}
        token = create_access_token(identity=user.id, additional_claims=claims)
        return jsonify(access_token=token,role=user.role,approved = user.manager_approved)
    else:
        return 'bad credentials',455

@app.post("/register")
def register():
    mail = request.json.get("mail", None)
    password = request.json.get("password", None)
    role = request.json.get("role",None)
    user = models.User.create(mail,password,role)
    if user:
        claims = {"role": user.role,"approved": user.manager_approved}
        token = create_access_token(identity=user.id, additional_claims=claims)
        return jsonify(access_token=token,role=user.role,approved = user.manager_approved)
    else:
        return 'user exists', 456

@app.delete("/user")
@jwt_required()
def delete():
    id = get_jwt_identity()
    if models.User.delete(id):
        return 'OK',200
    else:
        return 'error', 457
    
@app.get("/categories")
def getCat():
    cats = models.Category.get()
    cats_mod = []
    for cat in cats:
        cats_mod.append({'id':cat.id,'name':cat.name,'desc':cat.description})
    return cats_mod,200

@app.post("/categories")
@admin_required()
def addCat():
    name = request.json.get("name", None)
    desc = request.json.get("description", None)
    if name:
        models.Category.create(name,desc)
    return 'OK',200

@app.put("/categories")
@admin_required()
def editCat():
    id = request.json.get("id", None)
    name = request.json.get("name", None)
    desc = request.json.get("description", None)
    if id and name:
        models.Category.edit(id,name,desc)
    return 'OK',200

@app.delete("/categories")
@admin_required()
def delCat():
    id = request.json.get("id", None)
    if id:
        models.Category.delete(id)
    return 'OK',200

@app.get("/managers")
@admin_required()
def getUnapproved():
    m = models.User.get_unapproved_managers()
    mn = []
    for a in m:
        mn.append({'id':a.id,'mail':a.mail})
    return mn,200

@app.post("/approve")
@admin_required()
def approve():
    id = request.json.get("id", None)
    if id:
        models.User.approve_manager(id)
    return 'OK',200

@app.post("/declinemanager")
@admin_required()
def declineManager():
    id = request.json.get("id", None)
    if id:
        models.User.delete(id)
    return 'OK',200

@app.post("/catapprovals")
@admin_required()
def approveCat():
    id = request.json.get("id", None)
    if id:
        models.Approvals.approve(id)
    return 'OK',200

@app.delete("/catapprovals")
@admin_required()
def deleteCat():
    id = request.json.get("id", None)
    if id:
        models.Approvals.delete(id)
    return 'OK',200

@app.get("/catapprovals")
@admin_required()
def getApprovals():
    m = models.Approvals.get()
    mn = []
    for a in m:
        if a.task==1:
            cat = models.Category.query.filter_by(id=a.cid).one_or_none()
            mn.append({'id':a.id,'cid':a.cid,'name':a.name,'description':a.description,'task':a.task,'oldname':cat.name,'olddesc':cat.description})
        else:
            mn.append({'id':a.id,'cid':a.cid,'name':a.name,'description':a.description,'task':a.task})
    return mn,200

@app.put("/catapprovals")
@manager_required()
def catchange():
    cid = request.json.get("cid", None)
    name = request.json.get("name", None)
    description = request.json.get("description", None)
    task = request.json.get("task",None)
    if name:
        models.Approvals.create(cid,name,description,task)
    return 'OK',200

@app.get("/products/<id>")
def getProd(id):
    ps = models.Product.get(id)
    ps_arr = []
    for p in ps:
        ps_arr.append({'id':p.id,'name':p.name,'expiry':p.expiry,'rate':p.rate,'quantity':p.quantity,'units':p.units,'added':p.added})
    return ps_arr,200

@app.get("/product/<id>")
def getProdSingle(id):
    p = models.Product.query.filter_by(id=id).one_or_none()
    if p:
        return {'name':p.name,'rate':p.rate}
    else:
        return 'not found',467

@app.post("/products")
@manager_required()
def addProd():
    json_data = json.loads(request.form['json'])
    name = json_data["name"]
    expiry = json_data["expiry"]
    rate = json_data["rate"]
    quantity = json_data["quantity"]
    cid = json_data["cid"]
    units = json_data["units"]
    if name is not None and expiry is not None and rate is not None and quantity is not None and cid is not None:
        p = models.Product.create(name,expiry,rate,quantity,cid,units)

        return 'OK',200
    else:
        return 'FAILED',478

@app.delete("/products")
@manager_required()
def delProd():
    id = request.json.get("id", None)
    if id:
        models.Product.delete(id)
    return 'OK',200

@app.put("/products")
@manager_required()
def editProd():
    json_data = json.loads(request.form['json'])
    id = json_data["id"]
    name = json_data["name"]
    expiry = json_data["expiry"]
    rate = json_data["rate"]
    quantity = json_data["quantity"]
    cid = json_data["cid"]
    units = json_data["units"]
    if id is not None and name is not None and expiry is not None and rate is not None and quantity is not None and cid is not None:
        models.Product.edit(id,name,expiry,rate,quantity,cid,units)
    return 'OK',200

from flask import send_file,Response



@app.post("/orders")
def postOrder():
    mail = request.json.get("mail", None)
    order = request.json.get("order", None)
    if mail is not None and order is not None:
        items = json.loads(order)
        for i in items:
            models.Product.order(i,items[i])
        models.Orders.create(order,mail)
    return 'OK',200

from app_instance import sendreport

@app.post("/productsummary")
@manager_required()
def mailProds():
    mail = request.json.get("mail", None)
    sendreport(mail)
    return 'OK',200