######## Imports and Keys
import re
from typing import Tuple
import os
import json

from utils.utils import set_openai_apikey, get_sudoku_data
api_dir = '../apikeys/api.txt'
set_openai_apikey(api_dir)

from langchain.llms import OpenAI
from langchain_experimental.tot.base import ToTChain
from langchain_experimental.tot.checker import ToTChecker
from langchain_experimental.tot.thought import ThoughtValidity
######## Initialize LLM using OpenAI
modeltype = "text-davinci-003"
llm = OpenAI(temperature=0.1, max_tokens=512, model=modeltype)

class MyChecker(ToTChecker):
    def evaluate(self,
        problem_description: str,
        thoughts: Tuple[str, ...] = ()) -> ThoughtValidity:
        
        last_thought = thoughts[-1]
        clean_solution = last_thought.replace(" ", "").replace('"', "")
        regex_solution = clean_solution.replace("*", ".").replace("|", "\\|")
        if sudoku_solution in clean_solution:
            return ThoughtValidity.VALID_FINAL
        elif re.search(regex_solution, sudoku_solution):
            return ThoughtValidity.VALID_INTERMEDIATE
        else:
            return ThoughtValidity.INVALID

######## There are multiple files within the data directory - note, files came mostly from http://www.sudoku-download.net/sudoku_8x8.php
datadir = 'data/'
artifactsdir = 'artifacts/'
savefile = 'output.json'
out_dict = {}
for i in os.listdir('data/'):
    
    filename = i
    tile_size = filename.split('.')[0].split('_')[-1]
    
    sudoku_data = get_sudoku_data('data/'+i)
    sudoku_puzzle = sudoku_data['sudoku_puzzle']
    sudoku_solution = sudoku_data['sudoku_solution']

    problem_description = f"""
    {sudoku_puzzle}

    - This is a {tile_size} Sudoku puzzle.
    - The * represents a cell to be filled.
    - The | character separates rows.
    - At each step, replace one or more * with digits 1-{tile_size.split('x')[0]}.
    - There must be no duplicate digits in any row, column or subgrid.
    - Keep the known digits from previous valid thoughts in place.
    - Each thought can be a partial or the final solution.
    """.strip()


    print(problem_description)

    #######
    # The following code implement a simple rule based checker for 
    # a specific 4x4 sudoku puzzle.
    #######



    #######
    # Testing the MyChecker class above:
    #######
    checker = MyChecker()
    ####We'll only test the base problem like such
    if i == 'base_problem_4x4.txt':
        assert checker.evaluate("", ("3,*,*,2|1,*,3,*|*,1,*,3|4,*,*,1",)) == ThoughtValidity.VALID_INTERMEDIATE
        assert checker.evaluate("", ("3,4,1,2|1,2,3,4|2,1,4,3|4,3,2,1",)) == ThoughtValidity.VALID_FINAL
        assert checker.evaluate("", ("3,4,1,2|1,2,3,4|2,1,4,3|4,3,*,1",)) == ThoughtValidity.VALID_INTERMEDIATE
        assert checker.evaluate("", ("3,4,1,2|1,2,3,4|2,1,4,3|4,*,3,1",)) == ThoughtValidity.INVALID

    #######
    # Initialize and run the ToT chain, 
    # with maximum number of interactions k set to 30 and 
    # the maximum number child thoughts c set to 8.
    #######

    for j in range(1, 11):
        k = 5*j
        c = 5
        tot_chain = ToTChain(llm=llm, checker=MyChecker(), k=50, c=c, verbose=True, verbose_llm=False)
        solution = tot_chain.run(problem_description=problem_description)
        if solution == sudoku_solution:
            break

    out_dict[i] = {'model':modeltype,
                'description': problem_description,
                'problem': sudoku_puzzle,
                'known solution': sudoku_solution,
                'tot_solution': solution,
                'k': k,
                'c': c}

with open(artifactsdir+savefile, "w") as json_file:
    json.dump(out_dict, json_file)
print(f"Dictionary saved to {artifactsdir+savefile}")
    #######