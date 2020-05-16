FROM python:3.6.10
WORKDIR /usr/server/app
RUN ls
RUN python3.6 -m pip install pipenv
RUN pipenv --python 3.6
RUN pipenv install --deploy
RUN . $(pipenv --venv)/bin/activate
EXPOSE 2020
COPY . .
CMD [ "python", 'app.py' ]
