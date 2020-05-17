FROM tiangolo/uwsgi-nginx-flask:python3.6
WORKDIR /usr/server/app
COPY . .
RUN ls -la
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip install pipenv
RUN ls -la
RUN pipenv install --deploy --ignore-pipfile
EXPOSE 8080
ENV FLASK_APP=app.py
CMD [ "uwsgi", "uwsgi.ini" ]