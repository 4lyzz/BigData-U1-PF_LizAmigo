from flask import Flask, render_template, request
from scripts import (
    cargar_datos,
    obtener_opciones_filtro,
    manipular_datos,
    calcular_resumen,
    generar_graficos,
)

app = Flask(__name__)
DF_BASE = cargar_datos("kpopgroups.csv")


@app.route("/")
def index():
    genero = request.args.get("genero", "")
    estado = request.args.get("estado", "")
    empresa = request.args.get("empresa", "")
    buscar = request.args.get("buscar", "")
    ordenar_por = request.args.get("ordenar_por", "Name")
    orden = request.args.get("orden", "asc")
    detalle = request.args.get("detalle", "compacto")

    opciones = obtener_opciones_filtro(DF_BASE)
    df_filtrado = manipular_datos(
        DF_BASE,
        genero=genero,
        estado=estado,
        empresa=empresa,
        buscar=buscar,
        ordenar_por=ordenar_por,
        orden=orden,
    )
    resumen = calcular_resumen(df_filtrado)
    graficos = generar_graficos(df_filtrado)

    grupos = df_filtrado.to_dict(orient="records")

    filtros = {
        "genero": genero,
        "estado": estado,
        "empresa": empresa,
        "buscar": buscar,
        "ordenar_por": ordenar_por,
        "orden": orden,
        "detalle": detalle,
    }

    return render_template(
        "index.html",
        grupos=grupos,
        opciones=opciones,
        resumen=resumen,
        graficos=graficos,
        filtros=filtros,
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)