# Patten Recommender 

Recommendation system powered by recommendation models.
## Implemented by Team #7

# Dependencies
* Python 3.7
* flask
* sqlite
* pandas

# Instructions to Start the Application

Install packages by

`pip install -r requirements.txt`

Set the env variable
`sudo ./setenv.sh`

Initialize the sqlite db by
`python manage.py initdb`

Download the common stopwords by
`python recommender/download.py`
then select to download the `popular` section.

Start the app by
`python manage.py runserver`
