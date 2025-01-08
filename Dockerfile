FROM python:3.11-slim
 
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

ENV AWS_IP_RANGES_URL=https://ip-ranges.amazonaws.com/ip-ranges.json
ENV REGION_FILTER=eu-west-
ENV IPS_REFRESH_TIME=86400

COPY ./app /app

EXPOSE 5000

ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "access_verifier:app"]