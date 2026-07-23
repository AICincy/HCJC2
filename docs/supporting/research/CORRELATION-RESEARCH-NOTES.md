# Correlation Research Notes

## Research question

How should HCJC2 replace V1's booking-to-dispatch candidate matchers with an enterprise-grade, explainable, extensible correlation system?

## V1 evidence reviewed

- `scraper/match.py`
- `scraper/correlate.py`
- `tests/test_match.py`
- `tests/test_correlate.py`
- `web/build.py`
- `web/pages.py`
- `web/templates/inmate.html`
- `.github/workflows/sweep.yml`
- July 20, 2026 custody and CFS data snapshots

## External foundations

### Fellegi and Sunter

The classical record-linkage framework separates links, non-links, and possible links rather than forcing every pair into a binary conclusion.

Reference: Ivan P. Fellegi and Alan B. Sunter, “A Theory for Record Linkage,” Journal of the American Statistical Association 64, no. 328 (1969), DOI `10.1080/01621459.1969.10501049`.

### Sadinle

Bipartite linkage research shows why independent pair scoring can be unreasonable when assignments compete. It also supports leaving uncertain relationships unresolved.

Reference: Mauricio Sadinle, “Bayesian Estimation of Bipartite Matchings for Record Linkage,” arXiv `1601.06630`.

HCJC2 cannot directly impose strict one-to-one matching because one dispatch may lead to multiple bookings. The useful principle is that candidate pairs must be evaluated within the full assignment context.

### Murray

Blocking and filtering affect linkage inference. HCJC2 must record the candidate-generation policy and evaluate excluded pairs rather than treating blocking as a neutral optimization.

Reference: Jared S. Murray, “Probabilistic Record Linkage and Deduplication after Indexing, Blocking, and Filtering,” arXiv `1603.07816`.

### Probability calibration

A numerical score is not a probability merely because it falls between zero and one. Calibrated probabilities require empirical agreement between predicted probability and observed frequency. Reliability diagrams and calibration metrics support that validation.

Reference: scikit-learn 1.9 documentation, “Probability calibration.”

### NIST AI RMF

If HCJC2 introduces learned scoring, NIST AI RMF provides a governance baseline for validity, reliability, transparency, explainability, documentation, testing, and recourse. The same controls are useful for a deterministic high-impact inference system.

References:

- NIST AI 100-1, Artificial Intelligence Risk Management Framework 1.0
- NIST AI RMF Playbook, Measure 2.9

### W3C PROV

The W3C PROV model provides a useful vocabulary for entities, activities, agents, derivation, generation, and responsibility. HCJC2 does not need to publish RDF, but its internal provenance fields should map cleanly to these concepts.

Reference: W3C Recommendation, PROV-O: The PROV Ontology, 30 April 2013.

## Key design inference

Booking-to-dispatch correlation is not ordinary person-level entity resolution because CFS data lacks identity fields. It is event linkage under uncertain time, incomplete attributes, and potentially one-to-many relationships.

Therefore HCJC2 should:

1. represent time as intervals
2. separate candidate generation from assessment
3. retain unresolved cases
4. evaluate candidates in competition context
5. model group relationships
6. calibrate only from labeled outcomes
7. preserve complete provenance and recourse
