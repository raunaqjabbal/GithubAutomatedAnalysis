FROM python:3.8
EXPOSE 8080
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \ cloc
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]