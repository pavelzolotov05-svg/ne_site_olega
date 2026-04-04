import flask
import wtforms
# инициализируем апу 
app = flask.Flask(import_name=__name__)

class Forma1(wtforms.Form):
    username = wtforms.StringField(label='Имя пользователя', validators=[wtforms.validators.Length(min=6,message="Минимум 6 символов, латиница и цифры"), wtforms.validators.InputRequired()])
    email = wtforms.EmailField(label="E-mail", validators=[wtforms.validators.Email(), wtforms.validators.InputRequired()])
    password = wtforms.PasswordField(label="Пароль", validators=[wtforms.validators.Length(min=8), wtforms.validators.InputRequired()])
    fio = wtforms.StringField(label="ФИО", validators=[wtforms.validators.InputRequired()])
    phone = wtforms.StringField(label="Номер телефона", validators=[wtforms.validators.Length(max=12,min=12), wtforms.validators.InputRequired()])

# страница регистрации(фио только кирилица)
@app.route("/")
def main():
    regform = Forma1()
    ctx = {"form":regform}
    return flask.render_template("index.html", ctx)

# страница авторизации

# страница просмотра заявок

# страница формирования заявки 

# панель админа 