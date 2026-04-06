import flask
import wtforms
import sqlalchemy
import sqlalchemy.orm
import os
# инициализируем апу 
app = flask.Flask(import_name=__name__, template_folder=os.getcwd())
conn_string = "postgresql+psycopg2://postgres:122345@127.0.0.1:5432/Ne_oleg"
engine = sqlalchemy.create_engine(conn_string)
cyr_str="абвгдеёжзиклмнопрстуфхцчшщъыьэюя"

class Forma1(wtforms.Form):
    username = wtforms.StringField(label='Имя пользователя', validators=[wtforms.validators.Length(min=6,message="Минимум 6 символов, латиница и цифры"), wtforms.validators.InputRequired()])
    email = wtforms.EmailField(label="E-mail", validators=[wtforms.validators.Email(), wtforms.validators.InputRequired()])
    password = wtforms.PasswordField(label="Пароль", validators=[wtforms.validators.Length(min=8), wtforms.validators.InputRequired()])
    fio = wtforms.StringField(label="ФИО", validators=[wtforms.validators.InputRequired()])
    phone = wtforms.StringField(label="Номер телефона", validators=[wtforms.validators.Length(max=12,min=12), wtforms.validators.InputRequired()])

class Base(sqlalchemy.orm.DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    username = sqlalchemy.orm.mapped_column(sqlalchemy.String(), primary_key=True)
    email = sqlalchemy.orm.mapped_column(sqlalchemy.String())
    password = sqlalchemy.orm.mapped_column(sqlalchemy.String())
    fio = sqlalchemy.orm.mapped_column(sqlalchemy.String())
    phone = sqlalchemy.orm.mapped_column(sqlalchemy.String())
    def __init__(self, username, email, password, fio, phone):
        self.username = username
        self.email = email
        self.password = password
        self.fio = fio
        self.phone = phone

# страница регистрации(фио только кирилица)
@app.route("/")
def main():
    regform = Forma1()
    if flask.request.method == "POST" and regform.validate():
        form_data = flask.request.form
        username = form_data.get("username")
        email = form_data.get("email")
        password = form_data.get("password")
        fio = form_data.get("fio")
        for c in fio:
            if c == " ":
                continue
            if not(c.lower() in cyr_str):
                return flask.render_template("index.html", form=regform, error="Допускаются только кириллические символы")
        phone = form_data.get("phone")
        new_user = User(username, email, password, fio, phone)
        with sqlalchemy.orm.Session(engine) as s:
            fail = None
            stmt = sqlalchemy.select(User).filter_by(username).one()
            fail = s.scalars(stmt)
            if fail != None:
                return flask.render_template("index.html", form=regform, error="Такой пользователь уже существует")
            s.add(new_user)
            s.commit()
            
    return flask.render_template("index.html", form=regform, error="")


# страница авторизации

# страница просмотра заявок

# страница формирования заявки 

# панель админа 