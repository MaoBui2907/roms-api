FROM ubuntu:18.04
COPY server /app
WORKDIR /app
RUN ls
RUN python -m pip install pipenv
RUN pipenv --python 3.6
RUN pipenv install --deploy
RUN . $(pipenv --venv)/bin/activate
EXPOSE 2020
CMD [ "python", 'app.py' ]
