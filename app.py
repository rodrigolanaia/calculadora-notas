from flask import Flask, render_template, request
import random

app = Flask(__name__)

def calcular_notas_controladas(promedio_deseado, minimo=0, maximo=100, diferencia_maxima=5):
    suma_deseada = int(promedio_deseado * 4)
    intentos = 0
    while True:
        intentos += 1
        base = random.randint(max(minimo, int(promedio_deseado) - diferencia_maxima),
                              min(maximo, int(promedio_deseado) + diferencia_maxima))
        notas = [random.randint(max(minimo, base - diferencia_maxima), min(maximo, base + diferencia_maxima)) for _ in range(3)]
        cuarta_nota = suma_deseada - sum(notas)
        notas_completas = notas + [cuarta_nota]

        if (
            minimo <= cuarta_nota <= maximo and
            max(notas_completas) - min(notas_completas) <= diferencia_maxima and
            all(nota != promedio_deseado for nota in notas_completas)
        ):
            random.shuffle(notas_completas)
            return notas_completas

        if intentos > 3000:
            return None

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    error = None
    if request.method == "POST":
        try:
            promedio = float(request.form["promedio"])
            notas = calcular_notas_controladas(promedio)
            if notas:
                resultado = {
                    "notas": notas,
                    "promedio_real": round(sum(notas) / 4, 2)
                }
            else:
                error = "No se pudo generar un conjunto de notas válido con esas condiciones."
        except ValueError:
            error = "Por favor, ingresa un número válido como promedio."
    return render_template("index.html", resultado=resultado, error=error)

if __name__ == "__main__":
    app.run(debug=True)
