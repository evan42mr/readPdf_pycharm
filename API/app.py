import json
from flask import jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import DsmeText

from flask import Flask

app = Flask(__name__)

table_name = ''
"""
sql alchemy session
"""
db_id = 'dev'
pw = '424242'
ip = '192.168.0.230'
data_base = 'dsme_phase2'

Base = declarative_base()
engine = create_engine(f'mysql+pymysql://{db_id}:{pw}@{ip}/{data_base}',
                       encoding='utf-8',
                       echo=False)

Session = sessionmaker(bind=engine)


from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from flask import Flask

app = Flask(__name__)


"""
sql alchemy session
"""
db_id = 'dev'
pw = '424242'
ip = '192.168.0.230'
data_base = 'dsme_phase2'

Base = declarative_base()
engine = create_engine(f'mysql+pymysql://{db_id}:{pw}@{ip}/{data_base}',
                       encoding='utf-8',
                       echo=False)

Session = sessionmaker(bind=engine)



@app.route('/readAll')
def read_all():
    session = Session()
    qry = session.query(DsmeText).all()
    return jsonify(qry = [i.serialize for i in qry])




if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.0.229', port=6000)

# To load json to a dictionary
json.loads
# To convert dictionary to json
json.dumps




