# AI Safety Legislation in the U.S. Congress

This repository contains the research paper, data, and supplementary materials for our study on **AI Safety Legislation in the United States Congress**, accepted at the **NeurIPS 2025 RegML Workshop**.

## 📄 Paper
**Title:** *From Proposals to Enactment: The Procedural Bottleneck in AI Safety Regulation*<br> 
**Authors:** Mansur Ali Khan, Efe Akengin, Dr. Ahmed Rushdi<br>
**Workshop:** NeurIPS 2025 Workshop on Regulatable Machine Learning (RegML)<br>
**View Paper at:** https://openreview.net/pdf?id=OCn2y7QDTB

## 📘 Introduction
While AI models advance at unprecedented rates, AI safety legislation remains largely symbolic, stalled, or unrealized. Through a year-by-year analysis of AI breakthroughs, U.S. congressional policy proposals, and international legislative enactments, this study identifies a structural gap: the United States is not deficient in AI safety bill proposals but in legislative action, with only 4.23% of U.S. AI bills reaching any terminal outcome. We quantify enactment rates, map U.S. Congressional AI bills across thematic domains, identify procedural bottlenecks, and develop a logistic regression model to test which factors predict legislative stalling.

## ⚙️ Methodology
We have created the **first comprehensive dataset of US AI bills spanning 2017 to August 2025 (150 bills)** by aggregating data from Congress.gov that describes the structural causes of AI legislation failure.
The causes are categorized as *Bill End-Point Categorization:* No Action after the introduction,, Stalled in Committee (House/Senate), Declined, Passed, Calendar Inaction (House/Senate), Expired without action

We introduce the **Action Rate Metric:** as a representative for congressional engagement and legislative momentum.

**Action Rate =  (Passed Bills + Declined Bills) / Total Proposed Bills**

We make **thematic classification** and **Penalized Logistic Regression**, by defining thematic subfields related to AI and AI Safety for each bill.

To identify *stallation* predictors, we expanded the dataset via the Congress.gov API, incorporating chamber origin, sponsor party affiliation, bipartisanship status, and sponsor quantity (12 parameters total).

A penalized logistic regression model with ridge penalty (C=1.0, max_iterations=100, solver=lbfgs) was trained using 80/20 train-test splits with bootstrap resampling across 100 iterations. Standard errors and p-values were computed via bootstrap methodology, with statistical significance assessed at α=0.05 post Bonferroni correction.


## 📈 Key Findings
<div style="display: flex; flex-direction: column; align-items: center;">

  <img src="images/bills_action.png"
       alt="AI Bill Endpoints"
       width="500"
       style="margin: 20px 0;" />

  <img src="images/ai_legislation_llm_breakthroughs.png"
       alt="Quantitative comparison of AI legislation vs LLM breakthroughs"
       width="500"
       style="margin: 20px 0;" />

  <img src="images/bills_flow.png"
       alt="AI Bill Endpoints"
       width="500"
       style="margin: 20px 0;" />

  <img src="images/regression_table.png"
       alt="Logistic Regression Results"
       width="500"
       style="margin: 20px 0;" />

  <img src="images/proposals_distribution.png"
       alt="Comprehensive taxonomy of AI policy subfields for Bills in United States Congress"
       width="500"
       style="margin: 20px 0;" />

</div>

## 📌 Recommendations
**1. Establish dedicated AI Policy committees to address pigeonholing.** If the leadership decides the bill does not fit within its overall agenda, a decision not to act will ‘kill’ the bill just as effectively as a vote against it.<br>
**2. Create Independent AI Safety Specialized Agencies.** The Agencies should be empowered to regulate AI systems, audit compliance, and intervene in development when necessary.<br>
**3. Introduce Sunset Clauses to speed up policy enactment.** Create mechanisms to proceed without consensus at speed, overcoming analysis/paralysis modes.<br>
**4. Implement Preemptive Enactment Models.** Develop frameworks that would activate automatically when specific risk thresholds are crossed.<br>

## 🔗 Citation
If you use this work, please cite:
```bibtex
@inproceedings{khan2025aisafety,
  title={From Proposals to Enactment: The Procedural Bottleneck in AI Safety Regulation},
  author={Mansur Ali Khan, Efe Akengin, Dr. Ahmed Rushdi  },
  booktitle={NeurIPS 2025 Workshop on Regulatable Machine Learning (RegML)},
  year={2025}
}
