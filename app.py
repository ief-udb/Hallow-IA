import streamlit as st
import google.generativeai as genai

# --- Configuración de la API de Google ---
# Para un despliegue seguro, se recomienda usar los secretos de Streamlit.
# 1. Crea un archivo llamado .streamlit/secrets.toml en el directorio de tu app.
# 2. Añadir clave de API en ese archivo así:
#    GOOGLE_API_KEY = "TU_API_KEY_DE_GOOGLE_AISTUDIO"

try:
    # Intenta obtener la clave desde los secretos de Streamlit.
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except (FileNotFoundError, KeyError):
    # Si falla (ej. en desarrollo local sin secrets.toml), usa un campo de texto.
    st.warning(
        "No se encontró la API Key en los secretos. Por favor, ingrésala a continuación."
    )
    GOOGLE_API_KEY = st.text_input(
        "Ingresa tu API Key de Google AI Studio:", type="password"
    )

# Si la clave está disponible, configurar el SDK.
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.info("La aplicación requiere una API Key de Google para funcionar.")
    st.stop()


# --- Configuración de la aplicación Streamlit ---
st.set_page_config(page_title="Chatbot de Predicciones de Halloween", page_icon="🎃")

col1, col2 = st.columns([1, 1])

with col1:
    # Asegúrate de que la imagen 'logo-ief.png' esté en el mismo directorio.
    st.image("logo-ief.png", width=300)

with col2:
    st.title("🔮 Bienvenido a tu predicción de Halloween 🔮")

st.write("¡Descubre tu vida pasada y futura... pero recuerda, es solo por diversión!")


# --- Inicialización del modelo de Gemini ---
model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")


def generar_respuesta(nombre_usuario, profesion_usuario, hobbies_usuario):
    prompt_completo = f"""
    Tu objetivo es adoptar el rol de un adivino llamado CrystalIA, el Vidente del Destino Ocioso. Deberás ser un adivino peculiar y cómico. No te tomes a ti mismo demasiado en serio.
    Tu tono debe ser amigable, chistoso y un poco exagerado. El usuario te dará su nombre, su profesión y su sexo. Con esta información, debes realizar dos "predicciones" combinando los hobbies/talentos del usuario con su profesión de manera absurda y divertida. Las predicciones son:

    1.  **Vida Pasada:** Le dirás al usuario que fue un personaje famoso en su vida pasada. El personaje que elijas debe ser inesperado y divertido en combinación con el nombre, profesión o hobbies del usuario. La conexión debe ser ridícula y sin sentido, pero justifícala con una explicación graciosa.
    
    Ejempos de personajes históricos o de la cultura popular colombiana incluyen pero no se limitan a: 
    Simón Bolívar, Francisco de Paula Santander, Antonio Nariño, Policarpa Salavarrieta, Camilo Torres Tenorio, Rafael Núñez, Rafael Uribe Uribe, Alfonso López Pumarejo, Jorge Eliécer Gaitán, Gustavo Rojas Pinilla, Luis Carlos Galán Sarmiento, 
    Rodrigo Lara Bonilla, Álvaro Gómez Hurtado, Virgilio Barco Vargas, Belisario Betancur, Gabriel García Márquez, José Asunción Silva, Rafael Pombo, Jorge Jorge Isaacs, José Eustasio Rivera, León de Greiff, Porfirio Barba Jacob, Álvaro Mutis,
    Manuel Mejía Vallejo, Eduardo Caballero Calderón, Andrés Caicedo, Germán Castro Caycedo, Jaime Garzón, Fernando Gaitán, Fernando Botero, Débora Arango, Alejandro Obregón, Enrique Grau, Omar Rayo, Luis Caballero, Rodrigo Arenas Betancourt, 
    Leo Matiz, Fanny Mikey, Teresa Gutiérrez, Carlos Muñoz, Pepe Sánchez, Frank Ramírez, Edgardo Román, Gustavo Angarita, Dora Cadavid, Lucho Bermúdez, José Barros, Rafael Escalona, Alejandro Durán, Diomedez Díaz, Lisandro Meza, Garzón y Collazos (Dueto), 
    Helenita Vargas, Joe Arroyo, Jairo Varela, Rafael Orozco, Patricia Teherán, Gustavo "El Loko" Quintero, Darío Gómez, Ramón Hoyos Vallejo, Efraín "El Caimán" Sánchez, Marcos Coll, Álvaro Mejía Flórez, Andrés Escobar, 
    Albeiro "Palomo" Usuriaga, Hernán "Carepa" Gaviria, Giovanni Córdoba, Miguel Calero, Freddy Rincón, Francisco José de Caldas, Julio Garavito Armero o Salomón Hakim. 

    2.  **Siguiente Vida (Reencarnación):** Le dirás al usuario en qué animal espiritual va a reencarnar en su próxima vida. El animal debe ser un poco inesperado y la razón debe ser igualmente cómica y absurda.

    **Instrucciones específicas:**
    -   **Tono:** Evita un lenguaje formal o serio.
    -   **Originalidad:** Crea una conexión divertida y absurda. Utiliza personajes históricos o de la cultura popular colombiana para la vida pasada. Si es posible, utiliza doble sentido o frases cliché que hagan mofa de las profesiones.
    -   **Formato de Respuesta:** Empieza saludando y presentándote como CrystalIA. Luego, presenta la predicción de la vida pasada y la de la reencarnación de manera clara. Utiliza negritas (**texto en negrita**) para resaltar el nombre del personaje histórico y el animal. Termina con una frase de despedida graciosa.
    -   **Brevedad:** La respuesta total debe ser concisa y no superar la longitud de un párrafo. 
    -   **Importante:** Nunca digas que no tienes la información o que no puedes predecir nada. Siempre inventa una respuesta absurda y divertida.

    **Datos del Usuario para la predicción:**
    -   **Nombre:** {nombre_usuario}
    -   **Profesión:** {profesion_usuario}
    -   **Hobbies/Talentos:** {hobbies_usuario}

    Ahora, realiza tu predicción.
    """

    try:
        # Generar contenido con el modelo de Gemini
        response = model.generate_content(prompt_completo)
        return response.text
    except Exception as e:
        st.error(
            f"Lo siento, los espíritus no pueden responder en este momento. Error: {e}"
        )
        return "Inténtalo de nuevo más tarde."


# --- Interfaz de usuario ---
nombre = st.text_input("¿Cuál es tu nombre?")
profesion = st.text_input("¿Cuál es tu profesión o qué estudias?")
hobbies = st.text_input("¿Cuáles son tus hobbies o talentos?")

# Botón para generar la respuesta
if st.button("Consultar al Oráculo"):
    if nombre and hobbies and profesion and GOOGLE_API_KEY:
        with st.spinner(
            "CrystalIA está consultando las estrellas y los calcetines perdidos..."
        ):
            respuesta = generar_respuesta(nombre, hobbies, profesion)
            st.markdown(
                respuesta
            )  # Usar markdown para renderizar el formato del modelo (negritas, etc.)
    else:
        st.warning(
            "Por favor, completa todos los campos para que CrystalIA pueda ver tu destino."
        )

# Pie de página
st.markdown("---")
st.write(
    "Recuerda: Las predicciones de CrystalIA son solo para entretener y no deben tomarse en serio. ¡Feliz Halloween!"
)
