FROM python:2.7

WORKDIR /app

COPY . /app

RUN pip install --no-cache-di -r req.txt

#Non Root User Configuration
RUN useradd -ms /bin/sh 10000 && chown -R 10001:10000 /app

USER 10000

EXPOSE 8000

ENTRYPOINT python api/app.py
