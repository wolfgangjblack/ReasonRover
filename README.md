# ReasonRover
Utilize Tree-of-thought to explore complex problem solving in Large Language Models:

Data Modified: 9/14/23
Author: Wolfgang Black

This repositiory contains code exploring the [Tree-of-Thought method](https://arxiv.org/pdf/2305.08291.pdf). In this paper, 
the authors use the Tree-of-Thought to solve sudoku problems. To explore this, in this repo there are a series of different sudoku problems
increasing the grid size of the problems and the difficulty of the problems found in the 9x9 grid. This determines whether the tree-of-thought method as implemented in [langchain]() can solve this range of problems. The parameters k, c, and modeltype are all explored. These parameters are explain before

## Parameters of Exploration
### Tuneable parameters:
<b>k:</b> the maximum number of interactions -This will range from 5-50 per given problem with an break condition on a successful solution
<b>c:</b> the maximum number of child thoughts - this will be a function of grid size
<b>modeltype:</b> Here we'll use both text-davinci-003 and ChatGPT-3.5-turbo

### Problem Parameters:
The majority of the sudoku problems and their solutions have been sourced from http://www.sudoku-download.net
<b>difficulty:</b> base, easy, medium, hard, expert - base is a problem gathered from the paper, the rest indicate increasing difficulty. Difficulty is a function of how many spaces are revealed at the start of the problem and how if a specific technique is required to be used to arrive at the solution (brick, ladder, ect)
<b>grid size:</b> #x# - the grid sizes explored in this problem range from 4x4 - 9x9, with increasing sizes yielding increasing difficulty. 

## Dependencies

## Usage
To run this code:
1. first in the terminal and root directory, install the requirements by ```pip install -r requirements.txt```
2. step into ```./scr```
3. type ```'python main.py```
4. if the code runs to completion, results can be found in ```./src/artifacts```

## Results

<b>WIP</b>

## Costs:
