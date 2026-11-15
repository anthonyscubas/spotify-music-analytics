# Resultados del análisis exploratorio

**Muestra facilitada:** 8,579 registros únicos de canciones y 2,547 artistas tras limpieza (CSV aportado, no catálogo completo de Spotify).

| Indicador | Resultado |
|---|---:|
| Canciones | 8,579 |
| Artistas | 2,547 |
| Popularidad media canción | 52.36 / 100 |
| Mediana de popularidad | 58.0 / 100 |
| Duración media | 3.49 minutos |
| Canciones marcadas explícitas | 25.03% |
| Sin géneros asignados | 39.14% |

## Hallazgos descriptivos

- **Popularidad:** media 52.36 y mediana 58.0 en escala 0–100; consultar el histograma para la dispersión.
- **Géneros:** los cinco géneros con mayor número de apariciones en registros son pop, country, soundtrack, hip hop, indie. Los géneros son etiquetas multivalor y pertenecen al artista; no necesariamente describen por separado cada canción.
- **Top artistas:** el ranking exige al menos cinco canciones registradas para evitar promedios sustentados en una sola observación; solo compara la muestra disponible.
- **Seguidores:** se usa escala logarítmica para visualizar diferencias de órdenes de magnitud. La correlación no demuestra causalidad.

## Limitaciones

1. **Muestra no aleatoria ni catálogo completo:** no extrapolar porcentajes a toda la plataforma.
2. Popularidad y seguidores son valores registrados en el CSV, no mediciones actuales ni series temporales.
3. Varios registros del mismo artista comparten seguidores y popularidad de artista; pueden crear dependencia estadística.
4. Fechas corresponden a lanzamientos de álbumes, no necesariamente a la primera publicación de cada canción.
5. Las comparaciones explícito/no explícito son descriptivas, no causalidad.
6. El CSV original no se redistribuye porque no consta licencia de distribución.
