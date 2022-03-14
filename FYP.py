#!/usr/bin/env python
# coding: utf-8

#%%
# a star search
tree = {'S':[['L1',1],['M1',1]],
        'L1': [['L2', 1], ['M1', 5], ['M2', 8], ['S',1]],
        'L2': [['L1', 1], ['M2', 3]],
        'M1': [['L1', 5], ['M2', 4],['S',1]],
        'M2': [['L1', 8], ['L2', 3], ['M1', 4]],
        }

# =============================================================================
# tree2 = {'S': [['A', 1], ['B', 2]],
#          'A': [['S', 1]],
#          'B': [['S', 2], ['C', 3], ['D', 4]],
#          'C': [['B', 2], ['E', 5], ['F', 6]],
#          'D': [['B', 4], ['G', 7]],
#          'E': [['C', 5]],
#          'F': [['C', 6]]
#          }
# =============================================================================

heuristic = {'S': 10, 'L1': 8, 'L2': 4, 'M1': 3, 'M2': 5}
# heuristic2 = {'S': 0, 'A': 5000, 'B': 2, 'C': 3, 'D': 4, 'E': 5000, 'F': 5000, 'G': 0}

# cost = {'M1': 0}             # total cost for nodes visited
def getting_start_node(startNode):
    global heuristic
    node = list()
    for destinationNode,value in heuristic.items():
        if startNode == destinationNode:
            node.append(startNode)
            node.append(value)
    return node

def AStarSearch(startNode,goalNode):
    global tree, heuristic
    cost = {}
    # breakpoint()
    cost[startNode] = 0
    closed = []             # closed nodes
    # opened = [['S', 8]]     # opened nodes
    opened  = list()
    opened=[getting_start_node(startNode)]
    '''find the visited nodes'''
    while True:
        fn = [i[1] for i in opened]     # fn = f(n) = g(n) + h(n)
        chosen_index = fn.index(min(fn))
        node = opened[chosen_index][0]  # current node
        closed.append(opened[chosen_index])
        del opened[chosen_index]
        if closed[-1][0] == goalNode:      # break the loop if node G has been found
            break
        for item in tree[node]:
            if item[0] in [closed_item[0] for closed_item in closed]:
                continue
            cost.update({item[0]: cost[node] + item[1]})            # add nodes to cost dictionary
            fn_node = cost[node] + heuristic[item[0]] + item[1]     # calculate f(n) of current node
            temp = [item[0], fn_node]
            opened.append(temp)                                     # store f(n) of current node in array opened

    '''find optimal sequence'''
    trace_node = goalNode                        # correct optimal tracing node, initialize as node G
    optimal_sequence = [goalNode]                # optimal node sequence
    for i in range(len(closed)-2, -1, -1):
        check_node = closed[i][0]           # current node
        if trace_node in [children[0] for children in tree[check_node]]:
            children_costs = [temp[1] for temp in tree[check_node]]
            children_nodes = [temp[0] for temp in tree[check_node]]

            '''check whether h(s) + g(s) = f(s). If so, append current node to optimal sequence
            change the correct optimal tracing node to current node'''
            if cost[check_node] + children_costs[children_nodes.index(trace_node)] == cost[trace_node]:
                optimal_sequence.append(check_node)
                trace_node = check_node
    optimal_sequence.reverse()              # reverse the optimal sequence


    print(optimal_sequence)
    return closed, optimal_sequence


# if __name__ == '__main__':
visited_nodes, optimal_nodes = AStarSearch('L2','S')
# getting_start_node('M1')
print('visited nodes: ' + str(visited_nodes))
print('optimal nodes sequence: ' + str(optimal_nodes))



# In[1]:
# AStarSearch('M1','L2')
schedule={}

while True:
    try:
        noOfJobs=int(input('Please enter the number of jobs: '))
        break
    except Exception as e:
        print(str(e), "Invalid Input")
        
