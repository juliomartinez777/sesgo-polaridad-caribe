# Bitácora humano-IA

| Fecha | Integrante | Herramienta | Para qué se usó | Qué se aceptó, modificó o descartó | Cómo se verificó |
|---|---|---|---|---|---|
| 2026-11-02 | Julio | Claude (claude.ai) | Evaluar si el proyecto de Ingeniería I podía reutilizarse en IA y definir el alcance (polaridad en vez de detección de sesgo) | Se aceptó la propuesta de recortar el alcance a polaridad con Rest-Mex; se descartó usar YouTube o Tripadvisor por falta de licencia en el plazo | Se contrastó con la guía del proyecto (rutas, componentes obligatorios) |
| 2026-11-02 | Julio | Claude | Redactar el correo de solicitud del corpus Rest-Mex a los organizadores | Se aceptó con ajustes menores | Respuesta positiva de los organizadores con el corpus y su Readme |
| 2026-11-02 | Julio | Claude | Borrador del hito 1 (propuesta de una página) | Se modificó varias veces: foco en Cartagena y el Caribe, comparación con región andina, descripción del agente | Revisión del equipo; hito 1 aprobado por el docente |
| 2026-11-06 | Julio | Claude | Verificar la estructura y distribuciones del corpus (columnas, 66.703 reseñas de Colombia, conteo de menciones de destinos) | Se aceptó; corrigió una afirmación previa errónea de la IA (que la parte de Colombia era "pequeña"): es un tercio del corpus | Conteo directo sobre el archivo oficial con pandas; coincide con el Readme |
| 2026-11-16 | Julio | Claude | Escribir los scripts de preparación de datos, partición y línea base TF-IDF; redactar README y esta bitácora | Se aceptó la estructura; se decidió agrupar la polaridad en 3 clases y fijar las listas de destinos antes de evaluar | Ejecución completa de los tres scripts; macro-F1 reproducido con 3 semillas; revisión manual de la muestra de errores |
| 2026-11-16 | Julio | Claude | Interpretar el primer resultado por subgrupo | Se aceptó la advertencia de que el grupo con expresiones costeñas (58 reseñas, 5 en prueba) es demasiado pequeño para concluir; se pospone esa comparación hasta ampliar el glosario | Conteos reportados en el JSON de resultados |

Caso en que la IA propuso algo incorrecto: en la fase de planificación la IA afirmó que Rest-Mex tenía pocas reseñas de
Colombia; al verificar el archivo resultaron 66.703 (un tercio del corpus). Se detectó contando directamente sobre los datos.
