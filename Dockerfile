FROM python:3.10

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
