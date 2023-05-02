# Introduction

This is a project that takes a topic  as an input creat an analysis about trend and user emotions about this topic

## Setup

<b>Prerequisites</b>

- Python

<details><summary><b>Setup locally</b></summary>



To run the app open a new terminal and enter the following:
```
# install dependencies
pip install -r requirements.txt

# go to app folder and run app in development
cd app
python -m uvicorn main:app --reload
```


send request to http://127.0.0.1:8000/getAnalysis?3D glasses with a topic in the body

<details><summary><b>Dokrize</b></summary>


To build the docker image.
```
docker build -t trend_wise .
```

To run the docker image.
```
docker run --name trend_wise -p 8000:80 trend_wise
```

To tag the docker image.
```
docker tag trend_wise mohammedaleryani/trend_wise
```

Then to push it.
```
docker push mohammedaleryani/trend_wise
```
</details>

