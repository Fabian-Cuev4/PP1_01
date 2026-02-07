// Formularios SIGLAB - Gestión de Máquinas y Mantenimiento
// Maneja registro de máquinas y mantenimientos del sistema

document.addEventListener("DOMContentLoaded", () => {

    // Creamos modal de notificaciones dinámicamente
    // Permite reutilización en toda la aplicación
    const codigoModalHTML = `
    <div id="validationModal" class="validation-modal-overlay">
        <div class="validation-card">
            <div id="modalIcon" class="modal-icon"></div>
            <h3 id="modalTitle" class="modal-title"></h3>
            <p id="modalMessage" class="modal-message"></p>
            <button id="btnModalOk" class="btn-modal-ok">Entendido</button>
        </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend', codigoModalHTML);

    // Referencias a elementos del modal
    const modalNotificacion = document.getElementById("validationModal");
    const iconoModal = document.getElementById("modalIcon");
    const tituloModal = document.getElementById("modalTitle");
    const mensajeModal = document.getElementById("modalMessage");
    const botonAceptarModal = document.getElementById("btnModalOk");

    // Función global: muestra modal con diferentes tipos de notificación
    // Parámetros: tipo (success/error/warning), título, mensaje, callback (opcional)
    window.mostrarModal = (tipo, titulo, mensaje, callback = null) => {
        let codigoIcono = '';
        
        // Seleccionar ícono según tipo de mensaje
        if (tipo === 'success') codigoIcono = '<i class="fa-solid fa-circle-check icon-success"></i>';
        else if (tipo === 'error') codigoIcono = '<i class="fa-solid fa-circle-xmark icon-error"></i>';
        else if (tipo === 'warning') codigoIcono = '<i class="fa-solid fa-triangle-exclamation icon-warning"></i>';

        // Configurar modal con datos recibidos
        iconoModal.innerHTML = codigoIcono;
        tituloModal.textContent = titulo;
        mensajeModal.textContent = mensaje;
        modalNotificacion.classList.add("active");
        
        // Configurar botón aceptar
        botonAceptarModal.onclick = () => {
            console.log("Botón 'Entendido' presionado");
            modalNotificacion.classList.remove("active");
            // Ejecutar callback si existe (para redirecciones automáticas)
            if (callback) {
                console.log("Ejecutando callback después de cerrar modal");
                callback();
            }
        };
    };

    // Referencias a elementos principales de formularios
    const botonCancelar = document.getElementById("btn-cancel-action");
    const formularioMaquina = document.querySelector(".form");
    const botonGuardarMantenimiento = document.querySelector(".btn-save");

    // Botón cancelar: regresa a lista de máquinas
    if (botonCancelar) {
        botonCancelar.addEventListener("click", () => {
            window.location.href = "/pagina/maquinas";
        });
    }

    // Formulario de máquina: maneja registro de nuevas máquinas
    if (formularioMaquina) {
        formularioMaquina.addEventListener("submit", async (evento) => {
            evento.preventDefault();

            // Obtener nombre de usuario desde sesión
            const nombreUsuario = sessionStorage.getItem('username') || null;
            
            // Recopilar datos del formulario
            const datosMaquina = {
                tipo_equipo: document.getElementById("tipo_equipo").value,
                codigo_equipo: document.getElementById("codigo").value,
                estado_actual: document.getElementById("estado_actual").value,
                area: document.getElementById("area").value,
                fecha: document.getElementById("fecha").value,
                usuario: nombreUsuario
            };

            // VALIDACIÓN: Verificar campos obligatorios
            if (!datosMaquina.tipo_equipo || !datosMaquina.codigo_equipo || !datosMaquina.estado_actual) {
                mostrarModal('warning', 'Campos Incompletos', 'Por favor, completa todos los campos obligatorios.');
                return;
            }

            try {
                // ENVIAR DATOS: Realizar la petición al backend
                const respuesta = await fetch("/api/maquinas/agregar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosMaquina)
                });

                // ÉXITO: Verificar respuesta.ok ANTES de procesar JSON
                if (respuesta.ok) {
                    const resultado = await respuesta.json();
                    mostrarModal('success', '¡Registro Exitoso!', 'La máquina ha sido registrada correctamente.', () => {
                        console.log("Redirigiendo a /pagina/maquinas");
                        window.location.href = "/pagina/maquinas";
                    });
                } else {
                    // ERROR: Procesar el error del backend
                    let errorPayload = null;
                    try {
                        errorPayload = await respuesta.json();
                    } catch (e) {
                        errorPayload = null;
                    }

                    let msg = "No se pudo guardar la máquina.";
                    if (errorPayload && errorPayload.detail !== undefined && errorPayload.detail !== null) {
                        if (typeof errorPayload.detail === 'string') {
                            msg = errorPayload.detail;
                        } else {
                            try {
                                msg = JSON.stringify(errorPayload.detail);
                            } catch (e) {
                                msg = String(errorPayload.detail);
                            }
                        }
                    } else {
                        try {
                            const txt = await respuesta.text();
                            if (txt) {
                                msg = txt;
                            }
                        } catch (e) {
                        }
                    }

                    mostrarModal('error', 'Error al Guardar', msg);
                }
            } catch (error) {
                // ERROR DE CONEXIÓN: Problemas de red o servidor caído
                mostrarModal('error', 'Error de Conexión', 'No se pudo contactar con el servidor.');
            }
        });
    }

    // DETECTAR PÁGINA: Verificamos si estamos en el formulario de mantenimiento
    const esPaginaMantenimiento = document.getElementById("mant-empresa") !== null;

    // FORMULARIO DE MANTENIMIENTO: Maneja el registro de mantenimientos con polling en tiempo real
    if (botonGuardarMantenimiento && esPaginaMantenimiento) {
        // CONFIGURACIÓN DE POLLING PARA MANTENIMIENTO
        const TIEMPO_POLLING_MS = 2000; // Cada 2 segundos para mayor estabilidad
        let pollingInterval = null;
        
        // FUNCIÓN: Iniciar polling para mantenimientos
        function iniciarPollingMantenimiento() {
            // Detener polling anterior si existe
            if (pollingInterval) {
                clearInterval(pollingInterval);
            }
            
            // Obtener el código de la máquina desde los parámetros de la URL
            const parametrosURL = new URLSearchParams(window.location.search);
            const codigoMaquina = parametrosURL.get("codigo");
            
            if (!codigoMaquina) return;
            
            // Iniciar nuevo polling
            pollingInterval = setInterval(async () => {
                try {
                    const timestamp = new Date().getTime();
                    const response = await fetch(`/api/mantenimiento/listar/${encodeURIComponent(codigoMaquina)}?_t=${timestamp}`, {
                        headers: { 'Cache-Control': 'no-cache' }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        // Aquí podríamos actualizar una lista de mantenimientos recientes si quisiéramos
                        console.log("Polling de mantenimientos actualizado");
                    }
                } catch (error) {
                    console.error("Error en polling de mantenimientos:", error);
                }
            }, TIEMPO_POLLING_MS);
            
            console.log(`Polling de mantenimientos iniciado para máquina: ${codigoMaquina}`);
        }

        // FUNCIÓN: Detener polling
        function detenerPolling() {
            if (pollingInterval) {
                clearInterval(pollingInterval);
                pollingInterval = null;
                console.log("Polling de mantenimientos detenido");
            }
        }

        // Iniciar polling automáticamente al cargar la página
        iniciarPollingMantenimiento();

        botonGuardarMantenimiento.addEventListener("click", async (evento) => {
            evento.preventDefault();

            // Obtener el código de la máquina desde los parámetros de la URL
            const parametrosURL = new URLSearchParams(window.location.search);
            const codigoMaquinaSeleccionada = parametrosURL.get("codigo");

            // VALIDACIÓN: Asegurarnos de que tenemos una máquina válida
            if (!codigoMaquinaSeleccionada) {
                mostrarModal('error', 'Error', 'No se ha seleccionado una máquina válida.');
                return;
            }

            // Obtener el nombre de usuario desde la sesión
            const nombreUsuario = sessionStorage.getItem('username') || null;
            
            // Recopilar los datos del formulario de mantenimiento
            const datosMantenimiento = {
                codigo_maquina: codigoMaquinaSeleccionada,
                empresa: document.getElementById("mant-empresa").value,
                tecnico: document.getElementById("mant-tecnico").value,
                tipo: document.getElementById("mant-tipo").value,
                fecha: document.getElementById("mant-fecha").value,
                observaciones: document.getElementById("mant-observaciones").value,
                usuario: nombreUsuario
            };

            // VALIDACIÓN: Campos obligatorios para mantenimiento
            if (!datosMantenimiento.tecnico || !datosMantenimiento.fecha || !datosMantenimiento.tipo) {
                mostrarModal('warning', 'Faltan Datos', 'El técnico, la fecha y el tipo de mantenimiento son obligatorios.');
                return;
            }

            try {
                // ENVIAR DATOS: Realizar la petición al backend
                const respuesta = await fetch("/api/mantenimiento/agregar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosMantenimiento)
                });

                // ÉXITO: Mostrar confirmación y redirigir
                if (respuesta.ok) {
                    const resultado = await respuesta.json();
                    mostrarModal('success', 'Mantenimiento Guardado', `Se registró el mantenimiento para ${codigoMaquinaSeleccionada}.`, () => {
                        console.log("Redirigiendo a /pagina/maquinas");
                        window.location.href = "/pagina/maquinas";
                    });
                } else {
                    // ERROR: Procesar el error del backend
                    let errorPayload = null;
                    try {
                        errorPayload = await respuesta.json();
                    } catch (e) {
                        errorPayload = null;
                    }

                    let msg = "No se pudo registrar el mantenimiento.";
                    if (errorPayload && errorPayload.detail !== undefined && errorPayload.detail !== null) {
                        if (typeof errorPayload.detail === 'string') {
                            msg = errorPayload.detail;
                        } else {
                            try {
                                msg = JSON.stringify(errorPayload.detail);
                            } catch (e) {
                                msg = String(errorPayload.detail);
                            }
                        }
                    } else {
                        try {
                            const txt = await respuesta.text();
                            if (txt) {
                                msg = txt;
                            }
                        } catch (e) {
                        }
                    }

                    mostrarModal('error', 'Error al Guardar Mantenimiento', msg);
                }
            } catch (error) {
                // ERROR DE CONEXIÓN: Problemas de red o servidor caído
                mostrarModal('error', 'Error Crítico', 'Falló la conexión con el servidor.');
            }
        });
    }
});