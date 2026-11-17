# Datos

Fuente: **Rest-Mex 2023 Sentiment Analysis Training Corpus** (Álvarez-Carmona et al., 2023), opiniones de
TripAdvisor con polaridad de 1 a 5, país y tipo de lugar. Su documentación establece que los datos se usan
**exclusivamente con fines académicos y de investigación**, por lo que el archivo **no se incluye en este repositorio**.

Cómo obtenerlo: solicitarlo a los organizadores (CIMAT) o a través del portal ODESIA
(https://portal.odesia.uned.es/en/dataset/rest-mex-2023-sentiment). Guardar el archivo como
`data/Rest_Mex_Sentiment_Analysis_2023_Train.xlsx` y ejecutar `python src/preparar_datos.py --entrada data/Rest_Mex_Sentiment_Analysis_2023_Train.xlsx`.

Los archivos derivados (`colombia.csv`, `particion.csv`) se generan localmente y tampoco se suben.
