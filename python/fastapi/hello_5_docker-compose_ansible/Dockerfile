FROM python:3.11-slim

# Set the current working directory to /code.
# This is where we'll put the requirements.txt file and the app directory.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
# Copy only the file with the requirements first, not the rest of the code.
# As this file doesn't change often, Docker will detect it and use the cache for this step,
# enabling the cache for the next step too.
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file.
# The --no-cache-dir option tells pip to not save the downloaded packages locally,
# as that is only if pip was going to be run again to install the same packages,
# but that's not the case when working with containers.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the ./app directory inside the /code directory.
# As this has all the code which is what changes most frequently
# the Docker cache won't be used for this or any following steps easily.
# So, it's important to put this near the end of the Dockerfile,
# to optimize the container image build times.
COPY ./app /code/app

# Set the command to run the uvicorn server.
# CMD takes a list of strings, each of these strings is what you would type in the command line separated by spaces.
# This command will be run from the current working directory,
# the same /code directory you set above with WORKDIR /code.
# Because the program will be started at /code and inside of it is the directory ./app with your code,
# Uvicorn will be able to see and import app from app.main.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]