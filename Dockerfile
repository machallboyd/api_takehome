FROM python:3.10.8
WORKDIR /api_homework

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /api_homework/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]