import mlflow

# Set tracking URI

# Verify if the run exists
run_id = "de76a974868344329bafa0975bf29f24"
run = mlflow.get_run(run_id)
print(run.info)
