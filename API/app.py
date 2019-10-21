import json
from flask import jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from models import DsmeText

from flask import flash, request
from flask import Flask
import mysql.connector as mariadb
from flask_cors import CORS

with open('config.json') as f:
    config_dict = json.loads(f.read())

db_id = config_dict['data_base']['db_id']
pw = config_dict['data_base']['pw']
ip = config_dict['data_base']['ip']
data_base = config_dict['data_base']['data_base']

app = Flask(__name__)
CORS(app)

@app.route('/read_annual/<string:file_year>',  methods=['GET'])
def read_annual(file_year):
    try:
        mydb = mariadb.connect(
            host=ip,
            user=db_id,
            passwd=pw,
            database=data_base
        )
        cursor = mydb.cursor()
        file_name = 'dsme_tender_spec_' + file_year
        sql = "SELECT * FROM %s" % (file_name,)
        cursor.execute(sql)
        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        result = []
        for row in rows:
            row = dict(zip(columns, row))
            result.append(row)


        resp = jsonify(result)

        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        mydb.close()

@app.route('/readAll/<string:file_name>',  methods=['GET'])
def read_all(file_name):
    try:
        mydb = mariadb.connect(
            host=ip,
            user=db_id,
            passwd=pw,
            database=data_base
        )
        cursor = mydb.cursor()
        # sql = "SELECT * FROM " + file_name
        sql = "SELECT * FROM %s" % (file_name,)
        cursor.execute(sql)
        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        result = []
        for row in rows:
            row = dict(zip(columns, row))
            result.append(row)


        resp = jsonify(result)

        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        mydb.close()




# Using sqlAlchemy
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
"""



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=6000)

# # To load json to a dictionary
# json.loads
# # To convert dictionary to json
# json.dumps




