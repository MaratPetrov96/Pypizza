from database import *
from flask_admin import AdminIndexView,Admin,expose,BaseView
from flask_admin.contrib.sqla import ModelView

class AdminP(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self,name , **kwargs):
        return self.render('UniversalLogin.html')
class Model(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self,name , **kwargs):
        return self.render('UniversalLogin.html')
class Mod(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self,name ,**kwargs):
        return self.render('UniversalLogin.html')
class NewUser(Mod): #форма для добавления пользователя
    column_exclude_list = ('password',)
    create_template='CreateUser.html'
class NewFood(Mod): #форма для добавления товара
    column_list = ['kind_id','name','price','description','picture']
    form_columns = ['kind_id','name','price','description','picture']
class KindView(Mod): #просмотр разделов подредактирован, чтобы админ нашёл ID нужного
    column_list = ['id','name']

admin=Admin(app,'Food',url='/',index_view=AdminP(name='Pizzeria'))
admin.add_view(NewUser(User,db.session))
admin.add_view(KindView(Kind,db.session))
admin.add_view(NewFood(Food,db.session))
