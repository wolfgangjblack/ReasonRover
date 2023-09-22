# ReasonRover
Utilize Tree-of-thought to explore complex problem solving in Large Language Models:

Data Modified: 9/14/23
Author: Wolfgang Black

This repositiory contains code exploring the [Tree-of-Thought method](https://arxiv.org/pdf/2305.08291.pdf) (ToT). In this paper, 
the authors use the Tree-of-Thought to solve sudoku problems. To explore this, in this repo there are a series of different sudoku problems
increasing the grid size of the problems and the difficulty of the problems found in the 9x9 grid. This determines whether the tree-of-thought method as implemented in [langchain]() can solve this range of problems. The parameters k, c, and modeltype are all explored. These parameters are explain before

## Parameters of Exploration
### Tuneable parameters:
<b>k:</b> the maximum number of interactions -This will range from 5-50 per given problem with an break condition on a successful solution <br>
<b>c:</b> the maximum number of child thoughts - this will be a function of grid size<br>
<b>modeltype:</b> Here we'll use text-davinci-003 

### Problem Parameters:
The majority of the sudoku problems and their solutions have been sourced from http://www.sudoku-download.net <br>
<b>difficulty:</b> base, easy, medium, hard, expert - base is a problem gathered from the paper, the rest indicate increasing difficulty. Difficulty is a function of how many spaces are revealed at the start of the problem and how if a specific technique is required to be used to arrive at the solution (brick, ladder, ect) <br>
<b>grid size:</b> #x# - the grid sizes explored in this problem range from 4x4 - 9x9, with increasing sizes yielding increasing difficulty. 

## Dependencies

## Usage 
Note: This is a [WIP] and main.py does not yet exist. 
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
easy            base            medium          hard            Solution 
3, 4, *, 2,     3, *, *, 2      3, *, *, 2      3, *, *, 2      3, 4, 1, 2
1, *, 3, *      1, *, 3, *      1, *, 3, *      1, *, 3, *      1, 2, 3, 4
*, 1, *, 3      *, 1, *, 3      *, 1, *, 3      *, 1, *, 3      2, 1, 4, 3
$, *, *, 1      4, *, *, 1      4, *, *, *      *, *, *, *      4, 3, 2, 1

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

As to be expect, we see that the average number of interactions increases as we increase problem difficulty. Difficulty here is proxied by decreasing the number of initially populated cells. 

![alt text](https://github.com/wolfgangjblack/ReasonRover/blob/main/src/artifacts/avg_k.jpg)

Similarly, we can also see that not all initial conditions are equal. While the difficulty rating indicated the number of initial populated parameters, they didn't share the same number of blank rows, columns, or populated indices. As such, the actual difficulty within a difficulty band could vary. We see that while it was a hard problem that required the highest number of interactions ([hard,base] required k = 85), the second highest k occured at medium base. 

![alt text](https://github.com/wolfgangjblack/ReasonRover/blob/main/src/artifacts/max_k.jpg)

### 5x5, 9x9

From the paper, LLM Guided Tree-of-Thought, we see that the model starts to perform poorly at puzzles larger than 4x4. I suspect this is partially because of the increased difficulty of the parameters and the blank spaces. For example, if we have 8 blank spaces in a 4x4 we have a total of 4**8 of a permutation with repitition of ~66k. If we increase the grid (and therefore possible ints) from 4 to 5, we now have a permutation of 5**8 or 390k. While this is an order of magnitutde greater in the problem space, the paper shows a decrease of 10% is the models ability to solve the 5x5 grid. An interesting observation, from the [GitHub](https://github.com/jieyilong/tree-of-thought-puzzle-solver) associated with LLM Guided Tree-of-Thought we see that the 4x4 problem had 12 blanks, and the 5x5 problem had 11 - this gives us brute force permutations on the order of 1e8 (with 5**11 ~ 3x 4**12). If we assume this scale as a proxy of difficulty we can roughly estimate that to be solvable with the initial parameter used in the paper (k = 20, c = 8) then to solve a 9x9 we can only have 8 blank parameters. While this isn't necessarily a linear scaling (or the best substiture for difficulty) we'll explore 5x5 with 3 different initial configurations of 11 blank spaces, and then 9x9 with 6 different configurations. The first 3 configurations will all have 8 blanks, the second 3 will have 10, 15, 20. For the equivalent permutation space (11 blanks at 5x5 and 8 blanks at 9x9) we'll allow $k_{max} == 40$ and $c = 12$. For the increasing blank spaces in the 9x9 we'll allow $40 \leq k_{max} \leq 100$ and $c = 12$. 

#### Results:
Unlike the results found in the article, we were unable to solve any of the 5x5 or 9x9 puzzles we presented to the tree-of-thought agent. Its important to note that we considered one puzzle with many different initial conditions, and considered the initial blank count as the difficulty this isn't a real measurement of difficulty in sudoku. We did use a puzzle the journal paper git repo used and was able to solve, but fixed the children at 12 and k = 40. With additional testing we're confident we could solve the 5x5 at least. However, the project is costly and as such we'll end here. The main takeaway is that while this method DOES improve the problem solving abilities of an LLM it also comes with its challenges. 


### TLDR:

1. This repo expored [Tree-of-Thought](https://arxiv.org/pdf/2305.08291.pdf) method to solve sudoku puzzle
2. Good results were found for a 3x3, however results were not as conclusive for 5x5, 9x9
3. While this method does show some promise for helping an LLM reason, the final solution MUST be known and the method does not generalize well even on problems of the same type. 
4. Tree-of-Thought may work better with a specialist model over a generalist model 

#### Notes:

<b> k vs c </b> <br>
Originally I wanted to explore total thoughts (k) vs C (number of children). But what I'm finding from the library is that as we increase depth (step down further into children nodes) we consume thoughts. Therefor, we already know theoretical upper limit of thoughts/children. We know that the max number of children is equal to the number of blank spaces in the puzzle and the number of unique thoughts is the possible integers raised to the blank spaces. 

For example, if we have a 9x9 puzzle with 25 spaces to fill that can be anything from 1-9 we could say there are a total of 9**25 unique thoughts. It should be noted that this is a max for a brute search and neglects any rules about what numbers go where.  Instead of exploring k vs c then, we'll explore the idea of this increasing permutation space based on grid size and initial conditions.

## Costs:
So far, utilizing text-davinci-003 I've run around 6 hours with a total cost of ~$25
