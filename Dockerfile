FROM python:3.9

WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DATABASE_URL postgres://user:password@db:5432/app
ENV SNS_TOPIC_ARN arn:aws:sns:us-east-1:123456789012:my-topic
ENV AWS_ACCESS_KEY_ID my-access-key-id
ENV AWS_SECRET_ACCESS_KEY my-secret-access-key
ENV AWS_DEFAULT_REGION us-east-1
CMD python cart_app.py