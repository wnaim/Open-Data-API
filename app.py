import pandas as pd
import numpy
import math
import os
from flask import *

# education_data_enrollment_by_language = pd.read_excel('/Users/ashar/Downloads/documents-export-2015-02-15/EnrollmentByLanguage.xlsx', 0, index_col=None, na_values=['NA'])
# education_data_sanctioned_non_teaching_staff = pd.read_excel('/Users/ashar/Downloads/documents-export-2015-02-15/SanctionedNonTeachingStaff.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
# education_data_sanctioned_teaching_staff = pd.read_excel('/Users/ashar/Downloads/PBSPSLM_2005-2013.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
# education_data_school_detailed_info = pd.read_excel('/Users/ashar/Downloads/PBSPSLM_2005-2013.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
# education_data_school_teachers_profile = pd.read_excel('/Users/ashar/Downloads/PBSPSLM_2005-2013.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
# education_data_working_non_teaching_staff = pd.read_excel('/Users/ashar/Downloads/PBSPSLM_2005-2013.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
# education_data_working_teaching_staff = pd.read_excel('/Users/ashar/Downloads/PBSPSLM_2005-2013.xlsx', 'Sheet1', index_col=None, na_values=['NA'])

ATTENDANCE_DATA_FILE = "./data_sets/PBSPSLM_2005-2013.xlsx"
CPLC_DATA = "./data_sets/Karachi Killing Data 2013 - CPLC.xls"
open_data_df = pd.read_excel(ATTENDANCE_DATA_FILE, 0, index_col=None, na_values=['NA'])
cplc_data_df = pd.read_excel(CPLC_DATA, 'Combined 2013', index_col=None, na_values=['NA'])
cplc_idx_size = len(cplc_data_df.index._data)
idx_size = len(open_data_df.index._data)

app = Flask(__name__)

@app.route("/api/v1/open_data/education/all", methods=["GET"])
def all():
    to_return = {'data':[], 'end_idx': 0, 'limit':30}
    start_idx = int(request.args.get('start_idx') if request.args.get('start_idx') else 0)
    limit = int(request.args.get('limit') if request.args.get('limit') else 30)
    end = start_idx+limit
    for i in range(idx_size):
        clean = {}
        row_dict = open_data_df.iloc[i].to_dict()
        for key in row_dict:
            if type(row_dict[key]) is numpy.float64 and not math.isnan(row_dict[key]):
                clean[key] = int(row_dict[key])
            elif type(row_dict[key]) is numpy.float64 and math.isnan(row_dict[key]):
                clean[key] = None
            else:
                clean[key] = row_dict[key]
        to_return['data'].append(clean)
    to_return['data'] = to_return['data'][start_idx:end]
    to_return['end_idx'] = end
    to_return['limit'] = limit
    return jsonify(to_return)

@app.route("/api/v1/open_data/education/columns", methods=["GET"])
def columns():
    to_return = {
        "columns": []
    }
    to_return["columns"].extend(open_data_df.columns._data)
    return jsonify(to_return)

@app.route('/api/v1/open_data/education/downloads/<path:filename>', methods=["GET"])
def download(filename):
    downloads = './data_sets/'
    return send_from_directory(directory=downloads, filename=filename)

@app.route("/api/v1/open_data/cplc/all", methods=["GET"])
def cplc_all():
    to_return = {'data':[], 'end_idx': 0, 'limit':30}
    start_idx = int(request.args.get('start_idx') if request.args.get('start_idx') else 0)
    limit = int(request.args.get('limit') if request.args.get('limit') else 30)
    end = start_idx+limit
    for i in range(idx_size):
        clean = {}
        row_dict = cplc_data_df.iloc[i].to_dict()
        for key in row_dict:
            if type(row_dict[key]) is numpy.float64 and not math.isnan(row_dict[key]):
                clean[key] = int(row_dict[key])
            elif type(row_dict[key]) is numpy.float64 and math.isnan(row_dict[key]):
                clean[key] = None
            else:
                clean[key] = row_dict[key]
        to_return['data'].append(clean)
    to_return['data'] = to_return['data'][start_idx:end]
    to_return['end_idx'] = end
    to_return['limit'] = limit
    return jsonify(to_return)

@app.route("/api/v1/open_data/cplc/columns", methods=["GET"])
def cplc_columns():
    to_return = {
        "columns": []
    }
    to_return["columns"].extend(cplc_data_df.columns._data)
    return jsonify(to_return)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)