FROM docker.io/python:3

WORKDIR /app
COPY requirements.txt ./
RUN python -m venv .venv
RUN .venv/bin/pip install -r requirements.txt
COPY . ./

CMD [".venv/bin/gunicorn", "-b", "0.0.0.0", "--access-logfile", "/dev/stdout", "--error-logfile", "/dev/stderr", "wsgi:app"]
