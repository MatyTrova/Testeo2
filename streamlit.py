# Importamos las librerias a utilizar
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime
import pytz
import time

# Configuramos la página
st.set_page_config(
    page_title="Calculadora Ahora 12",
    page_icon="imgs/CAME-Transparente.ico.ico",
    )

# Creamos la tasa de interés
tasas_cft = {"Ahora 3" : 0.1024 ,
         "Ahora 6" : 0.2887 ,
         "Ahora 12" : 0.3297 , 
         "Ahora 18" : 0.4380 ,
         "Ahora 24"  : 0.5221}
aux = False


# Aplicar estilos de formato CSS para agrandar el título
st.markdown("<h1 style='text-align: center; font-size: 54px; font-family: Verdana, sans-serif;'>Calculadora Ahora 12</h1>", unsafe_allow_html=True)

st.write("---")

# Columnas inferiores
col1, col2, col3 = st.columns([0.5,3,0.5])

with col1 :
    st.write("")

with col2 : 
    st.image("imgs/logos_came_recortados.png",use_column_width=True)
    
with col3 :
    st.write("")


st.write("---")
# Realizamos el input del monto

monto_input = st.text_input("Precio contado", value="$")
monto_credito = monto_input.strip()
monto_credito = monto_credito.replace("$", "").replace(".","").replace(",,",",").replace(",",".")

# listado de provincias
provincias = [
    "Seleccione una provincia",
    "Buenos Aires",
    "Ciudad Autónoma de Buenos Aires",
    "Catamarca",
    "Chaco",
    "Chubut",
    "Córdoba",
    "Corrientes",
    "Entre Ríos",
    "Formosa",
    "Jujuy",
    "La Pampa",
    "La Rioja",
    "Mendoza",
    "Misiones",
    "Neuquén",
    "Río Negro",
    "Salta",
    "San Juan",
    "San Luis",
    "Santa Cruz",
    "Santa Fe",
    "Santiago del Estero",
    "Tierra del Fuego",
    "Tucumán"
]


if monto_credito == "" or monto_credito == "$" or monto_credito == " " : 
    aux3 = False 
else:
    try:
        monto_credito = float(monto_credito)
        aux3= True
    except ValueError:
        st.text("Coloque un número válido porfavor")
        aux3 = False         
st.write("---")

provincia_seleccionada = st.selectbox("# Seleccione la provincia",provincias)  

if provincia_seleccionada == "Seleccione una provincia":
    aux_seleccionar_provincia = False
else:
    aux_seleccionar_provincia = True

st.write("---")
# Inputo de la cuota
programas = ["Ahora 3","Ahora 6","Ahora 12","Ahora 18","Ahora 24"]
programa_seleccionado = st.selectbox("Seleccione el programa",programas)    

st.write("---")

# Que seleccione 
inscripciones = ["Monotributista", "Responsable Inscripto", "Sociedad"]
tipo_inscripcion = st.selectbox("Seleccione el tipo de inscripción",inscripciones)

st.write("---")


                    # programa seleccionado



