FROM python:3.9
ENV PYTHONUNBUFFERED True

EXPOSE 8080

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
# RUN sudo apt install cloc -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD streamlit run --server.port 8080 --server.enableCORS false app.py