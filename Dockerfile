# We choose an official and lightweight Python image as our base
FROM python:3.11-slim

# We set the working directory inside the container
WORKDIR /app

# We copy the list of requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We copy the rest of our code to the container
COPY . .

# Komenda, która uruchomi nasz serwer
CMD ["python", "main.py"]