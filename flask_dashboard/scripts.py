#   python app.py

import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def cargar_datos(ruta_csv="kpopgroups.csv"):
    df = pd.read_csv(ruta_csv)

    df["Short"] = df["Short"].fillna("—")
    df["Fanclub Name"] = df["Fanclub Name"].fillna("No registrado")
    df["Company"] = df["Company"].fillna("Sin agencia")
    df["Debut"] = df["Debut"].fillna("Sin fecha")

    reemplazo_estado = {
        "Yes": "Activo",
        "No": "Inactivo",
    }
    df["Active"] = df["Active"].replace(reemplazo_estado)

    fechas = pd.to_datetime(df["Debut"], format="%d/%m/%Y", errors="coerce")
    df["Debut_Year"] = fechas.dt.year.fillna(0).astype(int)

    df["Cambio_Miembros"] = df["Members"] - df["Orig Memb"]

    return df


def obtener_opciones_filtro(df):
    generos = sorted(df["Gender"].dropna().unique().tolist())
    estados = sorted(df["Active"].dropna().unique().tolist())
    empresas = sorted(df["Company"].dropna().unique().tolist())

    opciones = {
        "generos": generos,
        "estados": estados,
        "empresas": empresas,
    }
    return opciones


def manipular_datos(df, genero="", estado="", empresa="", buscar="", ordenar_por="Name", orden="asc"):
    datos = df.copy()

    if genero != "":
        datos = datos[datos["Gender"] == genero]

    if estado != "":
        datos = datos[datos["Active"] == estado]

    if empresa != "":
        datos = datos[datos["Company"] == empresa]

    if buscar.strip() != "":
        texto = buscar.strip().lower()
        coincide_nombre = datos["Name"].astype(str).str.lower().str.contains(texto, na=False)
        coincide_coreano = datos["Korean Name"].astype(str).str.lower().str.contains(texto, na=False)
        coincide_empresa = datos["Company"].astype(str).str.lower().str.contains(texto, na=False)
        coincide_fandom = datos["Fanclub Name"].astype(str).str.lower().str.contains(texto, na=False)
        datos = datos[coincide_nombre | coincide_coreano | coincide_empresa | coincide_fandom]

    columnas_validas = ["Name", "Debut_Year", "Members", "Orig Memb", "Cambio_Miembros", "Company"]
    if ordenar_por not in columnas_validas:
        ordenar_por = "Name"

    ascendente = True
    if orden == "desc":
        ascendente = False

    datos = datos.sort_values(by=ordenar_por, ascending=ascendente)
    return datos


def calcular_resumen(df_filtrado):
    total = len(df_filtrado)
    activos = int((df_filtrado["Active"] == "Activo").sum())

    if total > 0:
        media_miembros = round(float(df_filtrado["Members"].mean()), 1)
    else:
        media_miembros = 0

    con_cambios = int((df_filtrado["Cambio_Miembros"] != 0).sum())

    resumen = {
        "total": total,
        "activos": activos,
        "media_miembros": media_miembros,
        "con_cambios": con_cambios,
    }
    return resumen


def generar_graficos(df_filtrado, carpeta_graficos="static/charts"):
    os.makedirs(carpeta_graficos, exist_ok=True)
    graficos = {}

    if df_filtrado.empty:
        return graficos

    plt.figure(figsize=(8, 4))
    top_empresas = df_filtrado["Company"].value_counts().head(10).iloc[::-1]
    plt.barh(top_empresas.index, top_empresas.values, color="#6c5ce7")
    plt.title("Top 10 agencias por número de grupos")
    plt.xlabel("Número de grupos")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_graficos, "top_empresas.png"), dpi=120)
    plt.close()
    graficos["top_empresas"] = "charts/top_empresas.png"

    plt.figure(figsize=(6, 4))
    estados = df_filtrado["Active"].value_counts()
    plt.bar(estados.index, estados.values, color="#00b894")
    plt.title("Estado actual de los grupos")
    plt.ylabel("Cantidad de grupos")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_graficos, "estados.png"), dpi=120)
    plt.close()
    graficos["estados"] = "charts/estados.png"

    plt.figure(figsize=(7, 4))
    miembros = df_filtrado["Members"].value_counts().sort_index()
    plt.bar(miembros.index.astype(str), miembros.values, color="#fd79a8")
    plt.title("Distribución de miembros actuales por grupo")
    plt.xlabel("Miembros actuales")
    plt.ylabel("Número de grupos")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_graficos, "miembros.png"), dpi=120)
    plt.close()
    graficos["miembros"] = "charts/miembros.png"

    return graficos