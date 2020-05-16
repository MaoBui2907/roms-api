FROM ubuntu:18.04
RUN ls
RUN apt install python3.6 python3-pip
RUN python3.6 -m pip install pipenv
RUN pipenv --python 3.6
RUN pipenv install --deploy
RUN . $(pipenv --venv)/bin/activate
EXPOSE 2020
CMD [ "python", 'app.py' ]
