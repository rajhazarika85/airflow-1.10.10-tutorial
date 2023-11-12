# airflow-1.10.10-tutorial
airflow-1.10.10 tutorial
airflow-1.10.10 works best on python 3.7
Here are the steps for mac

1. ```brew install pyenv```
2. ```pyenv install 3.7```
Output message: ```Installed Python-3.7.17 to /Users/{username}/.pyenv/versions/3.7.17```
3. Create venv
```/Users/{username}/.pyenv/versions/3.7.17/bin/python3.7 -m venv venv```

4. Important to set AIRFLOW_HOME to all new terminal
```export AIRFLOW_HOME="/airflow"```
```echo $AIRFLOW_HOME```

5. pip install ```'apache-airflow[gcp,statsd,sentry]==1.10.10'```
6. Encrypt passwords for airflow connections 
```pip install cryptography==2.9.2```  

7. ```pip install pyspark==2.4.5```

8. ```pip install markupsafe==2.0.1
   pip install numpy==1.20
   pip install WTForms==2.3.3
   pip install SQLAlchemy==1.3.23 
   pip install Flask-SQLAlchemy==2.4.4
   pip install pandas-gbq==0.14.1```

9. To check airflow version
```airflow version```                  
10. All sql db for airflow 
 ```airflow initdb```                   
11. ```airflow webserver --debug --port 8080```
12. ```airflow scheduler```