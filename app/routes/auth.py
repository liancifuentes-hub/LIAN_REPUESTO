from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import Usuario

auth_bp = Blueprint("auth", __name__)


def login_required(f):
    """Decorador para proteger rutas que requieren autenticación"""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


@auth_bp.route("/")
def index():
    """Redirigir a login desde la raíz"""
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Vista de login - Vista principal"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Validaciones
        if not username or not password:
            flash("Por favor, complete todos los campos", "error")
            return render_template("auth/login.html")

        # Buscar usuario en BD
        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario:
            flash("Usuario no existe", "error")
            return render_template("auth/login.html")

        # Verificar contraseña
        if not check_password_hash(usuario.password, password):
            flash("Contraseña incorrecta", "error")
            return render_template("auth/login.html")

        # Login exitoso - crear sesión
        session["user_id"] = usuario.id
        session["username"] = usuario.username

        flash(f"¡Bienvenido {usuario.username}!", "success")
        return redirect(url_for("repuestos.listar"))

    # Si ya está logueado, redirigir a repuestos
    if "user_id" in session:
        return redirect(url_for("repuestos.listar"))

    return render_template("auth/login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    """Vista de registro de nuevos usuarios"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")

        # Validaciones
        if not username or not password:
            flash("Por favor, complete todos los campos", "error")
            return render_template("auth/registro.html")

        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "error")
            return render_template("auth/registro.html")

        if password != password_confirm:
            flash("Las contraseñas no coinciden", "error")
            return render_template("auth/registro.html")

        # Verificar si el username ya existe
        usuario_existente = Usuario.query.filter_by(username=username).first()
        if usuario_existente:
            flash("Este nombre de usuario ya existe", "error")
            return render_template("auth/registro.html")

        # Crear nuevo usuario
        try:
            password_hash = generate_password_hash(password)
            nuevo_usuario = Usuario(username=username, password=password_hash)
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Login automático después del registro
            session["user_id"] = nuevo_usuario.id
            session["username"] = nuevo_usuario.username

            flash(f"¡Registro exitoso! Bienvenido {username}", "success")
            return redirect(url_for("repuestos.listar"))
        except Exception:
            db.session.rollback()
            flash("Error al registrar usuario. Intente nuevamente.", "error")
            return render_template("auth/registro.html")

    return render_template("auth/registro.html")


@auth_bp.route("/logout")
def logout():
    """Cerrar sesión"""
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("auth.login"))
