from flask import redirect, render_template, request
from flask.ext import admin
from flask.ext.admin import expose
from flask.ext.admin.base import MenuLink
from flask.ext.admin.contrib import sqla
from flask.ext import login

from dialogando.models import *
from dialogando.tools.email import get_person_email

# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect('/login')
        return super(MyAdminIndexView, self).index()

    @expose('/lista')
    def lista(self):
        if not login.current_user.is_authenticated():
            return redirect('/login')

        persons = Person.query.all()
        return render_template('lista.html', persons=persons)

    @expose('/email')
    def email(self):
        if not login.current_user.is_authenticated():
            return redirect('/login')

        person_id = request.args.get('id')
        person_email = get_person_email(person_id)
        return render_template('email.html', person_email=person_email)

class UserAdmin(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

class AlternativeQuestionAdmin(sqla.ModelView):
    inline_models = (AlternativeOption,)

    def is_accessible(self):
        return login.current_user.is_authenticated()

class ThemeQuestionAdmin(sqla.ModelView):
    inline_models = (DissertativeQuestion,)

    def is_accessible(self):
        return login.current_user.is_authenticated()

class SimpleQuestionAdmin(sqla.ModelView):
#    inline_models = (SimpleQuestion,)

    def is_accessible(self):
        return login.current_user.is_authenticated()

class SimpleAnswersAdmin(sqla.ModelView):
    inline_models = (Person, )

    def is_accessible(self):
        return login.current_user.is_authenticated()

class PersonAdmin(sqla.ModelView):
#    inline_models = (SimpleQuestion,)
    column_searchable_list = ('name',)

    def is_accessible(self):
        return login.current_user.is_authenticated()


admin = admin.Admin(name='Dialogando', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(UserAdmin(User, db.session))
#admin.add_view(ThemeQuestionAdmin(ThemeQuestions, db.session))
admin.add_view(SimpleQuestionAdmin(SimpleQuestion, db.session))
admin.add_view(SimpleAnswersAdmin(SimpleAnswers, db.session))
admin.add_view(PersonAdmin(Person, db.session))
#admin.add_link(MenuLink(name='Lista candidatos', url='/lista'))
#admin.add_view(AlternativeQuestionAdmin(AlternativeQuestion, db.session))


