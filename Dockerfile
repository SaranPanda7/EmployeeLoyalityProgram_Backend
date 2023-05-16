FROM python:3.9.13

# set working directory as app

#RUN pip install virtualenv
#RUN python -m venv /env/Scripts

#ENV PATH="/env/Scripts/activate:$PATH"

WORKDIR /app

# copy requirements.txt file from local (source) to file structure of container (destination) 
COPY requirements.txt requirements.txt

# Install the requirements specified in file using RUN
RUN pip install -r requirements.txt

# copy all items in current local directory (source) to current container directory (destination)
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--reload", "--host=0.0.0.0", "--port", "8000"] 
#CMD python -m uvicorn app.main:app --port 8080
