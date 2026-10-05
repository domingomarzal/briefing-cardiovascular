#!/usr/bin/env python3
# N17 · Dislipemia (decisión del usuario, 05-oct-2026: «tiene que haber alguno para dislipemia»).
# Único elegible de lípidos en la ventana: Atherosclerosis 121916 (online 02-oct-2026, Research article,
# acceso abierto). Sin abstract en PubMed/Crossref; abstract leído en la web del editor
# (atherosclerosis-journal.com) con Chrome real el 05-oct-2026. Idempotente.
import json, os
B = os.path.dirname(os.path.abspath(__file__))
DOI = "10.1016/j.atherosclerosis.2026.121916"
TIT = "Inflammation and Lipoprotein(a) as Predictors of Cardiovascular Events Across Baseline Risk Levels – Results from the UK Biobank"
ABS = ("AIMS: To determine how high-sensitivity C-reactive protein (hsCRP) and lipoprotein(a) [Lp(a)] predict major adverse cardiovascular events (MACE) across the spectrum of baseline cardiovascular risk. "
"METHODS: UK Biobank participants were grouped according to baseline cardiovascular risk. The primary endpoint was first MACE (myocardial infarction, ischaemic stroke, cardiovascular death). Cox models estimated sex-specific hazard ratios (HR) based on standardised (per standard deviation [SD]) and categorised (quartile) biomarker levels, adjusted for components of the Systematic COronary Risk Evaluation (SCORE) 2 model and the other biomarker. "
"RESULTS: Median follow-up duration was 15.2 years. There were 241010 low-risk, 74179 high-risk, 25512 very high-risk, 60177 treated (lipid-lowering therapy) and 15720 secondary prevention participants included. Median calculated 10-year cardiovascular risk in the low-, high- and very high-risk subgroups was 1.8%, 6.3% and 10.4% respectively. Continuous hsCRP levels were directly associated with MACE in both sexes across all subgroups (p<0.001). The strongest quartile effect was in the secondary prevention cohorts (Q4 vs Q1: HR +79% men, +81% women; p<0.001). HsCRP associated with each MACE component. Lp(a) predicted MACE independently but heterogeneously: in women associations were consistent across subgroups (per-SD HR 1.06-1.11; p≤0.005), whereas in men Lp(a) predicted MACE only in primary prevention subgroups (per-SD HR 1.11-1.15; p<0.001) but not in secondary prevention (p=0.65). In primary prevention subgroups, Lp(a) associations were driven largely by myocardial infarction (p<0.001). "
"CONCLUSION: HsCRP and Lp(a) provide prognostic information beyond traditional risk factors used in SCORE2. These findings endorse selective measurement of hsCRP and Lp(a) to refine risk stratification, though randomised trials are needed to validate biomarker-directed interventions.")
EL = json.load(open(B + "/n17_el.json"))
for e in EL:
    if e.get("doi") == DOI:
        e.update(title=TIT, abstract=ABS, ptypes=["Journal Article"])
json.dump(EL, open(B + "/n17_el.json", "w"), ensure_ascii=False, indent=1)
S = json.load(open(B + "/n17_sel.json"))
if not any(o["key"] == "a46" for o in S):
    r = dict(rel=7, cambio=4, evid=5, efecto=4, rep=4, fi=4)
    tot = round(.20*r["rel"] + .25*r["cambio"] + .20*r["evid"] + .15*r["efecto"] + .12*r["rep"] + .08*r["fi"], 2)
    S.append(dict(key="a46", idx=None, pmid="CR:" + DOI, doi=DOI, pii="S0021915026012827", journal="Atherosclerosis",
                  sec=3, ptype="Estudio de cohorte", acr="", **r, total=tot,
                  prio="Relevante" if tot >= 5 else "Complementario", oblig=False, noabs=False, alt=None,
                  rec="crossref", title=TIT, abstract=ABS))
    print("a46", tot)
json.dump(S, open(B + "/n17_sel.json", "w"), ensure_ascii=False, indent=1)
# Enlace: ScienceDirect se queda en el reto de Cloudflare; la web de la revista abre (verificado en Chrome).
J = json.load(open(B + "/n17_jlinks.json"))
J["a46"] = "https://www.atherosclerosis-journal.com/article/S0021-9150(26)01282-7/fulltext"
json.dump(J, open(B + "/n17_jlinks.json", "w"), ensure_ascii=False, indent=1)
print("sel:", len(S))