colA, colB = st.columns([1,2])
with colA : 
    # por las dudas lo guardo :p
    #with st.form("my_form"):
    #    button_clicked = st.form_submit_button("Calcular", help="Haz clic para calcular",use_container_width=True)
    
    #if button_clicked:
        # Cuando se hace clic en el botón, realiza alguna acción
    #    aux = True
    if st.button("Calcular"):
        if aux3 == True :
            if aux_seleccionar_provincia == True:
                aux = True
                tasas_interes = tasas_cft[programa_seleccionado]
    
                    # Arancel de la tarjeta de credito
                arancel_tarjeta = 0.018
    
                            # Calculamos la tasa del probrama
                base_tasa_programa = monto_credito * tasas_interes
    
                            # Calculamos la base 2
                base_arancel = monto_credito * arancel_tarjeta
    
                            # Iva arancel
                iva_arancel = 0.21 * base_arancel
    
                            # Iva del programa
                iva_programa = 0.105 * base_tasa_programa
    
                            # ingreso bruto
                iibb = 0.025 * base_tasa_programa
    
                            # otro iva
                iva3 = 0.015 * base_tasa_programa
    
                            # total de descuentos
                total_descuentos_1 = base_tasa_programa + iva_arancel + iva_programa + iibb + iva3 + base_arancel
    
                            # neto_percibido
                neto_percibido = monto_credito - total_descuentos_1
    
                            # descuento en %
                total_descuentos_2 = (total_descuentos_1 / monto_credito )
    
                            # monto a cobrar
                monto_a_cobrar = ( 1 / (1-total_descuentos_2) * monto_credito )
    
                
    
                # vuelvo a definir las variables según el monto a cobrar
                # linea divisoria 1
                base_tasa_programa = monto_a_cobrar * tasas_interes
    
                            # Calculamos la base 2
                base_arancel = monto_a_cobrar * arancel_tarjeta
    
                            # Iva arancel
                iva_arancel = 0.21 * base_arancel
    
                            # Iva del programa
                iva_programa = 0.105 * base_tasa_programa
    
                            # ingreso bruto
                iibb = 0.025 * base_tasa_programa
    
                            # otro iva
                iva3 = 0.015 * base_tasa_programa
    
                # reintegro a percibir
                reintegro = iva_arancel + iva_programa + iva3
                # linea divisoria 2
    
                #descuentos %
                total_descuentos_en_porcentaje = (total_descuentos_1 / monto_credito )
    
                total_descuentos_en_porcentaje_2 = (total_descuentos_1 / monto_credito ) * 100
                
                total_descuentos_pesos = monto_a_cobrar * total_descuentos_en_porcentaje
    
                neto_a_percibir = monto_a_cobrar - total_descuentos_pesos
    
                # Creamos lista de variables
                lista_variables = [monto_credito, monto_a_cobrar, total_descuentos_pesos, neto_a_percibir, base_tasa_programa, base_arancel, iva_arancel, iva_programa, iibb, iva3, reintegro, total_descuentos_en_porcentaje_2]
    
                # iteramos para el formato
                for i in range (len(lista_variables)) :
                    lista_variables[i] = '{:,.1f}'.format(lista_variables[i]).replace(',', ' ')
                    lista_variables[i] = lista_variables[i].replace(".",",")
                    lista_variables[i] = lista_variables[i].replace(" ",".")
            else:
                # Define un estilo CSS personalizado para cambiar el color del texto
                custom_css = """
                <style>
                    .my-text {
                        color: red;
                    }
                </style>
                """
                
                # Aplica el estilo CSS personalizado usando st.markdown
                st.markdown(custom_css, unsafe_allow_html=True)
                
                # Agrega un st.write con la clase CSS personalizada
                st.write("Provincia no válida", key="my-text")
                st.write("Vamo el rojo!.", key="my-text")
        else:
            pass  
    if aux == True:
        # Nombre del archivo PDF
        pdf_filename = "Resumen precio sugerido.pdf"

            # Crear un objeto BytesIO para guardar el PDF en memoria
        pdf_buffer = BytesIO()
            # Generar el PDF
        c = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Establecer la zona horaria a Buenos Aires
        zona_horaria = pytz.timezone('America/Argentina/Buenos_Aires')

        # Obtener la fecha y hora actual en la zona horaria especificada
        fecha_hora_actual = datetime.datetime.now(zona_horaria)

        # Obtener la fecha en formato dd/mm/aa
        fecha_actual = fecha_hora_actual.strftime("%d/%m/%y")

        # Obtener la hora en formato hh:mm:ss
        hora_actual = fecha_hora_actual.strftime("%H:%M:%S")

        # Escribimos la fecha actual 
        c.setFont("Helvetica", 10)
        c.drawString(40, 760, f"{fecha_actual} - {hora_actual}")

        # Agregar título
        c.setFont("Helvetica-Bold", 32)
        titulo = "Calculadora Ahora 12"
        titulo_width = c.stringWidth(titulo, "Helvetica-Bold", 32)
        titulo_x = (letter[0] - titulo_width) / 2  # Centrar el título horizontalmente
        c.drawString(titulo_x, 720, titulo)

        # Coordenadas y dimensiones de la imagen
        imagen_path = "imgs/logos_came_con_fondo y recortados2.png"  # Reemplaza 'tu_imagen.png' con la ruta de tu propia imagen
        imagen_width = 300  # Ancho de la imagen
        imagen_height = 50  # Altura de la imagen
        imagen_x = (letter[0] - imagen_width) / 2  # Centrar la imagen horizontalmente
        imagen_y = 660  # Espacio entre el título y la imagen

        c.drawImage(imagen_path, imagen_x, imagen_y, width=imagen_width, height=imagen_height)

        # Coordenadas y dimensiones del rectángulo
        rect_width = 400  # Ancho del rectángulo
        rect_height = 50  # Altura del rectángulo
        rect_x = (letter[0] - rect_width) / 2  # Centrar el rectángulo horizontalmente
        rect_y = 580 # Espacio entre la imagen y el rectángulo

        c.rect(rect_x, rect_y, rect_width, rect_height)

        # Texto que quieres agregar dentro del rectángulo
        c.setFont("Helvetica-Bold", 20)
        texto = f"Precio sugerido: ${lista_variables[1]}"

        # Alinear el texto en el centro del rectángulo
        text_width = c.stringWidth(texto, "Helvetica-Bold", 20)
        text_x = rect_x + (rect_width - text_width) / 2
        text_y = rect_y + (rect_height - 20) / 2  # Alinear verticalmente en el centro

        # Agregar texto dentro del rectángulo
        c.drawString(text_x, text_y, texto)


        # Agrega una línea separadora
        line_x1, line_y1 = 100, 440
        line_x2, line_y2 = 520, 440
        # linea
        c.line(line_x1, line_y1, line_x2, line_y2)


        c.setFont("Helvetica", 12)
        c.drawString(200, 540, f"Monto actual: ${lista_variables[0]}")
        c.drawString(200, 520, f"Monto a cobrar: {lista_variables[1]}")
        c.drawString(200, 500, f"Total de descuentos: {lista_variables[11]}%")
        c.drawString(200, 480, f"Total de descuentos en pesos: ${lista_variables[2]}")
        c.drawString(200, 460, f"Neto a percibir: ${lista_variables[3]}")

        tasas_a_STR = str(tasas_cft[programa_seleccionado]*100).replace(".",",")

        c.setFont("Helvetica", 12)
        c.drawString(100, 420, f"ACLARACIÓN: Los montos se calcularon en base al precio sugerido, lo que ")
        c.drawString(100, 410, f"permite percibir el precio de contado luego de los descuentos.")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(200, 380, f"Detalle de descuentos")
        c.setFont("Helvetica", 12)
        c.drawString(200, 360, f"Tasa del programa {programa_seleccionado} ({tasas_a_STR}%): ${lista_variables[4]}")
        c.drawString(200, 340, f"IVA (10,5%) ley 25.063: ${lista_variables[7]}")
        c.drawString(200, 320, f"II.BB (2,5%): ${lista_variables[8]}")
        c.drawString(200, 300, f"IVA RG2408 (1,5%): ${lista_variables[9]}")
        c.drawString(200, 280, f"Arancel T.Cred (1,8%): ${lista_variables[5]}")
        c.drawString(200, 260, f"IVA (21%): ${lista_variables[6]}")
        
        
        
        if (tipo_inscripcion != "Monotributista"):
            c.drawString(40, 220, f"Al estar inscripto como {tipo_inscripcion} usted recuperará ${lista_variables[10]} en concepto de IVA")

            # Guardar y cerrar el PDF
        c.save()
        pdf_buffer.seek(0)
        st.download_button("Descargar PDF", pdf_buffer, file_name="Resumen precio sugerido.pdf")


