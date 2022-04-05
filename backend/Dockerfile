FROM python:3.9
WORKDIR /app
COPY . /app

RUN pip install -r ./requirements.txt
ENV FLASK_ENV development
ENV FLASK_APP hebbia
EXPOSE 3000
WORKDIR /app
# CMD ["gunicorn", "-b", ":3000", "api:app"]
CMD ["flask", "run", "--host=0.0.0.0"]]
