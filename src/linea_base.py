"""Línea base: TF-IDF (1-2 gramas de palabras) + regresión logística. Métrica principal: macro-F1 (3 clases).
Reporta F1 global y por subgrupo (región, expresiones costeñas) con intervalos bootstrap y la brecha ΔF1.
Resultados en experiments/E1_tfidf_lr/."""
import argparse, json, os, time
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, classification_report, confusion_matrix

CLASES = ["negativa", "neutra", "positiva"]

def bootstrap_f1(y, yhat, n=1000, seed=42):
    rng = np.random.default_rng(seed); y = np.asarray(y); yhat = np.asarray(yhat); vals = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        vals.append(f1_score(y[i], yhat[i], average="macro", labels=CLASES))
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))

def eval_subgrupo(df, yhat):
    f = f1_score(df.clase, yhat, average="macro", labels=CLASES)
    lo, hi = bootstrap_f1(df.clase, yhat)
    return {"n": int(len(df)), "macro_f1": round(f, 4), "ic95": [round(lo, 4), round(hi, 4)],
            "n_por_clase": {k: int(v) for k, v in df.clase.value_counts().items()}}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--semilla", type=int, default=42)
    ap.add_argument("--C", type=float, default=1.0)
    a = ap.parse_args()
    df = pd.read_csv("data/particion.csv")
    tr, va, te = df[df.split == "train"], df[df.split == "val"], df[df.split == "test"]
    t0 = time.time()
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_features=200000, sublinear_tf=True)
    Xtr = vec.fit_transform(tr.text)
    clf = LogisticRegression(C=a.C, max_iter=2000, class_weight="balanced", random_state=a.semilla)
    clf.fit(Xtr, tr.clase)
    seg = time.time() - t0
    out = {"experimento": "E1_tfidf_lr", "semilla": a.semilla,
           "hiperparametros": {"ngram": [1, 2], "min_df": 3, "max_features": 200000, "C": a.C, "class_weight": "balanced"},
           "tiempo_entrenamiento_s": round(seg, 1), "n_train": int(len(tr))}
    for nombre, d in [("val", va), ("test", te)]:
        yhat = clf.predict(vec.transform(d.text))
        out[nombre] = {"global": eval_subgrupo(d, yhat),
                       "por_region": {r: eval_subgrupo(d[d.region == r], yhat[(d.region == r).values]) for r in ["caribe", "andina", "sin_identificar"]},
                       "por_costeno": {str(c): eval_subgrupo(d[d.costeno == c], yhat[(d.costeno == c).values]) for c in [0, 1]},
                       "reporte": classification_report(d.clase, yhat, labels=CLASES, output_dict=True, zero_division=0),
                       "matriz_confusion": confusion_matrix(d.clase, yhat, labels=CLASES).tolist()}
        pr = out[nombre]["por_region"]
        out[nombre]["delta_f1_andina_menos_caribe"] = round(pr["andina"]["macro_f1"] - pr["caribe"]["macro_f1"], 4)
    mayor = tr.clase.mode()[0]
    out["clasificador_mayoritario_test"] = {"clase": mayor, "macro_f1": round(f1_score(te.clase, [mayor] * len(te), average="macro", labels=CLASES), 4)}
    os.makedirs("experiments/E1_tfidf_lr", exist_ok=True)
    json.dump(out, open(f"experiments/E1_tfidf_lr/resultados_semilla{a.semilla}.json", "w"), indent=2, ensure_ascii=False)
    yhat = clf.predict(vec.transform(te.text))
    err = te.assign(prediccion=yhat)[te.clase != yhat][["text", "clase", "prediccion", "region", "costeno"]].sample(60, random_state=a.semilla)
    err.to_csv("experiments/E1_tfidf_lr/muestra_errores_test.csv", index=False)
    g, m = out["test"]["global"], out["clasificador_mayoritario_test"]
    print(f"Macro-F1 test: {g['macro_f1']} IC95 {g['ic95']} | mayoritario: {m['macro_f1']} | entrenamiento {seg:.0f} s")
    for r, v in out["test"]["por_region"].items():
        print(f"  {r:16s} n={v['n']:5d} macro-F1={v['macro_f1']} IC95={v['ic95']} clases={v['n_por_clase']}")
    print(f"  ΔF1 (andina - caribe) = {out['test']['delta_f1_andina_menos_caribe']}")
    for c, v in out["test"]["por_costeno"].items():
        print(f"  costeno={c} n={v['n']:5d} macro-F1={v['macro_f1']} IC95={v['ic95']}")
    print("por clase (test):", {k: round(v["f1-score"], 3) for k, v in out["test"]["reporte"].items() if k in CLASES})

if __name__ == "__main__":
    main()
