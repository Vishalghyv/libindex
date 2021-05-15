# EBCatalog
## Ebooks Catalog
This is a database of books (digital, audio, scanned). The metadata for the books is collected from 3 major sources: Project Gutenberg, Internet Archives, Library Genesis. See this [proposal](#) for details about the project.

To run the project:
1. Install all the requirements mentioned in the `requirements.txt`.
2. From the root directory of the project, run `python ./manage.py flask run` (For Windows make an environment according to step 1 and then run `.\py ./manage.py flask run`). Visit http://localhost:5000/ to see the application running.

To generate TSV output file from providers:
Note that if the database is already filled, the script should not be executed again.
1. `cd` to `/application/pipeline/` and run `python project_gutenberg.py` (For Windows run `py project_gutenberg.py`). The output file will be created in `/application/pipeline/output` directory.

For initial development setup:
1. Clone the project in your local machine.
2. Install all the requirements from requirements.txt.
3. Create a postgresql database. Set the name of the database as the value for the `APPLICATION_DB` environment variable in the `development.json` file in `config/` folder. Also set OUTPUT_DIR in `config/.env` to point at `application/pipeline/output` directory.
4. `cd` into: `cd libindex/application/pipeline` and run `python project_gutenberg.py` (For Windows run `py project_gutenberg.py`).
5. `cd` into the project root and from there run `python ./manage.py flask run` (For Windows make an environment according to step 1 and then run `.\py ./manage.py flask run`). Visit http://localhost:5000/loading to load the data in `application/pipeline/output/{tsv_file_name}.tsv` into the database.

## Project Made by:
### Group 09
Member details:
1. Shubham Singh - 19/11/EC/050
2. Kartik Ohri - 19/11/EC/049
3. Vishal Chaudhary - 19/11/EC/021
4. Sidharth Kumar - 19/11/EC/044
5. Pragyan Jaiminy - 19/11/EC/028
6. Abhishek Jain - 19/11/EC/036
