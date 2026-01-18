// LIAN REPUESTOS - JavaScript Personalizado

// Función de confirmación antes de eliminar repuesto
function confirmarEliminacion() {
    return confirm('¿Está seguro de eliminar este repuesto?');
}

// Confirmación para formularios de eliminación
document.addEventListener('DOMContentLoaded', function() {
    // Buscar todos los formularios de eliminación y agregar confirmación
    const formsEliminar = document.querySelectorAll('form[action*="/eliminar/"]');
    
    formsEliminar.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirmarEliminacion()) {
                e.preventDefault();
                return false;
            }
        });
    });
});

// Validación de formularios (mejoras adicionales)
document.addEventListener('DOMContentLoaded', function() {
    // Validación en tiempo real de campos de formulario
    const nombreInput = document.getElementById('nombre');
    if (nombreInput) {
        nombreInput.addEventListener('input', function() {
            const value = this.value.trim();
            if (value.length > 0 && value.length < 3) {
                this.setCustomValidity('El nombre debe tener al menos 3 caracteres');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Validación de precio
    const precioInput = document.getElementById('precio');
    if (precioInput) {
        precioInput.addEventListener('input', function() {
            const value = this.value.trim();
            if (!value) {
                this.setCustomValidity('El precio es obligatorio');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Auto-ocultar alertas después de 5 segundos
    const alertas = document.querySelectorAll('.alert:not(.alert-permanent)');
    alertas.forEach(function(alerta) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alerta);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });
});
