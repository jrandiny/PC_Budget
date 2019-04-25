#!/usr/bin/env python3
from collections import deque
import importer
import sys

def budgeting(item,tahap, budget):
    optimum = []
    item_pick = []

    for curr_tahap in range(tahap):
        # print('Tahap {}'.format(curr_tahap))
        optimum.append([0 for _ in range(budget+1)])
        item_pick.append([-1 for _ in range(budget+1)])
        for curr_budget in range(budget+1):
            temp_max = 0
            temp_pick = []
            for k in range(len(item[curr_tahap])):
                calculated_cost = item[curr_tahap][k]['cost'] 
                if(curr_tahap != 0):
                    index_search = curr_budget-calculated_cost
                    if(index_search >=0 and index_search <= budget):
                        calculated_value = item[curr_tahap][k]['value'] + optimum[curr_tahap-1][index_search]
                    else:
                        calculated_value = 0
                        calculated_cost = -1
                else:
                    calculated_value = item[curr_tahap][k]['value']
                if(calculated_cost <= curr_budget and calculated_cost != -1):
                    if(temp_max < calculated_value):
                        temp_pick = [k]
                        temp_max = calculated_value
                    elif(temp_max == calculated_value):
                        temp_pick.append(k)

            item_pick[curr_tahap][curr_budget] = temp_pick
            optimum[curr_tahap][curr_budget] = temp_max
            # print('{} - {}'.format(temp_max,temp_pick))

    solution = []
    pick_queue = deque()
    tahap_queue = deque()
    budget_queue = deque()
    solution_queue = deque()
    for pick in item_pick[tahap-1][budget]:
        pick_queue.append(pick)
        tahap_queue.append(tahap-1)
        budget_queue.append(budget)
        solution_queue.append([])

    while(len(pick_queue)>0):
        temp_pick = pick_queue.pop()
        temp_tahap = tahap_queue.pop()
        temp_budget = budget_queue.pop()
        temp_solution = solution_queue.pop().copy()

        temp_solution.append(temp_pick+1)
        # print('Tahap {} - Pick {} - Budget {} - Solution {}'.format(temp_tahap,temp_pick,temp_budget,temp_solution))

        if(temp_tahap==0):
            temp_solution.reverse()
            solution.append(temp_solution)
        else:

            new_budget = temp_budget - item[temp_tahap][temp_pick]['cost']

            for pick in item_pick[temp_tahap-1][new_budget]:
                pick_queue.append(pick)
                tahap_queue.append(temp_tahap-1)
                budget_queue.append(new_budget)
                solution_queue.append(temp_solution)

    return solution


if __name__ == '__main__':
    if(len(sys.argv)>1):
        budget = int(sys.argv[1])
    else:
        budget = int(input('Budget (dalam USD)? '))

    item = [
        importer.importData('cpu.csv'),
        importer.importData('gpu.csv'),
        importer.importData('ssd.csv')
    ]

    results = budgeting(item,3,budget)

    if(len(results)>0):
        for result in results:
            for i in range(3):
                print(item[i][result[i]])
    else:
        print('Tidak ada yang cocok dengan budget')