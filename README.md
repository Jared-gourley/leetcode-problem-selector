# Leetcode Problem Selector
A program to randomly select the next problem from a pool of categories. Inspired by [neetcode.io](https://neetcode.io/practice) Practice which sorts problems into categories, but often makes them easier by spoiling said category thus giving a major hint on the required approach. With this problem selector, select as many categories as you like and then randomly receive the next unsolved problem from one of these categories, bringing back some of the challenge in identifying the type of problem.

### Usage

`pip install termcolor` <br />
`python3 leetcoder.py` <br />

Given a problems.txt file (example included), the script provides a console user interface to add desired categories into the pool and then receive questions. The script was designed with the intention that each category's problems should be done in order, and provides them to you as such. 


<p></p>problems.txt info: <br />

- The problems file consists of several paragraph blocks, where the first line of the block represent the name of the category and every other line in the block is a problem inside that category. There must be at least one blank line in between each block to distinguish them from each other.
- The Unicode ★ symbol is a delimiter in the file placed after the name of a problem to show that it is completed. The text on the same line after the star essentially serves as a comment to yourself and does not affect parsing.
- A difficulty tag can optionally be included directly after the name of the problem (but before the ★). On the console interface, (easy), (medium), and (hard) with brackets case-sensitive are valid key phrases that are specially handled when colouring and printing.


<p></p>Script running info:

- Currently there is no option to change the selection of categories inside the program. To do this, you would just have to exit the program and start again.
- There also is no way to 'un-solve' a problem as this seemed less common of an issue. For this you would delete the problem's ★ and everything to its right in the problems.txt file itself. (You can also manually mark problems as solved by adding the star in this way)

<br />

#### Note
This script could definitely be used for purposes other than Leetcode problems, and applies to any situation which has categories of tasks which need to be completed in order. With a bit of editing the script could also be used for unordered tasks as well (if it's worth the effort).