# Dockerfile

FROM python:3.11.1
RUN pip install --upgrade pip
WORKDIR /app-service

ENV APP_HOME /app-service
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r ./config/requirements.txt

# database env
ENV DB_USER=???
ENV DB_PASS=???
ENV DB_NAME=???
ENV DB_HOST=???
ENV DATABASE_URL=???
# ENV DB_HOST=???
# ENV DATABASE_URL=???
ENV DB_PORT=???

# Expose port 5000
EXPOSE 5000

# Run the Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]