from groq import Groq
import json
import traceback



async def implementar_IA(datos: dict):
    nombre = datos.get("datosPersonales", {}).get("nombre", "")
    apellido = datos.get("datosPersonales", {}).get("apellido", "")
    educacion = datos.get("educacion", [])
    experiencia = datos.get("experiencia", [])
    skills = datos.get("skills", [])
    idiomas = datos.get("idiomas", [])
    oferta = datos.get("ofertaDeTrabajo", {})
    descripcion_oferta = oferta.get("descripcion", "")

    prompt = f"""
Eres un experto en selección de personal. Analiza el perfil del candidato y devuelve un JSON con dos claves.

CANDIDATO: {nombre} {apellido}
- Educación: {educacion}
- Experiencia laboral: {experiencia}
- Skills: {skills}
- Idiomas: {idiomas}

{"OFERTA DE TRABAJO:" + descripcion_oferta if descripcion_oferta else "Sin oferta de trabajo."}

INSTRUCCIONES PARA EL PORCENTAJE:
- Compara las skills, experiencia e idiomas del candidato con los requisitos de la oferta.
- El porcentaje refleja cuántos requisitos de la oferta cumple el candidato (no si es perfecto para el puesto).
- Si el candidato tiene alguna skill o tecnología que pide la oferta, suma puntos.
- Si tiene experiencia en el sector, suma puntos.
- Si tiene los idiomas requeridos, suma puntos.
- El MÍNIMO es 10 aunque no cumpla nada. El MÁXIMO es 100.
- Sé realista pero generoso: un candidato con Angular para una oferta de Angular debe sacar al menos 30.

INSTRUCCIONES PARA LA DESCRIPCIÓN:
- Redacta un único párrafo de 4 a 6 líneas en primera persona.
- Tono profesional, natural y seguro, como si el candidato se estuviera presentando en una entrevista.
- Debe sonar específico y realista, evitando frases vacías o clichés tipo “soy proactivo” o “me apasiona la tecnología” sin contexto.
- Incluye de forma integrada la experiencia, tecnologías, sectores o tipos de proyectos en los que ha trabajado.
- Destaca fortalezas técnicas concretas (frameworks, lenguajes, herramientas, metodologías) si aparecen en el perfil.
- No uses listas, asteriscos ni formato markdown.
- No repitas literalmente el CV; reformúlalo de manera fluida y coherente.
- Evita exageraciones irreales, pero presenta el perfil de forma atractiva y convincente.

Devuelve SOLO este JSON sin nada más:
{{"descripcion": "...", "porcentaje": 42}}
"""

    try:
        client = Groq(api_key="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")
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        contenido = respuesta.choices[0].message.content.strip()
        print("RESPUESTA IA RAW:", contenido)

        if contenido.startswith("```"):
            contenido = contenido.split("```")[1]
            if contenido.startswith("json"):
                contenido = contenido[4:]
            contenido = contenido.strip()

        resultado = json.loads(contenido)
        descripcion = resultado.get("descripcion", "")
        porcentaje = max(10, min(100, int(resultado.get("porcentaje", 50))))
        print(f"PORCENTAJE FINAL: {porcentaje}")
        return descripcion, porcentaje

    except Exception as e:
        print(f"Error en IA: {e}")
        traceback.print_exc()
        return "", 50