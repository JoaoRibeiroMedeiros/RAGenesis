# Use the official lightweight Python image.
FROM python:3.9-slim

# Set the working directory in the container.
WORKDIR /app

RUN pip install --upgrade pip setuptools

# Copy the requirements file into the container.
COPY requirements.txt requirements.txt

RUN /bin/sh

# Install the python dependencies.
RUN pip install -r requirements.txt

# Copy the rest of the working directory contents into the container at /app.
COPY . .

# Expose the port that streamlit is running on.
EXPOSE 8080

# Command to run the app, assuming your main Streamlit script is named app.py
CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]