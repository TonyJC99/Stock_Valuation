# Valoración de Acciones de Grupo Melo

Herramienta de valoración en Python para Grupo Melo (Bolsa de Valores de Panamá). Combina análisis de razones financieras con un modelo DCF para estimar el valor intrínseco de la acción.

## Qué hace

Analiza los estados financieros consolidados de Grupo Melo (2023-2025) y genera:

- Razones de rentabilidad, apalancamiento y mercado a lo largo de tres años fiscales
- Una valoración DCF a 5 años con el valor intrínseco por acción
- Una tabla de sensibilidad según tasa de descuento y crecimiento terminal

## Resultado

Con una tasa de descuento del 10% y un crecimiento terminal del 3%, el modelo da un valor intrínseco de $147.22 por acción frente a un precio de mercado de $54.80 por acción. La tabla de sensibilidad mantiene la misma dirección en todas las combinaciones evaluadas (8-14% tasa de descuento, 2-4% crecimiento terminal).

Una diferencia de 2.7x entre valor intrínseco y precio de mercado es suficientemente grande como para revisar los supuestos de flujo de caja antes de tomarlo como una señal real. Ver Limitaciones.

## Funcionamiento

1. `load_data.py` procesa el CSV con los estados financieros brutos (balance general, estado de resultados y flujo de efectivo apilados en un solo archivo) y los separa en tres DataFrames.
2. `valuation.py` carga esos estados, calcula las razones (ROE, ROA, Margen Neto, Deuda/Patrimonio, UPA, P/E, P/B), corre el DCF, genera la tabla de sensibilidad y exporta todo como CSV para Power BI.

```
Grupo_Melo_CFS.csv → load_data.py → valuation.py → exports/*.csv → Dashboard de Power BI
```

## Razones calculadas

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

- FCF del año base: Flujo de Efectivo Operativo + CapEx (2025)
- Período de proyección: 5 años
- Caso base: tasa de descuento del 10%, crecimiento terminal del 3%
- Valor terminal calculado con el Modelo de Crecimiento de Gordon

## Limitaciones

- El crecimiento del FCF se mantiene constante a la tasa terminal durante los 5 años de proyección en lugar de disminuir o escalonarse — esto puede sobreestimar el valor intrínseco.
- Las proyecciones se basan en un solo año (2025) en lugar de un promedio normalizado de varios años.
- No hay ajuste por partidas no recurrentes en el flujo de efectivo o la utilidad neta.

## Stack

Python (pandas), Power BI

## Cómo ejecutarlo

```
pip install pandas
python valuation.py
```

Genera tres CSV en `exports/`: `ratios.csv`, `dcf.csv`, `sensitivity.csv`. Impórtalos en Power BI para reproducir el dashboard.

## Autor

Antonio J. Caballero de la Guardia
