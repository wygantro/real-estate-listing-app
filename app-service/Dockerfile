# Dockerfile

FROM python:3.11.1
RUN pip install --upgrade pip
WORKDIR /app-service

ENV APP_HOME /app-service
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r ./requirements.txt

# database env
ENV DB_USER=user
ENV DB_PASS=postgres
ENV SQLALCHEMY_DATABASE_URI=app-service-db
#ENV DB_HOST=10.79.48.5
ENV DB_HOST=34.68.47.133
ENV DB_PORT=5432

# Expose port 5000
EXPOSE 5000

# Run the Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]