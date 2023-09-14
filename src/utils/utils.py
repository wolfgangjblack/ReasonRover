import os
import json


def set_openai_apikey(api_dir):
    f = open(api_dir, 'r')
    key = f.readline()
    os.environ['OPENAI_API_KEY'] = key
    return

def get_sudoku_data(problem_dir:str) -> dict: 
   # reading the data from the file
    with open(problem_dir) as f:
        data = f.read()
        
    # reconstructing and return the data as a dictionary
    return json.loads(data)

    