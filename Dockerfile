FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
&& pip install gunicorn

COPY . .
RUN chmod a+x boot.sh

ENV FLASK_APP=simplechat:create_app

EXPOSE 5000

CMD ["./boot.sh"]
