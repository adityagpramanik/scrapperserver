# Fetch Python 3.12
FROM python:3.12

# The enviroment variable ensures that the python output is set straight to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /scrapperserver

# set working dir
WORKDIR /scrapperserver

# copy contents on current directory into WORKDIR
ADD . /scrapperserver

# create virtual env for the application
RUN apt-get update && \
    apt-get install -y curl git python3-venv && \
    curl https://pyenv.run | bash

ENV PATH="/root/.pyenv/shims:/root/.pyenv/bin:$PATH"

RUN pyenv install 3.12.3 && \
    pyenv global 3.12.3 && \
    pip install --upgrade pip

RUN python -m venv .pyconfig
RUN . .pyconfig/bin/activate

# Run requirements.txt
RUN pip install -r requirements.txt

# Run the application (with manage.py commands)
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]