# use an lightweight Python runtime as a parent image
FROM python:3.10-slim

# set the working directory
WORKDIR /app

# copy the dependency list and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy all code and model files to the container
COPY . .

# tell Docker the port the app runs on
EXPOSE 8000

# startup command (use 0.0.0.0 so the API is accessible outside the container)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]