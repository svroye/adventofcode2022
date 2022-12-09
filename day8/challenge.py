'''
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as
 a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from
outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390
Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is,
only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example,
that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?
'''

with open('./input.txt', 'r') as f:
    data = [line.strip('\n') for line in f.readlines()]

count = 0

def execute(data):
    count = 0

    number_of_rows = len(data)
    for row_idx in range(len(data)):
        current_row = data[row_idx]
        number_of_columns = len(current_row)
        for column_idx in range(number_of_columns):
            if row_idx == 0 or row_idx == number_of_rows - 1 or column_idx == 0 or column_idx == number_of_columns - 1:
                count += 1
                continue
            current_value = data[row_idx][column_idx]
            from_left = [i for i in range(0, column_idx) if data[row_idx][i] < current_value]
            from_right = [i for i in range(number_of_columns - 1, column_idx, -1) if data[row_idx][i] < current_value]
            from_top = [i for i in range(0, row_idx) if data[i][column_idx] < current_value]
            from_bottom = [i for i in range(number_of_rows - 1, row_idx, -1) if data[i][column_idx] < current_value]
            if len(from_left) == column_idx or len(from_right) == number_of_columns - column_idx - 1\
                or len(from_top) == row_idx or len(from_bottom) == number_of_rows - row_idx - 1:
                count += 1
    return count

test_data = [
'30373',
'25512',
'65332',
'33549',
'35390'
]

print(execute(data))


'''
--- Part Two ---
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a
lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the
same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't
be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4
(found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?
'''


def execute_optimal_place(data):
    max_score = 0

    number_of_rows = len(data)
    for row_idx in range(1, number_of_rows - 1):
        current_row = data[row_idx]
        number_of_columns = len(current_row)
        for column_idx in range(1, number_of_columns - 1):
            current_value = data[row_idx][column_idx]

            to_left = 0
            for i in range(column_idx - 1, -1, -1):
                if data[row_idx][i] < current_value:
                    to_left += 1
                elif data[row_idx][i] >= current_value:
                    to_left += 1
                    break

            to_right = 0
            for i in range(column_idx + 1, number_of_columns):
                if data[row_idx][i] < current_value:
                    to_right += 1
                elif data[row_idx][i] >= current_value:
                    to_right += 1
                    break

            to_top = 0
            for i in range(row_idx - 1, -1, -1):
                if data[i][column_idx] < current_value:
                    to_top += 1
                elif data[i][column_idx] >= current_value:
                    to_top += 1
                    break

            to_bottom = 0
            for i in range(row_idx + 1, number_of_rows):
                if data[i][column_idx] < current_value:
                    to_bottom += 1
                elif data[i][column_idx] >= current_value:
                    to_bottom += 1
                    break

            score = to_left * to_right * to_top * to_bottom

            max_score = max(max_score, score)
    return max_score




print(execute_optimal_place(data))
