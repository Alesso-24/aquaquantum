# Archivo: app.py
import streamlit as st
import time
from motor_cuantico import generar_clave_cuantica

# Configuración de página con diseño profesional y minimalista
st.set_page_config(page_title="Quantum Dashboard", layout="centered")

st.title("🚀 Panel de Control Cuántico")
st.write("Generador de claves criptográficas utilizando superposición de Qubits.")
st.divider()

# Controles de la interfaz
longitud = st.slider(
    "Selecciona la longitud de la clave (Número de Qubits)",
    min_value=4,
    max_value=24,
    value=8,
)

# Botón de acción
if st.button("Generar Clave Segura", type="primary"):
    with st.spinner("Procesando en el simulador cuántico..."):
        time.sleep(0.5)  # Pequeña pausa para efecto visual

        # Llamamos a nuestro otro archivo Python
        clave_binaria = generar_clave_cuantica(longitud)

        # Convertimos el binario a hexadecimal para que se vea más pro
        clave_hex = hex(int(clave_binaria, 2))[2:].upper()

        st.success("¡Colapso de superposición exitoso!")

        # Mostramos los datos en columnas limpias
        col1, col2 = st.columns(2)
        col1.metric(label="Binario Puro (Lectura del sensor)", value=clave_binaria)
        col2.metric(label="Token Hexadecimal", value=clave_hex)

        st.info(
            "Nota técnica: A diferencia de los números pseudoaleatorios clásicos, estos bits provienen de la incertidumbre fundamental modelada por compuertas Hadamard."
        )
