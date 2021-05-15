from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class DTM(db.Model):
    """
    Define 'DTM' class model representing 'dtm' database table

    Columns:
    dtm_id:             Unique integer key for each DTM entity
    author_id:          Unique integer key to for each author entity
    title:              Title of a DTM entity
    copyright_info:     Copyright and license information for a DTM entity
    foreign_landing_url:        Link of landing page of a DTM entity
    """

    # Table name:
    __tablename__ = "dtm"

    # Columns:
    dtm_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    languages = db.Column(db.String)
    download_links = db.Column(db.String)
    copyright_info = db.Column(db.String)
    foreign_landing_url = db.Column(db.String)
