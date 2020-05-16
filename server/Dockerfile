FROM tiangolo/uwsgi-nginx-flask:python3.6
WORKDIR /usr/server/app
COPY . .
RUN ls
RUN python3.6 -m pip install pipenv
RUN pipenv --python 3.6
RUN pipenv install --deploy
RUN . $(pipenv --venv)/bin/activate
EXPOSE 2020
ENV FLASK_APP=app.py
CMD flask run -h 0.0.0.0 -p = 80