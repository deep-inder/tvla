import numpy as np
import os 
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean

#-------------------------------------------------------------------------------

def files_by_parameter(path = None, message = None, cipher = None, key = None):
    if(message == None and cipher == None and key == None):
        print("have to provide atleast one parameter")
        return -1
    if(path == None):
        print("path is not given")
        return -1 

    parameters = []
    
    files = os.listdir(path)
    filtered_files = []
    ids = []

    for f in files:
        temp = f.split("_")
        
        pick = True
        if(message != None):
            if(temp[-2][2:] == message):
                pick = pick and True
            else:
                pick = pick and False
        
        if(cipher != None):
            if(temp[-1][2:-4] == cipher):
                pick = pick and True
            else:
                pick = pick and False
        
        if(key != None):
            if(temp[-3][2:] == key):
                pick = pick and True
            else:
                pick = pick and False

        if (pick == True):
            filtered_files.append(f)
            ids.append(int(temp[4][2:]))

    return filtered_files, ids
#-------------------------------------------------------------------------------

def get_traces(path, files):
    traces = {}

    count = 0
    for f in files:

        if(f[:4]!="wave"):
            continue
        tfile = open(path + f)
        trace = []
        
        for line in tfile:
            if(line[0]!="#"):
                raw_data = int(line)
                # raw_data = raw_data* 0.0000141351 
                raw_data = raw_data* 0.00141351 
                trace.append(raw_data)

        temp_file_name = f.split("_")
        id = int(temp_file_name[4][2:])

        if(len(trace) == 3253):
            traces[id] = trace

        if(count%1000 == 0):
            print("loaded "+ str(count)+ "traces")
        count = count + 1

    return traces
#-------------------------------------------------------------------------------

def split_dict(d, ratio):
    l = len(d)
    n = int(l*ratio)

    d1 = dict( list(d.items())[:n] )
    d2 = dict( list(d.items())[n:] ) 

    return d1, d2

#-------------------------------------------------------------------------------

def preprocess(d1, d2):
    trace1 = []
    trace2 = []

    _, x = next(iter(d1.items()))
    n1 = len(x)

    _, x = next(iter(d2.items()))
    n2 = len(x)

    for time_t1 in range(n1):
        temp1 = []
        for _, t1 in d1.items():
            temp1.append(t1[time_t1])
        trace1.append(temp1)

    for time_t2 in range(n2):
        temp2 = []
        for _, t2 in d2.items():
            temp2.append(t2[time_t2])
        trace2.append(temp2)

    # print(trace1[0][0])
    trace1 = np.power(trace1, 3)
    # print(trace1[0][0])
    trace2 = np.power(trace2, 3)

    return np.array(trace1), np.array(trace2)

#-------------------------------------------------------------------------------

def TVLA(trace1, trace2):

    n1 = trace1.shape[1]
    n2 = trace2.shape[1]
    
    mean_trace1 = np.mean(trace1, axis = 1)
    mean_trace2 = np.mean(trace2, axis = 1)

    var_trace1 = np.var(trace1, axis = 1)
    var_trace2 = np.var(trace2, axis = 1)

    t_test = (mean_trace1 - mean_trace2) / np.sqrt((var_trace1/n1) + (var_trace2/n2))

    return t_test
#-------------------------------------------------------------------------------

def MF_TVLA(trace1, trace2):

    n1 = trace1.shape[1]
    n2 = trace2.shape[1]
    # -----------------
    mean_trace1 = np.mean(trace1, axis = 1)
    mean_trace2 = np.mean(trace2, axis = 1)

    # trace1.shape==(3253,10000) & mean_trace1==(3253,) 

    for i in range(len(mean_trace1)):

        for j in range(n1):
            trace1[i][j] = trace1[i][j] - mean_trace1[i]
        for j in range(n2):
            trace2[i][j] = trace2[i][j] - mean_trace2[i]   

    #------------------ 

    mean_trace1 = np.mean(trace1, axis = 1)
    mean_trace2 = np.mean(trace2, axis = 1)

    var_trace1 = np.var(trace1, axis = 1)
    var_trace2 = np.var(trace2, axis = 1)

    t_test = (mean_trace1 - mean_trace2) / np.sqrt((var_trace1/n1) + (var_trace2/n2))

    return t_test

#-------------------------------------------------------------------------------

def run(path1, path2, name):
    files1 = os.listdir(path1)
    files2 = os.listdir(path2)

    t1 = get_traces(path1,files1)
    t2 = get_traces(path2,files2)
    
    t1, t2 = preprocess(t1, t2)
    my_tvla = TVLA(t1, t2) 


    plt.plot(my_tvla)
    plt.axhline(y =  4.5, color='r', linestyle='-')
    plt.axhline(y = -4.5, color='r', linestyle='-')
    plt.ylabel(name)
    plt.savefig("results/"+name+".png") 
    # print("saved " + name + ".png")


# if __name__ == "__main__":
    
#     path1 = "./p1/"
#     path2 = "./p2/"
    
#     run(path1, path2, "abc")

#-------------------------------------------------------------------------------

