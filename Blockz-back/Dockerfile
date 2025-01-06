
FROM python:3.9 as python
WORKDIR /code
COPY . .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM mysql:8.0 as mysql
RUN echo "[mysqld]\n\
    bind-address = 0.0.0.0\n\
    port = 3306" > /etc/mysql/conf.d/custom.cnf
EXPOSE 3306
CMD ["mysqld"]
