# 🎯 E2E Recommender System with MLOps

An end-to-end MLOps pipeline for Anime Recommendation System — from data preprocessing to model deployment.

## 📌 Problem Statement
Develop a recommender engine that suggests products based on user-item interactions, while embedding MLOps practices for production readiness.

## 🧠 Solution Overview
- Built a collaborative filtering model for recommendations.
- Integrated DVC for data and model versioning.
- Used Comet-ML to track experiments across model iterations.
- Deployed via Docker on GCP using container orchestration tools.

## 🛠️ Tech Stack
- Python, pandas, scikit-learn
- Comet-ML for experiment tracking
- DVC (Data Version Control)
- Docker + GCP (Compute Engine)
- Git for version control
- Streamlit for optional frontend

## 🔁 Workflow
```mermaid
graph TD
A[Data Collection & Processing] --> B[Feature Engineering]
B --> C[Model Building (Collaborative Filtering)]
C --> D[Experiment Tracking (Comet-ML)]
D --> E[Model Packaging (Docker)]
E --> F[Deployment on GCP]
