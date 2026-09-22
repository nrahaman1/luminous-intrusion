# Luminous Intrusion

Interactive atlas of nighttime-light exposure likelihood across U.S. bat habitat, 1992–2022.

**Live site:** https://nrahaman1.github.io/luminous-intrusion/

Companion to: Rahaman, S. N., Shermin, N., López-Carr, D., & Pricope, N. G. (2024). *Mapping the luminous intrusion: a nationwide multidecadal emerging bivariate cluster analysis of bat habitat's exposure likelihood to nighttime light.* Landscape Ecology 39:202. https://doi.org/10.1007/s10980-024-01997-8

## Features
- Year slider (1992–2022) with play-through, across four map layers: exposure likelihood, nighttime light, bat habitat share (all species or one species), and emerging-pattern class
- Click any county to see its 31-year light trend, exposure-likelihood trend, national percentile, and habitat for each of the three bat species
- **Harmonized / Raw** toggle for the DMSP → VIIRS sensor switch (see [Sensor harmonization](#4-sensor-harmonization-dashboard-only))
- County search, sortable county table, a ranked list of the most exposed counties, and shareable county links (e.g. `#12095` for Orange County, FL)
- Responsive layout for phone, tablet and desktop

## Method

### 1. Study unit and data
The analysis covers **3,108 counties in the contiguous United States** for each year from **1992 to 2022**.

**Bat habitat.** National-scale habitat maps for 2001 from the USGS Gap Analysis Project (GAP) for three species:

| Species | Scientific name | Distribution |
|---|---|---|
| Big brown bat | *Eptesicus fuscus* | nearly ubiquitous across the contiguous U.S. |
| Silver-haired bat | *Lasionycteris noctivagans* | mainly northwestern, southern and southeastern U.S. |
| Little brown myotis | *Myotis lucifugus* | mainly northwestern, southern and southeastern U.S. |

The GAP models are deductive predictions, not field occurrence records. They are built from literature-derived habitat associations and remotely sensed environmental variables such as land cover, elevation, proximity to water and forest edges. Habitat area was summed per county for each species, and the three species were combined into a **total bat habitat area** per county.

**Nighttime light (NTL).** Yearly county means were extracted in Google Earth Engine from two sensors:

| Years | Sensor | Resolution | Unit |
|---|---|---|---|
| 1992–2011 | DMSP-OLS Nighttime Lights Time Series v4 (stable lights) | ~927.67 m | digital number (DN), 0–63 |
| 2012–2022 | VIIRS Day/Night Band Composites v1 (average radiance) | ~463.83 m | nW·cm⁻²·sr⁻¹ |

### 2. Exposure likelihood: yearly bivariate cluster z-score
For every year, a bivariate spatial-autocorrelation analysis (PySAL) is run between **normalized mean NTL** and **normalized total bat habitat area**. Each county `n` in year `t` gets a z-score:

```
z(n,t) = ( x(n,t) − a(n,t) ) / sd(n,t)
```

where `x` is total bat habitat area, `a` is average nighttime light, and `sd` is the standard deviation. A **high z-score** means a county and its neighbours combine a large bat-habitat area with high nighttime light, i.e. a higher likelihood that the habitat is exposed to artificial light at night. Because the z-score is standardized within each year, the two sensors' different resolutions have less influence than they would on raw values.

### 3. Emerging bivariate cluster analysis
The yearly z-scores are stacked into a **space–time cube** (ArcGIS Pro) and analysed with Emerging Hot Spot Analysis, which combines:

- **Getis-Ord Gi\*** hot/cold-spot statistics for each county-year, and
- a **Mann-Kendall trend test** on each county's time series. For each successive pair of years, the test scores +1 if the value rises, −1 if it falls and 0 for a tie, then sums the scores into S. Under independence, E(S) = 0 and Var(S) = n(n−1)(2n+5)/18, with a correction for tied ranks.

Each county is assigned one of 16 space–time patterns, or "No Pattern Detected":

| Pattern | Meaning (hot-spot version; cold spots are analogous for low values) |
|---|---|
| New | Significant hot spot only in the final time step |
| Consecutive | A single uninterrupted run of hot spots in the final time steps (≥2 steps, <90% of all steps) |
| Intensifying | Hot spot in ≥90% of steps including the last, with significantly increasing intensity |
| Persistent | Hot spot in ≥90% of steps, with no significant trend in intensity |
| Diminishing | Hot spot in ≥90% of steps including the last, with significantly decreasing intensity |
| Sporadic | An on-and-off hot spot that is never a cold spot |
| Oscillating | Hot in the final step but a cold spot in some earlier steps; hot in <90% of steps |
| Historical | Not hot in the final step, but hot in ≥90% of earlier steps |

**Key results (paper):**
- 24.9% of bat habitat lies in diminishing cold spots.
- 1.4% of bat habitat is in persistent hot spots, mainly in 82 counties around Orlando, Tampa, Atlanta and the Virginia coast.
- 20 counties are intensifying hot spots, mainly around Los Angeles, the Virginia coast and New Orleans.
- 28 counties are consecutive hot spots around Los Angeles, Houston, New Orleans and Dallas.
- 86 counties are sporadic hot spots.
- 1 county near Houston is a new hot spot.

### 4. Sensor harmonization (dashboard only)
DMSP and VIIRS differ in units, resolution and saturation, so raw county values and their yearly distributions jump at 2012. The drop affects both light and the exposure z-score. In raw data, counties with z ≥ 1.96 fall from 186 to 98, and about 980 counties shift by more than 10 percentiles in rank, against about 110 in a typical year.

**Harmonized** mode (the default) corrects this for display in two steps, applied to both light and z:

1. **Quantile matching.** A county at the *p*-th percentile of the 2012 VIIRS distribution is given the *p*-th percentile value of the 2011 DMSP distribution. This single mapping, fitted on the adjacent 2011↔2012 pair, is applied to every VIIRS year, so change after 2012 is kept.
2. **Per-county anchoring.** DMSP saturates at 63 DN in bright urban cores and spreads light into dark areas nearby, so counties rank differently under VIIRS. Each county's harmonized VIIRS series is shifted so that its 2012–14 mean equals its 2009–11 DMSP mean. Light values are floored at 0.

After harmonization, the 2011→2012 transition looks like an ordinary year: the count of counties with z ≥ 1.96 goes from 186 to 186, and rank shifts drop to 63 for light and 41 for z.

**Assumptions and limits.**
- The anchor assumes no real change in each county between 2009–11 and 2012–14.
- VIIRS values above the 2012 maximum are clipped to the 2011 maximum.
- Harmonized values are for visualization only. The emerging-pattern classes and **Raw** mode show the values as published.

### 5. Dashboard metrics
| Metric | Definition |
|---|---|
| Counties with exposure z ≥ 1.96 | Counties whose yearly bivariate z-score is at least 1.96 (≈ 95% significance) |
| Share of bat habitat inside them | Habitat in those counties ÷ total habitat. Species ranges overlap, so each county contributes its largest single-species footprint. |
| National percentile | A county's rank among all counties' z-scores in the selected year |
| Habitat share of county | GAP habitat area ÷ county land area (Census ALAND) |
| Mean county light | Unweighted mean of county NTL values (in DN when harmonized) |

`data.js` is generated from the study tables by `build_data.py`.

## Data sources
- Nighttime light: DMSP-OLS Nighttime Lights Time Series v4; VIIRS Day/Night Band Composites v1 (Earth Observation Group, via Google Earth Engine)
- Habitat: USGS Gap Analysis Project species habitat models (2001)
- County boundaries: U.S. Census Bureau via [us-atlas](https://github.com/topojson/us-atlas)
- Basemap: © CARTO, © OpenStreetMap contributors

## License
MIT. See [LICENSE](LICENSE).
