        // Manejar la solicitud del formulario
        document.getElementById('consulta-form').addEventListener('submit', function(event) {
            event.preventDefault(); // Evita el envío tradicional del formulario
            let ciudad = document.getElementById('ciudad').value;
            let fechaInicio = document.getElementById('fechaInicio').value;
            let fechaFin = document.getElementById('fechaFin').value;
            console.log(ciudad, fechaInicio, fechaFin);
            // Realizar la solicitud AJAX
            fetch(`/consulta_rango/${ciudad}/${fechaInicio}/${fechaFin}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error en la consulta');
                    }
                    return response.text(); // Si la respuesta es HTML
                })
                .then(data => {
                    // Insertar el resultado en el div 'resultado'
                    document.getElementById('contenedorTabla').innerHTML = data;
                })
                .catch(error => {
                    console.error('Hubo un problema con la petición AJAX:', error);
                });
        });