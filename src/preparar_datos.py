"""Prepara el subconjunto colombiano de Rest-Mex 2023 con tres clases y subgrupos regionales.

Uso:
    python src/preparar_datos.py --entrada data/Rest_Mex_Sentiment_Analysis_2023_Train.xlsx

El archivo de Rest-Mex NO se redistribuye (uso académico por solicitud a los organizadores).
Salida: data/colombia.csv con columnas text, polarity, clase, type, region, costeno.
"""
import argparse
import pandas as pd

# Listas fijadas ANTES de evaluar (hito 1). Se buscan en minúsculas sobre título + reseña.
CARIBE = [r"cartagena", r"santa marta", r"barranquilla", r"san andr[eé]s", r"tayrona", r"rodadero",
          r"\bbar[uú]\b", r"islas? del rosario", r"getseman[ií]", r"bocagrande", r"minca", r"palomino",
          r"taganga", r"ciudad amurallada", r"castillo de san felipe", r"playa blanca", r"la boquilla"]
ANDINA = [r"bogot[aá]", r"medell[ií]n"]
# Glosario costeño mínimo (v0) para marcar reseñas con expresiones costeñas; se amplía con el glosario del proyecto.
COSTENO = [r"\bbacano\b", r"\bbacana\b", r"\bmamar gallo\b", r"\bmamando gallo\b", r"\bese man\b", r"\bla seño\b",
           r"\bcorroncho", r"\bcachaco", r"\btumbalocas\b", r"\bqu[eé] nota\b", r"\bbuena vibra\b",
           r"\bvaina\b", r"\bpelao\b", r"\bpelaos\b", r"\bech[eé]\b", r"\berda\b", r"\bnojoda\b", r"\bajá\b"]

def clase(p):
    return "negativa" if p <= 2 else ("neutra" if p == 3 else "positiva")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True, help="Ruta al archivo xlsx o csv de entrenamiento de Rest-Mex 2023")
    ap.add_argument("--salida", default="data/colombia.csv")
    a = ap.parse_args()
    df = pd.read_excel(a.entrada) if a.entrada.endswith(".xlsx") else pd.read_csv(a.entrada)
    df = df[df["Country"] == "Colombia"].copy()
    df["text"] = (df["Title"].astype(str).str.strip() + ". " + df["Review"].astype(str).str.strip())
    df = df.drop_duplicates(subset=["text"])
    df["clase"] = df["Polarity"].astype(int).map(clase)
    low = df["text"].str.lower()
    car = low.str.contains("|".join(CARIBE), regex=True)
    an = low.str.contains("|".join(ANDINA), regex=True)
    df["region"] = "sin_identificar"
    df.loc[an & ~car, "region"] = "andina"
    df.loc[car & ~an, "region"] = "caribe"
    df["costeno"] = low.str.contains("|".join(COSTENO), regex=True).astype(int)
    out = df.rename(columns={"Polarity": "polarity", "Type": "type"})[["text", "polarity", "clase", "type", "region", "costeno"]]
    out.to_csv(a.salida, index=False)
    print(f"{len(out)} reseñas guardadas en {a.salida}")
    print(out["clase"].value_counts().to_string())
    print(out["region"].value_counts().to_string())
    print("con expresiones costeñas:", int(out["costeno"].sum()))

if __name__ == "__main__":
    main()
