import os
import glob
import pandas as pd

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(CURRENT_DIR,'output')

def open_tsv():
    file_type = "\*tsv"
    files = glob.glob(OUTPUT_DIR + file_type)
    max_file = max(files, key=os.path.getctime)

    import_file = pd.read_csv(max_file, sep='\t\t')

    return import_file


def load_to_dtm_table(db, dtm_table):
    data = open_tsv()

    data = data.drop(data.columns[[7]], axis=1)
    data.columns = ["dtm_id","title", "author", "languages",
                    "download_links", "copyright_info",
                    "foreign_landing_url"]

    for _, row in data.iterrows():
        entity = dtm_table(
            dtm_id=row[0],
            title=row[1],
            author=row[2],
            languages=row[3],
            download_links=row[4],
            copyright_info=row[5],
            foreign_landing_url=row[6]
        )
        db.session.add(entity)

    db.session.commit()
