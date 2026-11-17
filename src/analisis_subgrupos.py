"""Comparación Caribe vs andina controlando el tipo de lugar (solo atractivos), con la línea base E1."""
import json, numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
CLASES = ["negativa", "neutra", "positiva"]
df = pd.read_csv("data/particion.csv"); tr, te = df[df.split == "train"], df[df.split == "test"]
vec = TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_features=200000, sublinear_tf=True)
clf = LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced", random_state=42).fit(vec.fit_transform(tr.text), tr.clase)
te = te.assign(pred=clf.predict(vec.transform(te.text)))
rng = np.random.default_rng(42); out = {}
for r in ["caribe", "andina"]:
    d = te[(te.region == r) & (te.type == "Attractive")]
    f = f1_score(d.clase, d.pred, average="macro", labels=CLASES)
    b = [f1_score(d.clase.values[i], d.pred.values[i], average="macro", labels=CLASES) for i in (rng.integers(0, len(d), len(d)) for _ in range(1000))]
    out[r] = {"n": int(len(d)), "macro_f1": round(f, 4), "ic95": [round(np.percentile(b, 2.5), 4), round(np.percentile(b, 97.5), 4)], "n_por_clase": {k: int(v) for k, v in d.clase.value_counts().items()}}
out["delta_f1_andina_menos_caribe"] = round(out["andina"]["macro_f1"] - out["caribe"]["macro_f1"], 4)
json.dump(out, open("experiments/E1_tfidf_lr/subgrupos_solo_atractivos.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps(out, indent=2, ensure_ascii=False))
