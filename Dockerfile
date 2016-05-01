FROM python:3.5.1-onbuild
CMD ["/usr/local/bin/gunicorn", "-w 2", "-b :8000", "carson:app"]
