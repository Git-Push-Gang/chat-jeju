FROM python:3.12-slim

WORKDIR /usr/src

COPY . .

RUN pip install --no-cache-dir -r config/requirements.txt

RUN pip install pre-commit
RUN pre-commit install

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]