from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Repuesto
from app.routes.auth import login_required

repuestos_bp = Blueprint('repuestos', __name__, url_prefix='/repuestos')

@repuestos_bp.route('/')
@repuestos_bp.route('/listar')
@login_required
def listar():
    """Listar repuestos con paginación (50 por página)"""
    page = request.args.get('page', 1, type=int)
    
    try:
        repuestos = Repuesto.query.paginate(
            page=page,
            per_page=50,
            error_out=False
        )
        return render_template('repuestos/listar.html', repuestos=repuestos)
    except Exception as e:
        flash('Error al cargar los repuestos', 'error')
        return render_template('repuestos/listar.html', repuestos=None)

@repuestos_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear nuevo repuesto"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio = request.form.get('precio', '').strip()
        
        # Validaciones
        if not nombre or len(nombre) < 3 or len(nombre) > 50:
            flash('El nombre debe tener entre 3 y 50 caracteres', 'error')
            return render_template('repuestos/crear.html')
        
        if not descripcion or len(descripcion) > 200:
            flash('La descripción es obligatoria y no puede exceder 200 caracteres', 'error')
            return render_template('repuestos/crear.html')
        
        if not precio:
            flash('El precio es obligatorio', 'error')
            return render_template('repuestos/crear.html')
        
        # Crear repuesto
        try:
            nuevo_repuesto = Repuesto(
                nombre_repuesto=nombre,
                descripcion_repuesto=descripcion,
                precio_repuesto=precio
            )
            db.session.add(nuevo_repuesto)
            db.session.commit()
            
            flash('Repuesto creado exitosamente', 'success')
            return redirect(url_for('repuestos.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el repuesto. Intente nuevamente.', 'error')
            return render_template('repuestos/crear.html')
    
    return render_template('repuestos/crear.html')

@repuestos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar repuesto existente"""
    repuesto = Repuesto.query.get_or_404(id)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio = request.form.get('precio', '').strip()
        
        # Validaciones
        if not nombre or len(nombre) < 3 or len(nombre) > 50:
            flash('El nombre debe tener entre 3 y 50 caracteres', 'error')
            return render_template('repuestos/editar.html', repuesto=repuesto)
        
        if not descripcion or len(descripcion) > 200:
            flash('La descripción es obligatoria y no puede exceder 200 caracteres', 'error')
            return render_template('repuestos/editar.html', repuesto=repuesto)
        
        if not precio:
            flash('El precio es obligatorio', 'error')
            return render_template('repuestos/editar.html', repuesto=repuesto)
        
        # Actualizar repuesto
        try:
            repuesto.nombre_repuesto = nombre
            repuesto.descripcion_repuesto = descripcion
            repuesto.precio_repuesto = precio
            db.session.commit()
            
            flash('Repuesto actualizado exitosamente', 'success')
            return redirect(url_for('repuestos.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el repuesto. Intente nuevamente.', 'error')
            return render_template('repuestos/editar.html', repuesto=repuesto)
    
    return render_template('repuestos/editar.html', repuesto=repuesto)

@repuestos_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    """Eliminar repuesto"""
    repuesto = Repuesto.query.get_or_404(id)
    
    try:
        db.session.delete(repuesto)
        db.session.commit()
        flash('Repuesto eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el repuesto', 'error')
    
    return redirect(url_for('repuestos.listar'))
