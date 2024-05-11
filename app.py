import os
from flask import Flask, request, render_template_string, jsonify
from weasyprint import HTML

app = Flask(__name__)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json  # Obtener datos de la solicitud JSON
        
        # Renderizar la plantilla HTML con los datos recibidos
        rendered_html = render_template_string("""
            <!DOCTYPE html>
                <html>
                <head>  
                <style>
                    * {
                    font-family: arial;
                    font-size: 9pt;
                    }

                    body {
                    background-image: url(data:image/png;base64,{{ BackImage.content }});
                    background-size: cover;
                    background-repeat: no-repeat;
                    }

                    .container {
                    width: 90%;
                    max-width: 1200px;
                    margin: 0 auto;
                    }

                    .head-left {
                    float: right;
                    top: 0;
                    right: 0;
                    padding: 20px;
                    background-color: #ffffff;
                    color: #003582;
                    }

                    .head2 {
                    margin-top: 120px;
                    color: black;
                    font-weight: 600;
                    }

                    .head3 {
                    margin-top: 10px;
                    }
                </style>
                </head>
                <body>
                <div class="container">

                    <div class="head-left">
                    <img src="data:image/png;base64,{{ Encabezado.content }}" alt="Firma" style="width: 360px; height: 90px; float: right; margin-top: 5px;" />
                    </div>
                    <br>
                    <br>
                    <br>

                    <div class="head2">

                    </div>
                    <div class="head3">
                    <b>SEÑOR</b><br>
                    <p>{{ Despacho }}</p><br>
                    </div>
                    <br>
                    <table>
                    <tr>
                        <td><b>REF:</b></td>
                        <td><b>PROCESO EJECUTIVO DE {{ Cuantia }} CUANTIA</b></td>
                    </tr>
                    <tr>
                        <td><b>RADICADO:</b></td>
                        <td><b>{{ Radicado }}</b></td>
                    </tr>
                    <tr>
                        <td><b>DEMANDANTE:</b></td>
                        <td><b>{{ demandante }}</b></td>
                    </tr>
                    <tr>
                        <td><b>DEMANDADO:</b></td>
                        <td><b>{{ Nombre }}</b></td>
                    </tr>
                    <tr>
                        <td><b>ASUNTO:</b></td>
                        <td><b>{{ asuntoName }}</b></td>
                    </tr>
                    </table>
                    <br><br><br><br>

                    {{ CuerpoDelCorreo }}
                    <br><br><br>
                    <p>Del Señor Juez,</p>
                    <p>Atentamente,</p>
                    <img src="data:image/png;base64,{{ Firma.content }}" alt="Firma" style="width: 150px; height: 70px;" /><br><br>
                    <p>CAROLINA CORONADO ALDANA</p>
                    <p>C.C. No. 52.476.306 de Bogotá D.C.</p>
                    <p>T.P 125.650 del C. S de la J.</p>
                </div>
                </body>
                </html>
        """, **data)

        # Generar el PDF utilizando WeasyPrint
        pdf = HTML(string=rendered_html).write_pdf()
        
        # Ruta de la carpeta donde se guardará el PDF
        folder_path = 'pdfs'
        # Crear la carpeta si no existe
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # Ruta del archivo PDF
        pdf_path = os.path.join(folder_path, 'documento.pdf')
        # Guardar el PDF en la carpeta
        with open(pdf_path, 'wb') as f:
            f.write(pdf)
        
        # Devolver la ruta del archivo PDF como respuesta al cliente
        return jsonify({'pdf_path': pdf_path}), 200
    except Exception as e:
           return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5005)
