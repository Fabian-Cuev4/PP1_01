document.addEventListener("DOMContentLoaded", () => {
    const btnBuscar = document.getElementById("btn-buscar");
    const inputCodigo = document.getElementById("input-codigo");
    const tablaBody = document.getElementById("tabla-reporte");

    const cargarDatos = async (codigo = "") => {
        try {
            const url = codigo ? `/home/mantenimiento/informe-general?codigo=${codigo}` : `/home/mantenimiento/informe-general`;
            const response = await fetch(url);
            if (!response.ok) throw new Error("No se encontraron datos");
            
            const data = await response.json();
            tablaBody.innerHTML = "";

            data.forEach(inf => {
                if (inf.mantenimientos.length === 0) {
                    tablaBody.innerHTML += `
                        <tr>
                            <td class="fw-bold">${inf.codigo}</td>
                            <td>${inf.area}</td>
                            <td colspan="5" style="text-align:center;">Sin mantenimientos</td>
                            <td><button class="btn-icon"><i class="fa-solid fa-eye"></i></button></td>
                        </tr>`;
                } else {
                    inf.mantenimientos.forEach(m => {
                        tablaBody.innerHTML += `
                            <tr>
                                <td class="fw-bold">${inf.codigo}</td>
                                <td>${inf.area}</td>
                                <td>${m.tecnico}</td>
                                <td>${m.fecha}</td>
                                <td><span class="badge">${m.tipo}</span></td>
                                <td><span class="badge">${inf.estado}</span></td>
                                <td>${m.observaciones}</td>
                                <td>
                                    <button class="btn-icon"><i class="fa-solid fa-eye"></i></button>
                                </td>
                            </tr>`;
                    });
                }
            });
        } catch (error) {
            tablaBody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:red;">${error.message}</td></tr>`;
        }
    };

    if (btnBuscar) {
        btnBuscar.addEventListener("click", () => {
            cargarDatos(inputCodigo.value.trim());
        });
    }

    // Cargar todo al inicio
    cargarDatos();
});