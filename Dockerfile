FROM python:3.5.1-onbuild
MAINTAINER gnm@the-merritts.net
EXPOSE 8080
ENV SQLALCHEMY_DATABASE_URI "sqlite:////tmp/carson_db.sqlite3"
CMD ["/usr/local/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "carson:app"]
