# Amazon Managed Workflows Example

Showing how to deploy some simple DAGs to Amazon Managed Workflows for Apache Airflow

## Setting up Amazon Managed Workflows

_Unless otherwise stated, uses the default settings where not directly mentioned._

1. Create an S3 bucket where we will be storing the DAG code called `test-workflows-bucket`, using all the default S3 settings
2. Locally create a `requirements.txt` file and enter this contents:

```
numpy==1.21.1
pandas==1.3.1
python-dateutil==2.8.2
pytz==2021.1
six==1.16.0

```

3. Upload the requirements.txt file to the root of the S3 bucket
    1. Note: creating this dummy file here as you cannot create an environment when it points to a `requirements.txt` file that doesn't exist
    2. The alternative is to not configure the requirements field, then update your environment config when you've uploaded the `requirements.txt` file
    3. Neither is ideal to be honest
5. Go to Amazon Managed Workflows and create a new environment
    1. Give it the name `test-workflows`
    2. Use Airflow version 2.0.2 (Latest)
    3. Set the S3 bucket to `s3://test-workflows-bucket`
    4. Set the DAGs folder to `s3://test-workflows-bucket/dags`
    5. Set the Requirements file to `s3://test-workflows-bucket/requirements.txt`
    6. Under VPC click `Create MWAA VPC`
        1. Call the stack `Test-MWAA-VPC`
        2. Leave all the settings as defaults
        3. Click `Create stack`
        4. Wait for all resources to be created
    7. Back in the MWAA config, click the refresh button next to the VPC
    8. Choose the newly created VPC, this will also auto fill your subnets for you
    9. For this demo’s purposes, click `Public network (No additional setup)` for the Web server access option
    10. Set `Maximum worker count` to `1`
    11. Leave the rest as default
    12. Click `Next` then `Create environment`
    13. Note creation can take some time, 20 to 30 minutes!

We now have a hosted version of Apache Airflow running, and a bucket in which to add our code.

## Deploying to Amazon Managed Workflows

Firstly, clone this repository to a local folder

This project is structured like so:

* dags/
    * dependencies/
        * \_init\_.py
        * config.py
            * _Contains a single config value, using this to check that an internal package can be imported_
    * dag_with_dependencies.py
        * _Depends on both an internal package and a PIP module_
    * simple_dag.py
        * _Basic hello world dag_
* requirements.txt
    * _The pip modules to be installed_

To upload manually to S3 (usually this would be synced through some CI process using the AWS CLI):

1. Open the S3 bucket in AWS Console
2. Click `Upload`
3. Click `Add files`
4. Select the `requirements.txt` file
5. Click `Add folder`
6. Choose the `dags/` folder
7. Then click `Upload`

## Running the DAGs

It takes ~1-2 minutes from uploading the DAGs to S3 to them being refreshed in the UI

Both the sample dags are set up to run when triggered rather than on a schedule.

To manually trigger them:

1. Open up the AWS MWAA environment `test-workflows`
2. Click on the `Airflow UI` link, which will open up the Apache Airflow UI
3. You’ll be shown a list of DAGs that are registered, 2 should be there: `simple_dag` and `dag_with_dependencies`
4. For the one you want to run, click the `>` play icon under Actions next to the dag
5. You can click on the dag name to see details, status of the run and logs
