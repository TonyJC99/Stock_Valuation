# Valoración de Acciones de Grupo Melo

Una herramienta de valoración en Python para Grupo Melo (Bolsa de Valores de Panamá), que combina análisis de razones financieras con un modelo de flujo de caja descontado (DCF) para estimar el valor intrínseco de la acción.

## Resumen

Este proyecto analiza los estados financieros consolidados de Grupo Melo (2023–2025) para evaluar el desempeño de la empresa y estimar su valor justo por acción. Genera:

- Razones de rentabilidad, apalancamiento y valor de mercado a lo largo de tres años fiscales
- Una valoración DCF a 5 años con el valor intrínseco por acción
- Una tabla de sensibilidad que evalúa el valor intrínseco bajo distintos supuestos de tasa de descuento y crecimiento terminal

## Hallazgo Principal

Con una tasa de descuento del 10% y un crecimiento terminal del 3%, el modelo estima un valor intrínseco de **$147.22 por acción**, frente a un precio de mercado de **$54.80 por acción** — lo que sugiere que la acción está subvalorada de forma significativa. La tabla de sensibilidad confirma esta subvaloración en todas las combinaciones evaluadas de tasa de descuento (8–14%) y crecimiento terminal (2–4%).

Esta es una prima considerable (2.7x), y debe interpretarse como una señal para examinar más a fondo los supuestos de flujo de caja, no como una señal definitiva de compra. Ver **Limitaciones** más abajo.

## Funcionamiento

1. **`load_data.py`** — Procesa el archivo CSV con los estados financieros brutos (balance general, estado de resultados, flujo de efectivo), que vienen apilados en un solo archivo, y los separa en tres DataFrames limpios.
2. **`valuation.py`** — Carga los estados procesados, calcula las razones financieras (ROE, ROA, Margen Neto, Deuda/Patrimonio, UPA, P/E, P/B), ejecuta el modelo DCF, genera la tabla de sensibilidad, y exporta los tres resultados como CSV para Power BI.


Grupo_Melo_CFS.csv → load_data.py → valuation.py → exports/*.csv → Dashboard de Power BI


## Razones Calculadas

| Razón | Fórmula |
|---|---|
| ROE | Utilidad Neta / Patrimonio Total |
| ROA | Utilidad Neta / Activos Totales |
| Margen Neto | Utilidad Neta / Ingresos |
| Deuda/Patrimonio | Pasivos Totales / Patrimonio Total |
| UPA (EPS) | Utilidad Neta / Acciones en Circulación |
| P/E | Precio por Acción / UPA |
| P/B | Capitalización de Mercado / Patrimonio Total |

## Supuestos del DCF

- Flujo de caja libre del año base: Flujo de Efectivo Operativo + CapEx (2025)
- Período de proyección: 5 años
- Caso base: tasa de descuento del 10%, crecimiento terminal del 3%
- Valor terminal calculado mediante el Modelo de Crecimiento de Gordon

## Limitaciones

- Se asume una tasa de crecimiento constante del flujo de caja libre durante los 5 años de proyección, en lugar de modelar una trayectoria de crecimiento decreciente o escalonada — esta simplificación puede sobreestimar el valor intrínseco.
- El modelo utiliza un único año (2025) como base para las proyecciones, en lugar de un promedio normalizado de varios años.
- No se realizan ajustes por partidas no recurrentes en el flujo de efectivo o la utilidad neta.

## Tecnologías Utilizadas

- **Python** (pandas) — procesamiento de datos y modelado financiero
- **Power BI** — visualización del dashboard (tendencias de razones, resumen DCF, matriz de sensibilidad)

## Cómo Ejecutar el Proyecto

- pip install pandas
- python valuation.py


Genera tres archivos CSV en `exports/`: `ratios.csv`, `dcf.csv`, `sensitivity.csv`. Importa estos archivos en Power BI para reproducir el dashboard.

## Autor

Antonio J. Caballero de la Guardia