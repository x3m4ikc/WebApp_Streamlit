# ml_streamlit

This is pet project to test abilities [Streamlit](https://www.streamlit.io/) framework. The data used in this repo is the [Titanic dataset](https://www.kaggle.com/c/titanic) .

Try app [![Open in Streamlit][share_badge]][share_link]

## Files

- `app.py`: streamlit app file
- `model.py`: script for generating the Random Forest classifier model
- `titanic.csv` and `model_weights.mw`: data file and pre-trained model
- `requirements.txt`: package requirements files
- `Dockerfile` for docker deployment

## Run project locally

### Shell

For directly run streamlit locally in repo root folder as follows:

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ streamlit run app.py
```
Open http://localhost:8501/ to view the app.

### Docker

For build and run docker image named 'titanic':
```
$ docker build -t titanic .
$ docker run -it --rm -p '8501:8501' titanic
```
Open http://localhost:8501/ to view the app

### Streamlit Cloud Deployment

1. Put app on GitHub (like this repo)
The repo must be public and have a 'requirements.txt' file
2. Sign in Streamlit Cloud
Sign into share.streamlit.io with your GitHub email address, you need to have access to Streamlit Cloud service
3. Deploy and share
Click "New App", fill in your repo, branch, file path, choose a Python version (3.11 for this app) and click "Deploy", then you  are able to see your app

[share_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[share_link]: https://titanic1prediction.streamlit.app/
