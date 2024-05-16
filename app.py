import os
from flask import Flask, request, render_template_string, jsonify
from weasyprint import HTML
import base64  # Agrega esta importación

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
                margin:0;
                padding:0;
                }

                body {
                
                background-size: cover;
                background-repeat: no-repeat;
                }

                .container {
                width: 100%;
                max-width: 1300px;
                margin: 0 auto;
                }

                .head-left {
                float: right;
                top: 0;
                right: 0;
                padding: 5px;
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
                <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjzIoACSSgvoWhXnOxrtZsF-nG1MdbhRt73Tm7IIrk7M1BSZtP1FS7JkN1J188kPXGH06uzjziV1p6zDoQuMx0qMTUph9WmPRvXwGuj4Q1UMv-U6vHb1TvPKobwndcrxG3_c2vCszXzmg2-YCziJ22npwE7b0Dhg-JTE_KjeTK4FKCWpUu5hbXM753-26M/w629-h137/encabezado.PNG" 
                alt="Encabezado" style="width: 380px; height: 90px; float: right;">
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
                <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhLrOQsNQT0U8V3w6TbA9ceiDjuwnWintWuM39Qqzxo5D983qfi2VMobt0978ILcKaXu2HpCFmOhULdyhPZ5hLl0xlCYjs0zNzfQYtq3cvMZ-pi9kAIq7Cp3yua3Yqg9fQEvRBIJpgoxAXjqJlN1L5RzFtIdaVbo3bIFGHwPyN5luUPxLLSwb92Y7vO0iU/s1600/firma.png"
                 alt="Firma" style="width: 150px; height: 70px;" /><br><br>
                <p>CAROLINA CORONADO ALDANA</p>
                <p>C.C. No. 52.476.306 de Bogotá D.C.</p>
                <p>T.P 125.650 del C. S de la J.</p>
            </div>
            </body>
            </html>
        """, **data)

        # Generar el PDF utilizando WeasyPrint
        pdf = HTML(string=rendered_html).write_pdf()

        # Codificar el PDF en Base64
        pdf_base64 = base64.b64encode(pdf).decode('utf-8')

        # Devolver el PDF codificado en Base64 como respuesta al cliente
        return jsonify({'pdf': pdf_base64}), 200
    except Exception as e:
           return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5005)
