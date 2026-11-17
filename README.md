# Sesgo en la clasificación automática de polaridad de reseñas turísticas de Cartagena y el Caribe colombiano

Proyecto final de Inteligencia Artificial (ruta D, PLN) · Universidad Tecnológica de Bolívar · 2026-II
Julio Martínez (T00077681) y Jairo Mendoza (T0007725).

**Pregunta:** ¿los modelos de clasificación de polaridad funcionan peor con las reseñas turísticas sobre Cartagena y
el Caribe colombiano que con las de la región andina (Bogotá y Medellín)?

El sistema clasifica una reseña en tres clases (negativa, neutra, positiva) y reporta el macro-F1 por subgrupo
(Caribe, andina, reseñas con expresiones costeñas) con intervalos de confianza bootstrap y la brecha ΔF1.

## Ejecutar la línea base en 4 comandos

```bash
pip install -r requirements.txt
python src/preparar_datos.py --entrada data/Rest_Mex_Sentiment_Analysis_2023_Train.xlsx
python src/particion.py --semilla 42
python src/linea_base.py --semilla 42
```

Antes, colocar el archivo de Rest-Mex en `data/` (ver `data/README.md`; no se redistribuye).
Resultados en `experiments/E1_tfidf_lr/resultados_semilla42.json` y una muestra de errores en
`experiments/E1_tfidf_lr/muestra_errores_test.csv`.

## Estructura

| Carpeta | Contenido |
|---|---|
| `src/` | `preparar_datos.py` (subconjunto colombiano, clases y subgrupos), `particion.py` (70/15/15 estratificada), `linea_base.py` (TF-IDF + regresión logística) |
| `experiments/` | resultados por experimento y semilla (JSON) que respaldan cada tabla del informe |
| `notebooks/` | exploración del corpus |
| `docs/` | `bitacora_ia.md` (bitácora humano-IA) y entregas de los hitos |
| `app/` | prototipo en Streamlit (hito 3) |
| `data/` | instrucciones para obtener el corpus; los datos no se suben |

## Plan de experimentos

| ID | Descripción | Estado |
|---|---|---|
| E1 | Línea base TF-IDF (1-2 gramas) + regresión logística, 3 semillas | Hecho |
| E2 | BETO con ajuste fino, 3 semillas (Google Colab) | Pendiente |
| E3 | RoBERTuito con ajuste fino, 3 semillas | Pendiente |
| E4 | Comparación E1-E3 con bootstrap pareado y ΔF1 por región | Pendiente |

Métricas y umbral de éxito fijados en el hito 1: macro-F1 principal; el mejor transformer debe superar a la línea
base en al menos 3 puntos de macro-F1; una brecha ΔF1 mayor a 5 puntos entre regiones se considera relevante.
