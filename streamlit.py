# Importamos las librerias a utilizar
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime
import pytz
import time
import pandas as pd

        
# Configuramos la página
st.set_page_config(
    page_title="Calculadora Ahora 12",
    page_icon="imgs/CAME-Transparente.ico.ico",
    )

# Creamos la tasa de interés
tasas_cft = {"1 Cuota" : 0.0,
         "Ahora 03" : 0.1024 ,
         "Ahora 06" : 0.1887 ,
         "Ahora 12" : 0.3297 , 
         "Ahora 18" : 0.4380 ,
         "Ahora 24"  : 0.5221}
# Aux = False
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

if monto_credito == "" or monto_credito == "$" or monto_credito == " " : 
    aux3 = False 
elif monto_credito == "0":
    aux3 = False
    st.markdown("<span style='color: red;'>Ingrese un monto válido porfavor.</span>", unsafe_allow_html=True)
else:
    try:
        monto_credito = float(monto_credito)
        aux3 = True
    except ValueError:
        aux3 = False        
        st.markdown("<span style='color: red;'>Ingrese un monto válido porfavor.</span>", unsafe_allow_html=True)

st.write("---")

# listado de provincias
provincias = [
    "-",
    "Buenos Aires",
    "CABA",
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

# Seleccionar provincia
provincia_seleccionada = st.selectbox("Seleccione la provincia",provincias)  
if provincia_seleccionada == "-":
    aux_seleccionar_provincia = False
else:
    aux_seleccionar_provincia = True
    
st.write("---")

# Seleccionar el programa
programas = ["-", "1 Cuota","Ahora 03","Ahora 06","Ahora 12","Ahora 18","Ahora 24"]
programa_seleccionado = st.selectbox("Seleccione el programa",programas)    
if programa_seleccionado == "-":
    aux_programa = False
else:
    aux_programa = True

st.write("---")

# Seleccionar tipo de inscripción
inscripciones = ["-", "Monotributista", "Responsable Inscripto", "Sociedad"]
tipo_inscripcion = st.selectbox("Seleccione el tipo de inscripción",inscripciones)
if tipo_inscripcion == "-":
    aux_inscripcion = False
else:
    aux_inscripcion = True

st.write("---")

# Cambiamos un poco esto 
inscripcion_seleccionada = ""

if (tipo_inscripcion == "Responsable Inscripto") or (tipo_inscripcion == "Sociedad"): 
    inscripcion_seleccionada = "Responsable"
elif (tipo_inscripcion == "Monotributista"):
    inscripcion_seleccionada = "Monotributista"
else:
    pass    

colA, colB = st.columns([1,2])
with colA : 
    if st.button("Calcular"):
        if aux3 == True :
            if (aux_seleccionar_provincia == True) and (aux_programa == True) and (aux_inscripcion == True):
                # Creamos la combinación de variables
                variables = provincia_seleccionada + " " + programa_seleccionado + " " + inscripcion_seleccionada   

                # OBTENEMOS LOS COEFICIENTES    
                df = pd.read_csv("Datos/coeficientes_provincias.csv")
                coeficiente = df.loc[df["Conjunto"].str.contains(variables, case=False)]["Coeficiente"]
                coeficiente = coeficiente.iloc[0]    
                    
                # OBTENEMOS LA TASA DEL PROGRAMA
                tasa_programa = tasas_cft[programa_seleccionado]
                    
                # ---
                # LIQUIDACIÓN DE PAGO
                # ---
                
                # PRIMER CALCULO
                precio_sugerido = monto_credito * coeficiente
                
                # SEGUNDO CALCULO   
                arancel_1_8 = 0.018 * precio_sugerido
                
                # TERCER CALCULO
                costo_financiero = tasa_programa * precio_sugerido
                
                # CUARTO CALCULO
                iva_arancel = 0.21 * arancel_1_8
                
                # QUINTO CALCULO
                iva_costo_financiero = costo_financiero * 0.105
                
                # CALCULAMOS EL SUBTOTAL
                subtotal = precio_sugerido - (arancel_1_8 + costo_financiero + iva_arancel+ iva_costo_financiero )
                
                # SEXTO CALCULO
                iva_rg = subtotal * 0.03
                
                # CALCULAMOS EL TOTAL COBRADO EN LA LIQUIDACIÓN
                total_cobrado_liquidacion = subtotal - iva_rg

                # ---
                # CALCULO DE IMPUESTOS 
                # ---
                
                # Definimos la tasa municipal
                porcentaje_municipal = 0.01
                
                if "Monotributista" in variables:
                    # PRIMER CALCULO
                    venta_neta_iva = 0
                
                    # SEGUNDO CALCULO
                    iva_debito = 0
                
                    # TERCER CALCULO
                    iva_credito = 0
                
                    # CUARTO CALCULO
                    posicion_iva = 0
                
                    # QUINTO CALCULO
                    saldo_cobrado = total_cobrado_liquidacion - posicion_iva
                
                elif "Responsable" in variables:
                    # PRIMER CALCULO
                    venta_neta_iva = precio_sugerido / (1+ 0.21)
                
                    # SEGUNDO CALCULO
                    iva_debito = venta_neta_iva * 0.21
                
                    # TERCER CALCULO
                    iva_credito = iva_arancel + iva_costo_financiero + iva_rg
                
                    # CUARTO CALCULO
                    posicion_iva = iva_debito - iva_credito
                
                    # QUINTO CALCULO
                    saldo_cobrado = total_cobrado_liquidacion - posicion_iva
                
                # SEXTO
                if "Monotributista" in variables:
                    tasa_municipal = precio_sugerido * porcentaje_municipal
                
                elif "Responsable" in variables:
                    tasa_municipal = venta_neta_iva * porcentaje_municipal
                
                
                # OBTENEMOS LA ALICUOTA
                alicuota = df.loc[df["Conjunto"].str.contains(variables, case=False)]["Alicuota"]
                alicuota = alicuota.iloc[0]
                    
                # SEPTIMO CALCULO
                if "Monotributista" in variables:
                    iibb = precio_sugerido * alicuota
                
                elif "Responsable" in variables:
                    iibb = venta_neta_iva * alicuota

                # OCTAVO CALCULO
                utilidad_antes_de_costos = saldo_cobrado - tasa_municipal - iibb

                # DEFINIMOS ALGUNAS VARIABLES
                total_descuento_pesos = precio_sugerido - monto_credito
                tasas_a_STR = str(tasas_cft[programa_seleccionado]*100).replace(".",",")
                alicuota_a_STR = str(alicuota *100).replace(".",",")
                    
                # Creamos lista de variables
                lista_variables = [monto_credito, precio_sugerido, arancel_1_8, costo_financiero, iva_arancel, iva_costo_financiero, subtotal, iva_rg, total_cobrado_liquidacion, venta_neta_iva, iva_debito, iva_credito, posicion_iva, saldo_cobrado, tasa_municipal, iibb, utilidad_antes_de_costos, total_descuento_pesos]
                    
                # iteramos para el formato
                for i in range (len(lista_variables)) :
                    lista_variables[i] = '{:,.2f}'.format(lista_variables[i]).replace(',', ' ')
                    lista_variables[i] = lista_variables[i].replace(".",",")
                    lista_variables[i] = lista_variables[i].replace(" ",".")

                # COLOCAMOS TRUE AL AUXILIAR PARA AVANZAR    
                aux = True    
            else:
               # Utiliza st.markdown para cambiar el color del texto
                st.markdown("<span style='color: red;'>Complete las variables.</span>", unsafe_allow_html=True)
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
        line_x1, line_y1 = 100, 280
        line_x2, line_y2 = 520, 280
        # linea
        c.line(line_x1, line_y1, line_x2, line_y2)

        # Define las coordenadas del cuadrado
        x1, y1 = 90, 330  # Esquina superior izquierda
        x2, y2 = 400, 540  # Esquina inferior derecha
        
        # Dibuja el cuadrado
        c.rect(x1, y1, x2 - x1, y2 - y1)
            
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 560, "Liquidación de pago")   
            
        c.setFont("Helvetica", 12)   
        c.drawString(100, 520, f"Venta a precio de contado: ${lista_variables[0]}")   
        c.drawString(100, 500, f"Financiado en {programa_seleccionado}: ${lista_variables[1]}")   
        c.drawString(100, 480, f"Provincia: {provincia_seleccionada}")   
        c.drawString(100, 460, f"AFIP: {tipo_inscripcion}")   
        c.drawString(100, 440, f"Arancel 1,8%: ${lista_variables[2]}")   
        c.drawString(100, 420, f"Costo Financiero del programa ({tasas_a_STR}): ${lista_variables[3]}")   
        c.drawString(100, 400, f"IVA Arancel (21%): ${lista_variables[4]}")   
        c.drawString(100, 380, f"IVA Costo Financiero (10,50%): ${lista_variables[5]}")   
        c.drawString(100, 360, f"Venta a precio de contado")   
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 340, f"Subtotal {lista_variables[6]}")
        c.setFont("Helvetica", 12)
        c.drawString(100, 320, f"IVA RG 140/98 (3%) {lista_variables[7]}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 300, f"Cálculo de impuestos")
            
        c.setFont("Helvetica", 12)


        # Guardar y cerrar el PDF
        c.save()
        pdf_buffer.seek(0)
        st.download_button("Descargar PDF", pdf_buffer, file_name="Resumen precio sugerido.pdf")
         
# ESCRIBIMOS RESULTADOS
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
        tarjeta = f'<div class="tarjeta" style="font-size: 45px;font-weight: bold; ">${lista_variables[1]}</div>'
        st.markdown('<div class="subheader">El precio sugerido a cobrar es:</div>', unsafe_allow_html=True)
        st.markdown(tarjeta, unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
        #st.write(f"El precio sugerido es:")
        #st.write(f"# $**{monto_final}**")
    else:
         st.write("")    



if aux == True : 
    st.write("---")
    st.write(f"+ ##### Precio de contado: ${lista_variables[0]}")
    st.write(f"+ ##### Precio sugerido a cobrar: ${lista_variables[1]}")
    st.write(f"+ ##### Total de descuentos en pesos: ${lista_variables[17]}")

if aux == True : 
    st.write("---")
    st.write("**ACLARACIÓN**: Los montos se calcularon en base al precio sugerido, aplicando los descuentos correspondientes al programa seleccionado, IVA, IIBB y la tasa municipal.")
    st.write("**Detalle de descuentos:**")
    st.write(f"+ Tasa del programa {programa_seleccionado} ({tasas_a_STR}%): **${lista_variables[3]}**")
    st.write(f"+ Arancel T.Cred (1,8%): **${lista_variables[2]}**")
    st.write(f"+ IVA (21%): **${lista_variables[4]}**")
    st.write(f"+ IVA (10,5%) ley 25.063: **${lista_variables[5]}**")
    st.write(f"###### **Subtotal: ${lista_variables[6]}**")   
    st.write(f"+ IVA RG 140/98 (3%): **${lista_variables[7]}**") 
    st.write(f"+ **Liquidación: ${lista_variables[8]}**") 
    st.write("---")
    st.write(f"+ Venta neta de IVA: **${lista_variables[9]}**")     
    st.write(f"+ IVA Débito: **${lista_variables[10]}**")     
    st.write(f"+ IVA Crédito: **${lista_variables[11]}**") 
    st.write(f"###### **Posición IVA: ${lista_variables[12]}**")   
    st.write(f"+ Tasa Municipal (1%): **${lista_variables[14]}**")     
    st.write(f"+ II.BB para {provincia_seleccionada} (Alícuota Gral: {alicuota_a_STR}%): **${lista_variables[15]}**")
    st.write(f"##### **Utilidad Antes de Costos e IIGG**: ${lista_variables[16]}")
        
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

# Marca de versión en la parte inferior con CSS personalizado
st.markdown(
    """
    <div style="font-size: 6px; text-align: left;">
        v1.1.3
    </div>
    """,
    unsafe_allow_html=True
)
