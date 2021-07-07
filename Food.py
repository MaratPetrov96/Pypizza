from admin_ import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/') #главная страница
def main():
    ip=request.remote_addr
    cur=Visitor.query.filter_by(ip=ip).first()
    if not cur:
        s=0
    else:
        s=sum([i.price for i in cur.order])
    return render_template('FoodMain.html',cur=current_user,kinds=Kind.query.all(),summ=s)

@app.route('/<int:kind_id>') #меню отдельного раздела
def menu(kind_id):
    ip=request.remote_addr
    cur=Visitor.query.filter_by(ip=ip).first()
    if not cur:
        s=0
    else:
        s=sum([i.price for i in cur.order])
    return render_template('FoodMenu.html',cur=current_user,data=Food.query.filter_by(
        kind_id=kind_id).all(),kinds=Kind.query.all(),summ=s,k=Kind.query.get(kind_id))

@app.route('/<int:food_id>/add',methods=['POST']) #добавление в корзину
def add_to_busket(food_id):
    ip=request.remote_addr
    if ip not in db.session.query().with_entities(Visitor.ip).all():
        db.session.add(Visitor(ip=ip))
    Visitor.query.filter_by(ip=ip).first().order.append(Food.query.get(
        food_id))
    db.session.commit()
    return request.referrer

@app.route('/busket') #корзина
def busket():
    ip=request.remote_addr
    if ip not in db.session.query().with_entities(Visitor.ip).all():
        db.session.add(Visitor(ip=ip))
        db.session.commit()
    cur=Visitor.query.filter_by(ip=ip).first()
    s=sum([i.price for i in cur.order])
    return render_template('FoodBusket.html',cur=current_user,data=Visitor.query.filter_by
                           (ip=ip).first().order,summ=s,kinds=Kind.query.all())

@app.route('/order',methods=['POST']) #заказ
def order():
    user=Visitor.query.filter_by(ip=ip).first()
    new=Order(s=sum([i.price for i in user.order]))
    new.order.extend(user.order)
    db.session.add(new)
    Visitor.query.delete(user)
    db.session.commit()
    form=request.form
    m=Message('New order',sender=admin_mail[0],recipients=admin_mail) #письмо с заказом
    m.html=render_template('FoodLetter.html',adres=form['address'],order=new.order,
                    phone=form['phone'],info=form['info'])
    m.text=render_template('FoodLetter.txt',adres=form['address'],order=new.order,
                    phone=form['phone'],info=form['info'])
    with app.app_context():
        mail.send(m)
    return redirect('/')

@app.route('/<int:id_>/from_busket',methods=['POST']) #удаление товара из корзины
def from_busket(id_):
    ip=request.remote_addr
    cur=Visitor.query.filter_by(ip=ip).first()
    cur.order.remove(Food.query.get(id_))
    db.session.commit()
    return render_template('FoodBusket.html',cur.order,summ=s,kinds=Kind.query.all())

@app.route('/login',methods=['GET', 'POST']) #авторизация
def login():
    if request.method=='POST':
        login_=request.form.get('login')
        password=request.form.get('password')
        if login_ and password:
            user=User.query.filter_by(name=login_).first()
            try:
                user.password
            except:
                return flash('Error')
            else:
                if check_password_hash(user.password,password):
                    login_user(user,remember=True)
                    return redirect('/admin')
                else:
                    flash('Error')
        flash('Fill both fields')
    return render_template('UniversalLogin.html',title='Вход',user_=current_user)

@app.route('/logout') #выход из аккаунта
def logout():
    logout_user()
    return redirect('/')

login_manager=LoginManager(app)
login_manager.login_view = '/login'
@login_manager.user_loader #загрузка пользователя
def load_user(user_id):
    return User.query.get(user_id)

if __name__=='__main__':
    app.run(debug=True)
