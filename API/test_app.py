import json
from flask import jsonify

from flask import Flask
import mysql.connector as mariadb
from flask_cors import CORS
import functions
import subprocess
from flask_caching import Cache

with open('config.json') as f:
    config_dict = json.loads(f.read())

db_id = config_dict['data_base']['db_id']
pw = config_dict['data_base']['pw']
ip = config_dict['data_base']['ip']
data_base = config_dict['data_base']['data_base']

app = Flask(__name__)
CORS(app)

config = {
    # "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple" # Flask-Caching related configs
    # "CACHE_DEFAULT_TIMEOUT": 3600
}
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)
# FILE_NAME = '2_Tender_Part+I+Appendix-ABB1F.pdf'
# FILE_NAME = '2.2.4_Shipyard_ITT_Attachment.pdf'
# FILE_NAME = 'KOGAS-2449.pdf'
# FILE_NAME = 'ON-2462.pdf'

# # ------------- TEST ---------------
# table_year = '2020'
# mydb = mariadb.connect(
#             host=ip,
#             user=db_id,
#             passwd=pw,
#             database=data_base
#         )
# cursor = mydb.cursor()
# table_name = 'dsme_tender_spec_' + table_year
#
# # Used to name a table in a database
# file_name_without_extension = FILE_NAME.split('.pdf', 1)[0]
# # Same file but with .txt format
# file_name_txt = file_name_without_extension + '.txt'
# # Make a program to wait until shell command completes
# subprocess.call(["pdftotext", "-layout", FILE_NAME, file_name_txt])
#
# cleaned_text = functions.remove_line_numbers(file_name_txt)
#
# lines_before_pgbrk, lines_after_pgbrk = functions.count_pgbrk_borders(cleaned_text)
#
# text_without_pgbrk = functions.sliding_window(lines_before_pgbrk, lines_after_pgbrk, file_name_txt)
#
# content_table, tab_end_line = functions.extract_content_table(text_without_pgbrk)
#
# line_num = 0
# functions.find_titles(mydb, table_name, file_name_without_extension, text_without_pgbrk, content_table, line_num, tab_end_line)
#
# lst_not_found_titles = []
# while content_table:
#     line_num = functions.find_titles(mydb, table_name, file_name_without_extension, text_without_pgbrk, content_table, line_num, tab_end_line)
#     if content_table:
#         lst_not_found_titles.append(content_table.pop(0))
# print("Process finished")
# # ______________ TEST __________

@app.route('/post_annual/with_numbers/<string:table_year>',  methods=['POST'])
def post_annual_numbers(table_year):
    try:
        FILE_NAME = '2.2.4_Shipyard_ITT_Attachment.pdf'
        mydb = mariadb.connect(
            host=ip,
            user=db_id,
            passwd=pw,
            database=data_base
        )
        cursor = mydb.cursor()
        table_name = 'dsme_tender_spec_' + table_year

        # Used to name a table in a database
        file_name_without_extension = FILE_NAME.split('.pdf', 1)[0]
        # Same file but with .txt format
        file_name_txt = file_name_without_extension + '.txt'
        # Make a program to wait until shell command completes
        subprocess.call(["pdftotext", "-layout", FILE_NAME, file_name_txt])

        cleaned_text = functions.remove_line_numbers(file_name_txt)

        lines_before_pgbrk, lines_after_pgbrk = functions.count_pgbrk_borders(cleaned_text)

        text_without_pgbrk = functions.sliding_window(lines_before_pgbrk, lines_after_pgbrk, file_name_txt)

        content_table, tab_end_line, title_indent_spaces = functions.extract_content_table(text_without_pgbrk)

        line_num = 0
        functions.find_titles(mydb, table_name, file_name_without_extension, text_without_pgbrk, content_table,
                              line_num, tab_end_line, title_indent_spaces)

        lst_not_found_titles = []
        while content_table:
            line_num = functions.find_titles(mydb, table_name, file_name_without_extension, text_without_pgbrk,
                                             content_table, line_num, tab_end_line, title_indent_spaces)
            if content_table:
                lst_not_found_titles.append(content_table.pop(0))

        return "Upload of a file finished"


    except Exception as e:
        print(e)
    finally:
        cursor.close()
        mydb.close()


@app.route('/post_annual/<string:table_year>', methods=['POST'])
def post_annual(table_year):
    FILE_NAME = 'ON-2462.pdf'
    try:
        mydb = mariadb.connect(
            host=ip,
            user=db_id,
            passwd=pw,
            database=data_base
        )
        cursor = mydb.cursor()
        table_name = 'dsme_tender_spec_' + table_year

        # Used to name a table in a database
        file_name_without_extension = FILE_NAME.split('.pdf', 1)[0]
        # Same file but with .txt format
        file_name_txt = file_name_without_extension + '.txt'
        # Make a program to wait until shell command completes
        subprocess.call(["pdftotext", "-layout", FILE_NAME, file_name_txt])

        cleaned_text = functions.clean_file_without_line_numbers(file_name_txt)

        lines_before_pgbrk, lines_after_pgbrk = functions.count_pgbrk_borders(cleaned_text)

        text_without_pgbrk = functions.sliding_window(lines_before_pgbrk, lines_after_pgbrk, file_name_txt)

        content_table, tab_end_line, title_indent_spaces = functions.extract_content_table(text_without_pgbrk)

        line_num = 0
        functions.find_titles(mydb, table_name, file_name_without_extension, text_without_pgbrk, content_table,
                              line_num, tab_end_line, title_indent_spaces)

        lst_not_found_titles = []
        while content_table:
            line_num = functions.find_titles(mydb, table_name, file_name_without_extension, text_without_pgbrk,
                                             content_table, line_num, tab_end_line, title_indent_spaces)
            if content_table:
                lst_not_found_titles.append(content_table.pop(0))

        return "Upload finished"
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        mydb.close()

@app.route('/read_annual/<string:table_year>/<string:table_name>',  methods=['GET'])
@cache.cached(timeout=3600)
def read_annual(table_year, table_name):
    try:
        mydb = mariadb.connect(
            host=ip,
            user=db_id,
            passwd=pw,
            database=data_base
        )
        cursor = mydb.cursor()
        file_name = 'dsme_tender_spec_' + table_year
        sql = "SELECT * FROM %s WHERE FILE_NAME = '%s' ORDER BY id ASC" % (file_name, table_name,)
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
@cache.cached(timeout=3600)
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
    app.run(host='0.0.0.0', port=6001)




# ---------------------------->
# # To load json to a dictionary
# json.loads
# # To convert dictionary to json
# json.dumps