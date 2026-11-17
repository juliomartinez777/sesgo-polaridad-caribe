"""Partición 70/15/15 estratificada por clase y región, con semilla fija. Se guarda en data/particion.csv."""
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default="data/colombia.csv")
    ap.add_argument("--semilla", type=int, default=42)
    a = ap.parse_args()
    df = pd.read_csv(a.entrada)
    estrato = df["clase"] + "_" + df["region"]
    tr, resto = train_test_split(df.index, test_size=0.30, random_state=a.semilla, stratify=estrato)
    val, te = train_test_split(resto, test_size=0.50, random_state=a.semilla, stratify=estrato[resto])
    df["split"] = "train"
    df.loc[val, "split"] = "val"
    df.loc[te, "split"] = "test"
    df.to_csv("data/particion.csv", index=False)
    print(df.groupby(["split", "clase"]).size().unstack().to_string())
    print(df[df.split == "test"].groupby("region").size().to_string())

if __name__ == "__main__":
    main()
