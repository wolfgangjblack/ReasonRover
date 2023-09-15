# ReasonRover
Utilize Tree-of-thought to explore complex problem solving in Large Language Models:

Data Modified: 9/14/23
Author: Wolfgang Black

This repositiory contains code exploring the [Tree-of-Thought method](https://arxiv.org/pdf/2305.08291.pdf) (ToT). In this paper, 
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

## Experiment
### 4x4 with different starting conditions
First to understand how this code works, we verified that the ToT method could solve a 4x4 problem presented in the paper. This problem was of the form

Problem                     Solution
```
3, *, *, 2                  3, 4, 1, 2
1, *, 3, *                  1, 2, 3, 4
*, 1, *, 3      ->          2, 1, 4, 3
4, *, *, 1                  4, 3, 2, 1
```

The ToT method, implemented with MyChecker() class was able to solve this with k = 10, c = 8. However, the form is relatively easy and straight forward. To understand how we can use this same form to explore k we changed the number of initial populated parameters and the populated pattern.


Example Initial Conditions
```
easy        base        medium        hard


```
#### Results
1. Did it ever generate a false answer, or fail to solve?
    - for the base 4x4 problem, this checker never failed to solve the problem with ``` 8 <= c <= 12 ``` and ```k <= 100```
2. How many initial parameters per easy, base, hard, medium?

    | Difficulty | total populated IC (out of 16) | Number of blank columns*| Number of blank rows* |
    |-|-|-|-|
    | easy | 9 | 0 | 0 |
    | base | 8 | 0 | 0 |
    | medium | 7 | 1| 8|
    | hard | 6 |1 | 1|

* Note, not all cases in the difficulty category may have the same number of blank columns/rows. This should be considered the max amount of blank rows/columns per difficulty. For the hard problem, [hard, 1] did have 1 blank row AND column

3. Avg K per problem type/k per problem type


### k vs C

[WIP]

### 5x5, 9x9

## Costs:
So far, utilizing text-davinci-003 I've run around 4 hours with a total cost of $19