with colB:
    
    custom_css = """
        <style>
            .tarjeta {
                text-align: left;
            }
            .subheader {
                font-size: 20px;
                font-weight: bold;
            }
        </style>
        """
        # Agregar el estilo CSS personalizado utilizando st.markdown
        
    if aux == True :
        st.markdown(custom_css, unsafe_allow_html=True)
        monto_final = f"${lista_variables[1]}"
        tarjeta = f'<div class="tarjeta" style="font-size: 45px;font-weight: bold; ">${lista_variables[1]}</div>'
        st.markdown('<div class="subheader">El precio sugerido es:</div>', unsafe_allow_html=True)
        st.markdown(tarjeta, unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
        #st.write(f"El precio sugerido es:")
        #st.write(f"# $**{monto_final}**")
    else:
         st.write("")    



if aux == True : 
    st.write("---")
    st.write(f"+ ##### Monto actual: ${lista_variables[0]}")
    st.write(f"+ ##### Monto a cobrar: ${lista_variables[1]}")
    st.write(f"+ ##### Total de descuentos: {lista_variables[11]}%")
    st.write(f"+ ##### Total de descuentos en pesos: ${lista_variables[2]}")
    st.write(f"+ ##### Neto a percibir: ${lista_variables[3]}")




if aux == True : 
    st.write("---")
    st.write("**ACLARACIÓN**: Los montos se calcularon en base al precio sugerido, lo que permite percibir el precio de contado luego de los descuentos.")
    st.write("**Detalle de descuentos:**")
    st.write(f"+ Tasa del programa {programa_seleccionado} ({tasas_a_STR}%): **${lista_variables[4]}**")
    st.write(f"+ Arancel T.Cred (1,8%): **${lista_variables[5]}**")
    st.write(f"+ IVA (21%): **${lista_variables[6]}**")
    st.write(f"+ IVA (10,5%) ley 25.063: **${lista_variables[7]}**")
    st.write(f"+ II.BB (2,5%): **${lista_variables[8]}**")
    st.write(f"+ IVA RG2408 (1,5%): **${lista_variables[9]}**")
    

    if (tipo_inscripcion != "Monotributista"):
        st.write(f"**ATENCIÓN**: Al estar inscripto como {tipo_inscripcion} usted recuperará **${lista_variables[10]}** en concepto de IVA")


st.write("---")

st.markdown("Para mayor información [click aquí](https://www.argentina.gob.ar/ahora-12/comerciantes#:~:text=Ahora%2012%2032%2C97%25%20es%20la%20tasa%20m%C3%A1xima%20de,a%20aplicar%20sobre%20el%20precio%20de%20contado%201%2C664)")


# Agrega CSS personalizado para el marcador en la parte inferior
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 5px;
        text-align: left;
        font-size: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Agrega el marcador
st.markdown('<div class="footer">Desarrollado por el departamento de <a href="https://www.redcame.org.ar/" target="_blank">Estadísticas y Bases de Datos de CAME</a></div>', unsafe_allow_html=True)


st.write("---")
# Titulo para las redes
st.markdown("<h1 style='text-align: center; font-size: 22px; font-family: Verdana, sans-serif;'>¡Seguí a CAME en redes sociales!</h1>", unsafe_allow_html=True)
# Creamos las columnas para los logos de apps
st.write("")

# Agregar espacio en blanco a la izquierda

# Columnas para centrar
col_izq, col_centro, colder = st.columns([0.7,1.8,0.5])
with col_izq :
    st.write("")

with col_centro:
    colFc, colIg, colTw, colLk, colYt = st.columns(5)
    with colFc:
        # URL de tu perfil de Instagram
        facebook_url = "https://www.facebook.com/redcame"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/facebook.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width=32)
        # Crear un enlace clickeable
        st.markdown(f"[Facebook]({facebook_url})", unsafe_allow_html=True)

    with colIg:
        # URL de tu perfil de Instagram
        instagram_url = "https://www.instagram.com/redcame/"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/ig.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width=32)
        # Crear un enlace clickeable
        st.markdown(f"[Instagram]({instagram_url})", unsafe_allow_html=True)

    with colTw:
        # URL de tu perfil de Instagram
        twiter_url = "https://twitter.com/redcame"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/twiter.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width=32)
        # Crear un enlace clickeable
        st.markdown(f"[Twitter]({twiter_url})", unsafe_allow_html=True)

    with colLk:
        # URL de tu perfil de Instagram
        linkedin_url = "https://ar.linkedin.com/company/redcame"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/linkedin.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width=32)
        # Crear un enlace clickeable
        st.markdown(f"[LinkedIn]({linkedin_url})", unsafe_allow_html=True) 

    with colYt:
        # URL de tu perfil de Instagram
        youtube_url = "https://www.youtube.com/c/CAMEar"
        # Cargar la imagen del logotipo de Instagram
        logo_image = "imgs/yutu.png"  # Reemplaza con la ruta de tu imagen
        # Mostrar el logotipo de Instagram
        st.image(logo_image, width = 40)
        # Crear un enlace clickeable
        st.markdown(f"[Youtube]({youtube_url})", unsafe_allow_html=True)               

with colder :
    st.write("")