for job in range(noOfJobs):
    jobDetail={}
    for machine in range(2):
        inputJobDetails={}
        jobType:None
        while True:
            try:
                jobType=input("Please enter job type: ").upper()
                if jobType == 'A':
                    jobType = "Milling"
                    break
                elif jobType == 'B':
                    jobType = "Lathe"
                    break
            except:
                print("Invalid Input")

        while True:
            try:
                inputJobDetails['processingTime']=eval(input("Please enter job processing time: "))
                break
            except:
                print("Invalid Input")
        while True:
            try:
                inputJobDetails['cost']=eval(input("Please enter job cost: "))
                break
            except:
                print("Invalid Input")
        inputJobDetails['proc/cost']=inputJobDetails['processingTime']/inputJobDetails['cost']
        inputJobDetails['workdone']=False
        jobDetail[jobType]=inputJobDetails
    jobDetail['totalRatio']=jobDetail['Milling']['proc/cost']+jobDetail['Lathe']['proc/cost']
    jobDetail['totalProcessingTime']=jobDetail['Milling']['processingTime']+jobDetail['Lathe']['processingTime']
    jobDetail['currentWork']=None
    schedule[job]=jobDetail   



# In[2]:

print(schedule)
jobScheduleNumber=0
jobTimeLimit=0
iteration=1
tmpSchedule={}
 
while iteration != noOfJobs:
    tmpSchedule=schedule[iteration]
    jobScheduleNumber=iteration-1;

    while jobScheduleNumber >= 0 and schedule[jobScheduleNumber]['totalRatio'] > tmpSchedule['totalRatio']:
        schedule[jobScheduleNumber+1]=schedule[jobScheduleNumber]
        jobScheduleNumber=jobScheduleNumber-1

    schedule[jobScheduleNumber+1]=tmpSchedule

    iteration=iteration+1


# =============================================================================
# print('filtering jobs that exced the time limit ')
# for job,jobDetail in schedule.items():
#     if jobDetail['totalProcessingTime']< 3601:
#         jobTimeLimit = jobTimeLimit + jobDetail['totalProcessingTime']
#         if jobTimeLimit < 3601:
#             print("\n\n",jobDetail)
# =============================================================================



# In[3]:

import threading,time
timer=0
allWorkCompleted = []
# for jobs in range():
#     allWorkCompleted.append(False)
counter=0
breakloop=False
machines={ 'L1':{'status':False,'processingTime':0},
           'L2':{'status':False,'processingTime':0},
           'M1':{'status':False,'processingTime':0},
           'M2':{'status':False,'processingTime':0},
                     
          }
jobTimeLimit=0
jobScheduleList=list()
index=-1

for job,jobDetail in schedule.items():
    if jobDetail['totalProcessingTime'] < 3601:
        jobTimeLimit = jobTimeLimit + jobDetail['totalProcessingTime']
        if jobTimeLimit < 3601:
            jobScheduleList.append(schedule[job])
            # print("\n\n\n",schedule[job])
for jobs in range(len(jobScheduleList)):
    allWorkCompleted.append(False)
# print(jobScheduleList[1]['Lathe'])
def execute_lathe_1():
    
    global machines,jobScheduleList,index,timer
    localIndex=index
    
    while machines['L1']['status'] == True:
       
        machines['L1']['processingTime']-=0.1
        # print(f"lathe 1 {machines['L1']['processingTime']}")
        if machines['L1']['processingTime'] <= 0:
            machines['L1']['status']=False
           
            jobScheduleList[localIndex]['Lathe']['workdone']=True
            jobScheduleList[localIndex]['currentWork']=None
            # AStarSearch('L1','S')
            # print('executed')
            
def execute_lathe_2():
    global machines,jobScheduleList,index
    localIndex=index
    while machines['L2']['status'] == True:
        machines['L2']['processingTime']-=0.1
        # print(f"lathe 2 {machines['L2']['processingTime']}")
        if machines['L2']['processingTime'] <= 0:
            
            machines['L2']['status']=False
            # print(localIndex)
            jobScheduleList[localIndex]['Lathe']['workdone']=True
            jobScheduleList[localIndex]['currentWork']=None
            # AStarSearch('L2','S')
            # print('executed')

def execute_milling_1():
    global machines,jobScheduleList,index
    localIndex=index
    while machines['M1']['status'] == True:
        
        machines['M1']['processingTime']-=0.1
        # print(f"Milling 1 {machines['M1']['processingTime']}")
        
        if machines['M1']['processingTime'] <= 0:
            machines['M1']['status']=False
            jobScheduleList[localIndex]['Milling']['workdone']=True
            jobScheduleList[localIndex]['currentWork']=None
            # AStarSearch('M1','S')
            # print('executed')
    
            
