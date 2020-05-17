FROM tiangolo/uwsgi-nginx-flask:python3.6
WORKDIR /usr/server/app
COPY . .
RUN ls -la
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip install pipenv
RUN ls -la
RUN pipenv install --deploy --ignore-pipfile
EXPOSE 80
ENV FLASK_APP=app.py
CMD ["pipenv", "run", "flask run -h 0.0.0.0 -p 80"]