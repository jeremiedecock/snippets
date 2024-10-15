#!/usr/bin/env python3

# C.f. https://mlflow.org/docs/latest/getting-started/logging-first-model/step2-mlflow-client.html

import mlflow

#from mlflow import MlflowClient

#client = MlflowClient(tracking_uri="http://127.0.0.1:8080")

# Démarrer une nouvelle expérience
mlflow.set_experiment("mon_experience_simple")

# Démarrer une nouvelle exécution (run)
with mlflow.start_run():
    # Loguer des métriques
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)
    mlflow.log_metric("epoch", 10)

    # Loguer des paramètres
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 32)

    print("Les métriques et paramètres ont été enregistrés avec succès dans MLflow.")