def execute_milling_2():
    global machines,jobScheduleList,index
    localIndex=index
    while machines['M2']['status'] == True:
        machines['M2']['processingTime']-=0.1
        # print(f"milling 2 {machines['M2']['processingTime']}")
       
        if machines['M2']['processingTime'] <= 0:
            machines['M2']['status']=False 
            print(localIndex)
            jobScheduleList[localIndex]['Milling']['workdone']=True
            jobScheduleList[localIndex]['currentWork']=None
            # AStarSearch('M2','S')
            # print('executed')

execute1=threading.Thread(target=execute_lathe_1)
execute2=threading.Thread(target=execute_lathe_2)
execute3=threading.Thread(target=execute_milling_1)
execute4=threading.Thread(target=execute_milling_2)

# breakpoint()
while True:
    # breakpoint()
    # counter=0
    for job in jobScheduleList:
        for machineName in job:
        
        
            # while machines['L1']['status'] == True and machines['L2']['status'] == True and machines['M1']['status'] == True and machines['M2']['status']==True:
            if 'Lathe' in machineName and job['currentWork'] == None and  job['Lathe']['workdone']==False: 
                if machines['L1']['status'] == False:
                    machines['L1']['status']=True
                    job['Lathe']['workdone']=True
                    index=jobScheduleList.index(job)
                    print(index)
                    # print("\n\n",machines['L1']['status'])
                    machines['L1']['processingTime']=job[machineName]['processingTime']
                    job['currentWork']='Lathe'
                    AStarSearch('S','L1')
                    time.sleep(10)
                    
                elif machines['L2']['status'] == False:
                    machines['L2']['status']=True
                    job['Lathe']['workdone']=True
                    index=jobScheduleList.index(job)
                    print(index)
                    machines['L2']['processingTime']=job[machineName]['processingTime']
                    job['currentWork']='Lathe'
                    AStarSearch('S','L2')
                    time.sleep(10)
                    
            if 'Milling' in machineName and job['currentWork'] == None and job['Milling']['workdone']==False: 
                if machines['M1']['status'] == False:
                    machines['M1']['status']=True
                    job['Milling']['workdone']=True
                    index=jobScheduleList.index(job)
                    print(index)
                    machines['M1']['processingTime']=job[machineName]['processingTime']
                    job['currentWork']='Milling'
                    AStarSearch('S','M1')
                    time.sleep(10)
                    
                elif machines['M2']['status'] == False:
                    machines['M2']['status']=True
                    job['Milling']['workdone']=True
                    index=jobScheduleList.index(job)
                    print(index)
                    machines['M2']['processingTime']=job[machineName]['processingTime']
                    job['currentWork']='Milling'
                    AStarSearch('S','M2')
                    time.sleep(10)
                
                
       
        if job['currentWork'] == 'Lathe':
            
            if execute1.is_alive():
                if machines['L1']['processingTime'] <= 0:
                    pass
                else:
                    if execute2.is_alive():
                        if machines['L2']['processingTime'] <= 0:
                            pass
                        else:
                            execute2=threading.Thread(target=execute_lathe_2)
                            AStarSearch('L2','S')
                            execute2.start()
            elif not execute1.is_alive():
                execute1=threading.Thread(target=execute_lathe_1)
                AStarSearch('L1','S')
                execute1.start()
            
            
        if job['currentWork'] == 'Milling':
            
            if execute3.is_alive():
                if machines['M1']['processingTime'] <= 0:
                    pass
                else:
                    if execute4.is_alive():
                        if machines['M2']['processingTime'] <= 0:
                            pass
                        else:
                            execute4=threading.Thread(target=execute_milling_2)
                            AStarSearch('M2','S')
                            execute4.start()
                        
            elif not execute3.is_alive():
                execute3=threading.Thread(target=execute_milling_1)
                AStarSearch('M1','S')
                execute3.start()
                
        
        
        
        if job['Lathe']['workdone'] == True and job['Milling']['workdone'] == True:
            job['currentWork']='workdone'
            allWorkCompleted[counter]=True
            counter+=1
            
        if False in allWorkCompleted:
            breakloop=False
        else:
            breakloop=True
        # break
        # for workdone in allWorkCompleted:
        #     if workdone is False:
        #         breakloop=False
        #         break
        #     else:
        #         print(allWorkCompleted)
        #         breakloop=True
                
    if breakloop:
        break
#%%
# allWorkCompleted = []
# for jobs in noOfJobs:
#     allWorkCompleted.append(False)
# print(allWorkCompleted)
print(machines)
print("\n\n",jobScheduleList)