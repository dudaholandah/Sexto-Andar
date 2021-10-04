from app import app, cnx
from flask import request, render_template, session, g
from werkzeug.utils import redirect
from app.models.cliente_dao import ClienteDAO
from app.models.corretor_dao import Corretor, CorretorDAO

from app.models.usuario_dao import Usuario
from app.models.login_dao import Login, LoginDAO
from app.models.endereco_dao import Endereco, EnderecoDAO
from app.models.proprietario_dao import ProprietarioDAO

def from_form_to_usuario(request):
    nome = request.form.get("InputName")
    cpf = request.form.get("InputCPF")
    data_de_nascimento = request.form.get("InputDateBirth")
    fk_endereco = None
    fk_login = None

    fem = request.form.getlist('Feminino') 
    masc = request.form.getlist('Masculino')
    sexo = ""

    if fem.count('on'): sexo = "Feminino" 
    elif masc.count('on'): sexo = "Masculino"
    else: sexo = "Outro"

    return Usuario(cpf, nome, data_de_nascimento, sexo, fk_endereco, fk_login)

def from_form_to_login(request):
    codigo = None
    email = request.form.get("InputEmail")
    senha = request.form.get("InputPassword")

    return Login(codigo, email, senha)

def from_form_to_endereco(request):
    codigo = None
    CEP = request.form.get("InputZipcode")
    rua = request.form.get("InputStreet")
    bairro = request.form.get("InputRegion")
    cidade = request.form.get("InputCity")
    estado = request.form.getlist('estado')[0]
    numero = request.form.get("InputNumber")
    complemento = request.form.get("InputAddressComplement")

    return Endereco(codigo, CEP, rua, bairro, cidade, estado, numero, complemento)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    # transformar para so um if
    if request.method == 'POST':
        if 'cadastrar' in request.form:

            # fazer a validacao dos dados para colocar no BD

            usuario = from_form_to_usuario(request)
            login = from_form_to_login(request)
            endereco = from_form_to_endereco(request)             

            cliente = request.form.getlist('Cliente') 
            corretor = request.form.getlist('Corretor')
            proprietario = request.form.getlist('Proprietario') 
            print(cliente, corretor, proprietario)
            
            try:
                cursor = cnx.connection.cursor()
                LoginDAO().create(cursor, login)
                EnderecoDAO().create(cursor, endereco)
                usuario.fk_endereco = endereco.codigo
                usuario.fk_login = login.codigo

                if cliente.count("ON"):
                    permission = f"INSERT INTO permissao(fk_login, tipo) VALUES ('{login.codigo}', 'cliente')"
                    cursor.execute(permission)

                    ClienteDAO().create(cursor, usuario)

                if corretor.count("ON"):

                    # bug aqui
                    permission = f"INSERT INTO permissao(fk_login, tipo) VALUES ('{login.codigo}', 'corretor' )"
                    cursor.execute(permission)

                    horario_inicio = request.form.get("InputHorarioInicialCorretor")
                    horario_final = request.form.get("InputHorarioFinalCorretor")
                    print(1)
                    corretor = Corretor(usuario.cpf, usuario.nome, usuario.data_de_nascimento, usuario.sexo,
                                        usuario.fk_endereco, usuario.fk_login, horario_inicio, horario_final)
                    print(2)
                    CorretorDAO().create(cursor, corretor)
                    print(3)
    
                if proprietario.count("ON"):
                    permission = f"INSERT INTO permissao(fk_login, tipo) VALUES ('{login.codigo}', 'proprietario')"
                    cursor.execute(permission)

                    ProprietarioDAO().create(cursor, usuario)

                cnx.connection.commit()

            except Exception as ex:
                print(ex)
                return render_template('sign_up.html', error_statement=ex)
                
            return render_template('sign_up_sucesso.html')
        else:
            return redirect('/login')
    else:
        return render_template('sign_up.html')

@app.before_request
def before_request():
    if 'user_id' in session:
        try:
            cursor = cnx.connection.cursor()
            select = f"SELECT * FROM login where codigo = '{session['user_id']}'"
            cursor.execute(select)
            user =  cursor.fetchone()
            if not user:
                return
            #print(user)

            sql = f"SELECT * FROM permissao WHERE fk_login = '{user[0]}'"
            cursor.execute(sql)
            permission = cursor.fetchone()

            g.user = user
            g.permission = permission
        except Exception as ex:
            print(ex)


#login falta só olhar se o user tem permissao de admin para habilitar a pagina do CRUD 
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        if 'sign_up' in request.form:
            return redirect("/sign_up")
        else:
            # pega o usuario e senha do login.html
            email = request.form.get("InputEmail")
            password = request.form.get("InputPassword")

            # deleta a sessao de usuario online
            session.pop('user_id', None)    

            #verifica email == senha
            try:
                cursor = cnx.connection.cursor()
                select = f"SELECT * FROM login where email = '{email}' AND senha = '{password}'"
                cursor.execute(select)
                user =  cursor.fetchone()

                print(user)
                print(email, password)

                if not user:
                    return render_template("login.html", error_statement='Login invalido!')                

                #cria a sessão do usuario
                session['user_id'] = user[0]

                return render_template("login_sucesso.html", user=user[1])
            
            except Exception as ex:
                return render_template("login.html", error_statement=ex)
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    user = g.user[1]
    session.pop('user_id', None)
    return render_template('logout.html', user=user)