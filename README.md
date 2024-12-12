# **MindLens**  
### **A Machine Learning-Powered Mental Health Screening App**  

## **Introduction**  
MindLens is a mental health screening application designed to assess stress levels and detect potential depression using machine learning. The app also provides actionable recommendations for users to improve their mental well-being.  

The mission of MindLens is to make mental health care accessible, reliable, and data-driven, empowering users to take proactive steps toward better mental health.  

---

## **Features**  
- Comprehensive stress and mental health survey.  
- ML-based predictions for potential depression.  
- Explanations and improvement suggestions based on results.  
- User-friendly interface for seamless engagement.  
- Modular codebase for easy extensibility.  

---

## **Tech Stack**  
- **Frontend**: React.js  
- **Backend**: Django REST Framework  
- **Database**: PostgreSQL  
- **ML Frameworks**: TensorFlow, Scikit-learn  
- **Other Tools**: Docker, Kubernetes, CI/CD pipelines  

---

## Build Pipeline Docs Quarto

```
cd quarto
quartodoc build
quarto preview
```

## Visualise ML Ops Pipeline

```
kedro viz run
``` 

## API endpoint for the model

The model can be served using mlflow and is accessible using, 

```
import requests

url = "http://127.0.0.1:8001/invocations"

data = {"instances": [list(X_test.values[5])]}

response = requests.post(
    url, headers={"Content-Type": "application/json"}, data=json.dumps(data)
)

print(response.json())
``` 
## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the files `src/tests/test_run.py` and `src/tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```
pytest
```


To configure the coverage threshold, look at the `.coveragerc` file.

## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. You can install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```



## Note: If pipeline is hangs, try using kaleido == 0.1.0post1
