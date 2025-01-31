from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

# Define default arguments
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

# Define the DAG
with DAG(
    dag_id="k8s_pod_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # Define the KubernetesPodOperator
    k8s_task = KubernetesPodOperator(
        namespace="default",  # Change as per your setup
        image="nvcr.io/nvidia/pytorch:25.01-py3",
        cmds=["/bin/bash", "-c"],
        arguments=["apt update; pip install mlflow scikit-learn boto3; git clone http://gitea.local/vamsi344/example-mlflow.git && source example-mlflow/.env; python3 example-mlflow/example-mlflow.py;"],
        name="airflow-pod-task",
        task_id="run-k8s-pod",
        get_logs=True,
        is_delete_operator_pod=True,  # Deletes the pod after execution
    )

    k8s_task

