from flask import Flask, render_template, request
from string import Template
from application.models import DTM
# from application.pipeline import project_gutenberg
import os
import sys


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app(config_name):

    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    from application.models import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/loading')
    def loading():

        if config_name == "development":
            # project_gutenberg.main()
            from application.pipeline import loader
            loader.load_to_dtm_table(db, DTM)
        else:
            return render_template('index.html')

        return config_name

    # Home page
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/submit", methods=['GET', 'POST', 'RESET'])
    def submit():
        if request.method == 'POST':
            try:
                text_entered = request.form['text']
            except:
                return render_template('index.html', message='Please give a valid input')

            if (text_entered == ''):
                return render_template(
                    'index.html', message='Please enter some text input to be searched'
                    )

            try:
                _results = []
                search_terms = text_entered.split()

                for search_term in search_terms:
                    _results.append(DTM.title.contains(search_term))

                _rec = []
                for record in _results:
                    _rec.append(record.title)


            #
            #     return _res.dtm_id
            #
            #         # for res in _res:
            #         #     _results.append(res.dtm_id)
            #     return len(_results)
            #
            #     # results = []
            #     # for dtm_id in _results:
            #     #     entity = DTM.query.filter_by(dtm_id=dtm_id).__dict__
            #     #     results.append(entity)
            #     # ans = results
            except:
                # return render_template('index.html', message='No such item found')
                pass
            return str(_results[2].title)
            # print(ans)
            # return render_template('found.html', output=ans)

    # Docs page and proposal page
    @app.route("/docs")
    def about():
        return render_template('docs.html')

    # Team page
    @app.route("/team")
    def OurTeam():
        return render_template('team.html')

    return app
