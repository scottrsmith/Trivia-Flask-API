## Introduction to the Full Stack Trivia API 

The Trivia application is a web-based app that allows for the playing of trivia games.

The application:

1) Display questions - both all questions and by category. Questions show the question, category, and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include a question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started - Backend

### Installing Dependencies

#### Python 3.7 ####

This project uses python 3.7.

To Install: [Python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the root directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies


- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. 

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross-origin requests from the frontend server. 

## Database Setup
With Postgres running, populate the database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory to run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```


## Documentation

### Opening the API Documentation
Documentation is generated with Sphinx.

#### HTML Documentation
From the root folder, open the index file in a browser

```bash
./docs/build/html/index.html
```

#### PDF Documentation

The PDF version of the documentation is located in the root project directory. Named triciaapi.pdf

### Generating documentation

Documentation is generated with Sphinx.

#### Installing Sphinx and support tools

To install Sphinx, reference the documents at https://www.sphinx-doc.org/en/master/usage/installation.html

For example:

```bash
 pip install -U sphinx
```

Install dependencies by navigating to the `root` project directory and running:

```bash
cd docs
pip install m2r
pip install recommonmark
pip install rinohtype
pip install -r requirements.txt
```


#### Generating the documentation
Generate the documentation with the following commands:

```bash
# From the root project directory
# Convert readme to rst to be included in generated docs
m2r README.md README.rst --overwrite
cp -R README.rst ./docs/source
cd ./docs
make html
# Make pdf
make latexpdf
cd ..
cp -R ./docs/build/latex/triviaapi.pdf .
```


## API End Points

The following APIs are available. Detailed html documentation can be found in the 'docs' folder.


- Create or Search Questions. This API will create a new question or search questions.
- Retrieve Questions. This API will retrieve a page of 10 trivia questions sorted by question_id. 
- Delete Question. This API will delete a question from the database.
- Retrieve Category. This API will retrieve a list of trivia categories.
- Retrieve Category Questions. This API will retrieve a list of questions by category Id.
- Play Quiz. This API will play the quiz. Presenting a random, non-repeated question in the category.


## Error Handling

Errors are returned as JSON objects in the following format:
```bash
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```

The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable 
- 500: Internal Server Error


## Testing

Testing is done with UnitTest

From the trivia/backend folder. Run:

```bash
. ./test.sh
```

## Full Stack Trivia API Frontend

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

## Required Tasks

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. To run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>
