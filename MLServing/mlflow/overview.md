# mlflow란 ?

```plain Text
MLflow is an open source platform to manage the ML lifecycle, including experimentation, reproducibility, deployment, and a central model registry. MLflow currently offers four components:
```

</br>

## 개요
- 실험 기록, 프로젝트 관리, 모델 관리 기능을 지원
- 모델 관리 분야에서 인기가 많은 오픈소스
- databricks에서 운영
- 주요 기능
    1. Tracking : Record and query experiments : code, data, config, results
    2. Project : Packaging format for reproducible runs on any platform (실험을 어느 플랫폼이든 재현 가능하도록)
    3. Models : General format for sending models to diverse deploy tools (모델을 패키징 해서 deploy할 수 있도록 관리)

</br>
</br>
<img width="779" alt="image" src="https://github.com/hijyun/TIL/assets/54613024/220c6efa-5ae0-4884-a293-07245ccd348e">

</br>
</br>

### 설치 

```bash
$ pip install mlflow
```

</br>
</br>

# 예제
## 명시적 모델 저장
- 예제 데이터 :iris

```python
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec

iris = datasets.load_iris()
iris_train = pd.DataFrame(iris.data, columns=iris.feature_names)
clf = RandomForestClassifier(max_depth=7, random_state=0)
clf.fit(iris_train, iris.target)

input_schema = Schema([
  ColSpec("double", "sepal length (cm)"),
  ColSpec("double", "sepal width (cm)"),
  ColSpec("double", "petal length (cm)"),
  ColSpec("double", "petal width (cm)"),
])
output_schema = Schema([ColSpec("long")])
signature = ModelSignature(inputs=input_schema, outputs=output_schema)
# input example 넣기 
input_example = {
  "sepal length (cm)": 5.1,
  "sepal width (cm)": 3.5,
  "petal length (cm)": 1.4,
  "petal width (cm)": 0.2
}
mlflow.sklearn.log_model(clf, "iris_rf", signature=signature, input_example=input_example)
mlflow.sklearn.save_model(path="iris_rf", sk_model=clf)

```

</br>

- 모델 등록 결과

    ![image](https://github.com/hijyun/TIL/assets/54613024/36f22533-90de-4b1b-9bff-823e01d364b8)


</br>
</br>

- 모델 저장 후 서빙하기
    ```bash
    $ mlflow models serve -m iris_rf -p 1234
    ```

</br>
</br>

- curl 날리기
    ```bash
    curl --location --request POST 'localhost:1234/invocations' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "columns":["sepal length (cm)", "sepal width (cm)", "petal length (cm)",  "petal width (cm)"],
            "data": [[5.1, 3.5, 1.4, 0.2]]
        }'
    ```

</br>
</br>

- 직접 모델을 python으로 구현할 때 `mlflow.pyfunc.PythonModel` 을 상속해주면 된다.

    ```python
    # Define the model class
    class AddN(mlflow.pyfunc.PythonModel):

        def __init__(self, n):
            self.n = n

        def predict(self, context, model_input):
            return model_input.apply(lambda column: column + self.n)
    ```


</br>
</br>

- 모델 커스터마이징
    ```python
    # Load training and test datasets
    import pandas as pd
    import cloudpickle
    import mlflow.pyfunc
    from sys import version_info
    import xgboost as xgb
    from sklearn import datasets
    from sklearn.model_selection import train_test_split

    PYTHON_VERSION = "{major}.{minor}.{micro}".format(major=version_info.major,
                                                    minor=version_info.minor,
                                                    micro=version_info.micro)
    iris = datasets.load_iris()
    x = iris.data[:, 2:]
    y = iris.target
    x_train, x_test, y_train, _ = train_test_split(
        x, y, test_size=0.2, random_state=42)
    dtrain = xgb.DMatrix(x_train, label=y_train)

    # Train and save an XGBoost model
    xgb_model = xgb.train(params={'max_depth': 10},
                        dtrain=dtrain, num_boost_round=10)
    xgb_model_path = "xgb_model.pth"
    xgb_model.save_model(xgb_model_path)

    # Create an `artifacts` dictionary that assigns a unique name to the saved XGBoost model file.
    # This dictionary will be passed to `mlflow.pyfunc.save_model`, which will copy the model file
    # into the new MLflow Model's directory.
    artifacts = {
        "xgb_model": xgb_model_path
    }

    # Define the model class


    class XGBWrapper(mlflow.pyfunc.PythonModel):

        def load_context(self, context):
            import xgboost as xgb
            self.xgb_model = xgb.Booster()
            self.xgb_model.load_model(context.artifacts["xgb_model"])

        def predict(self, context, model_input: pd.DataFrame):
            print("model_input:", model_input)
            print("model_input.values:", model_input.values)
            print("model_input type:", type(model_input))
            input_matrix = xgb.DMatrix(model_input.values)
            print("input_matrix:", input_matrix)
            return self.xgb_model.predict(input_matrix)


    # Create a Conda environment for the new MLflow Model that contains all necessary dependencies.
    conda_env = {
        'channels': ['defaults'],
        'dependencies': [
            'pip',
            {
                'pip': [
                    'mlflow',
                    'xgboost=={}'.format(xgb.__version__),
                    'cloudpickle=={}'.format(cloudpickle.__version__),
                ],
            },
        ],
        'name': 'xgb_env'
    }

    # Save the MLflow Model
    mlflow_pyfunc_model_path = "xgb_mlflow_pyfunc"
    mlflow.pyfunc.save_model(
        path=mlflow_pyfunc_model_path, python_model=XGBWrapper(), artifacts=artifacts,
        conda_env=conda_env)

    # Load the model in `python_function` format
    loaded_model = mlflow.pyfunc.load_model(mlflow_pyfunc_model_path)

    # Evaluate the model
    test_predictions = loaded_model.predict(pd.DataFrame(x_test))
    print(test_predictions)

    ```



</br>
</br>


## Model registry
- 모델 저장소를 backend 서버에 띄우기 

    ```bash
    $ mlflow server --backend-store-uri sqlite:///sqlite.db --default-artifact-root ~/mlflow
    ```
    </br>

    </br>
    </br>

- 모델 등록하기
    ```python
    from random import random, randint
    from sklearn.ensemble import RandomForestRegressor
    import mlflow
    import mlflow.sklearn
    with mlflow.start_run(run_name="YOUR_RUN_NAME") as run:
    params = {"n_estimators": 5, "random_state": 42}
    sk_learn_rfr = RandomForestRegressor(**params)
    # Log the sklearn model and register as version 1
    mlflow.sklearn.log_model(
    sk_model=sk_learn_rfr,
    artifact_path="sklearn-model",
    registered_model_name="sk-learn-random-forest-reg-model"
    )
    ```
    </br>

    ```bash
    $ export MLFLOW_TRACKING_URI=http://localhost:5000

    ```


</br>
</br>






# 참고
- [mlflow documentations](https://mlflow.org/)
- [머신러닝 엔지니어 실무](https://www.inflearn.com/course/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D-%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4-%EC%8B%A4%EB%AC%B4)
