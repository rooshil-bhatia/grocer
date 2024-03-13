from db_instance import db
import hashlib,secrets,time
import app_constants
from sqlalchemy.sql import func
from datetime import datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    manager_approved = db.Column(db.Boolean, default=False)
    last_visited = db.Column(db.DateTime(timezone=True), server_default=func.now())


    def __init__(self,mail,pwd,role):
        self.mail = mail
        self.salt = secrets.token_hex()
        self.password = hashlib.sha256((pwd+self.salt).encode('utf-8')).hexdigest()
        self.role = role
    
    def check_pwd(self, pwd):
        if hashlib.sha256((pwd+self.salt).encode('utf-8')).hexdigest()==self.password:
            return True
        else:
            return False
    
    @staticmethod
    def create(mail,pwd,role):
        user = User.query.filter_by(mail=mail).one_or_none()
        if user:
            return None
        else:
            user = User(mail,pwd,role)
            db.session.add(user)
            db.session.commit()
            return user
    
    @staticmethod
    def get(mail,pwd):
        user = User.query.filter_by(mail=mail).one_or_none()
        if user and user.check_pwd(pwd):
            user.last_visited = func.now()
            db.session.commit()
            return user
        else:
            return None 
    
    @staticmethod
    def delete(id):
        user = User.query.filter_by(id=id).one_or_none()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        else:
            return False 

    @staticmethod
    def change_mail(new_mail,id):
        user = User.query.filter_by(id=id).one_or_none()
        other =  User.query.filter_by(mail=new_mail).one_or_none()
        if (user) and (other is None):
            user.mail = new_mail
            db.session.commit()
            return True
        else:
            return False

    @staticmethod
    def approve_manager(m_id):
        manager = User.query.filter_by(id=m_id).one_or_none()
        if manager and manager.role==app_constants.MANAGER_ID:
            manager.manager_approved = True
            db.session.commit()
            return True
        else:
            return False 
    
    @staticmethod
    def get_unapproved_managers():
        managers = db.session.query(User).filter(User.role==app_constants.MANAGER_ID, User.manager_approved==False).all()
        return managers
    
    @staticmethod
    def create_if_no_admin():
        user = User.query.filter_by(role=app_constants.ADMIN_ID).one_or_none()
        if user==None:
            user = user = User("admin","secret",app_constants.ADMIN_ID)
            db.session.add(user)
            db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    products = db.relationship('Product', backref='category',
                                lazy='dynamic')

    def __init__(self,name,description):
        self.name = name
        self.description = description
    
    @staticmethod
    def create(name,description):
        cat = Category(name,description)
        db.session.add(cat)
        db.session.commit()
    
    @staticmethod
    def edit(id,name,description):
        cat = Category.query.filter_by(id=id).one_or_none()
        if cat:
            cat.name = name
            cat.description = description
            db.session.commit()
    
    @staticmethod
    def delete(id):
        cat = Category.query.filter_by(id=id).one_or_none()
        if cat:
            db.session.delete(cat)
            db.session.commit()
    
    @staticmethod
    def get():
        cats = Category.query.all()
        return cats

class Approvals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    task = db.Column(db.Integer, default = 0)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)


    def __init__(self,cid,name,description,task):
        self.cid = cid
        self.name = name
        self.description = description
        self.task = task
    
    @staticmethod
    def create(cid,name,description,task):
        approval = Approvals(cid,name,description,task)
        db.session.add(approval)
        db.session.commit()
    
    @staticmethod
    def delete(id):
        approval = Approvals.query.filter_by(id=id).one_or_none()
        if approval:
            db.session.delete(approval)
            db.session.commit()
    
    @staticmethod
    def get():
        approvals = Approvals.query.all()
        return approvals

    @staticmethod
    def approve(id):
        approval = Approvals.query.filter_by(id=id).one_or_none()
        if approval.task==0:
            cat = Category.create(approval.name,approval.description)
        elif approval.task==-1:
            Category.delete(approval.cid)
        else:
            Category.edit(approval.cid,approval.name,approval.description)
        db.session.delete(approval)
        db.session.commit()
        return 'OK',200

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    expiry = db.Column(db.String, nullable = False)
    rate = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    catID = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'))
    units = db.Column(db.Integer, nullable=False)
    #images = db.relationship('Image', back_populates='product', cascade='all, delete-orphan',)
    added = db.Column(db.DateTime(timezone=True), server_default=func.now())


    def __init__(self,name,expiry,rate,quantity,cid,units):
        self.name = name
        self.expiry = expiry
        self.rate = rate
        self.quantity = quantity
        self.catID = cid
        self.units = units
    
    @staticmethod
    def create(name,expiry,rate,quantity,cid,units):
        p = Product(name,expiry,rate,quantity,cid,units)
        db.session.add(p)
        db.session.commit()
        return p
    
    @staticmethod
    def delete(id):
        p = Product.query.filter_by(id=id).one_or_none()
        if p:
            db.session.delete(p)
            db.session.commit()
    
    @staticmethod
    def get(id):
        p = Product.query.filter_by(catID=id).order_by(Product.added.desc()).all()
        return p
    
    @staticmethod
    def edit(id,name,expiry,rate,quantity,cid,units):
        p = Product.query.filter_by(id=id).one_or_none()
        if p:
        
            p.name = name
            p.expiry = expiry
            p.rate = rate
            p.quantity = quantity
            p.catID = cid
            p.units = units
            db.session.commit()
            db.session.delete(i)
            db.session.commit()
    
    @staticmethod
    def order(id,units):
        p = Product.query.filter_by(id=id).one_or_none()
        if p:
            p.units-=units
            db.session.commit()

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.String, nullable = False)
    mail = db.Column(db.String, nullable = False)
    added = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self,order,mail):
        self.order = order
        self.mail = mail
    
    @staticmethod
    def create(order,mail):
        o = Orders(order,mail)
        db.session.add(o)
        db.session.commit()
    
    @staticmethod
    def get(mail):
        filter_after = datetime.today() - timedelta(days = 30)
        o = Orders.query.filter_by(mail=mail).filter(Orders.added >= filter_after).all()
        return o

        