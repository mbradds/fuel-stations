FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "fuel-stations", "/bin/bash", "-c"]

# Copy all the python files
COPY . /app

# The code to run when container is started:
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "fuel-stations", "python3", "api.py"]