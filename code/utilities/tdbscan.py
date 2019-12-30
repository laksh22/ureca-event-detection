import math
"""
T-DBSCAN
Author: Jaya
Source: Paper titled "T-DBSCAN: A Spatiotemporal Density Clustering for GPS Trajectory Segmentation"
"""
"""
INPUTS:
    df={o1,o2,...,on} Set of objects
    CEps = Outer radius for density calculation
    Eps = Inner radius defining the density calculation are
    MinPts = Minimun number of points in neighborhood
OUTPUT:
    df = Updated dataframe with annotated clusters
"""

def T_DBSCAN(df, CEps,Eps, MinPts):
    
    C = 0 #ID of cluster currently being searched
    Cp = {} #Points in cluster with ID same as C
    UNMARKED = 777777
    
    
    df['cluster'] = UNMARKED
    df['visited'] = 'Not visited'
    MaxId = -1 #Maximum ID of the visited point
        
    for index, P in df.iterrows(): #Go through each data point  
        if(index == 100):
            print("C IS:", C)
            break    
        if index > MaxId: #Only look at data after current observation           
            
            df.loc[index, "visited"] = "visited" #Mark current datapoint as visited          
            #Search for continuous density-based neighbours N
            N = getNeighbors(P, CEps, Eps, df, index)
            MaxId = index #Set new max ID as current          
            #Make new cluster if number of neighbours > MinPts
            if len(N) > MinPts: 
                C = C + 1                
            #Expand the cluster
            Ctemp, MaxId = expandCluster(P, N, CEps, Eps, MinPts, MaxId, df, index)            
            if C in Cp:
                Cp[C] = Cp[C] + Ctemp                             
            else:
                Cp[C] = Ctemp
                
    print("Clusters identified...")         
    Cp = mergeClusters(Cp) #merge clusters      
    df = updateClusters(df, Cp)  #update df     
       
    return df


# Retrieve neighbors
def getNeighbors(P, CEps, Eps, df, p_index):
    
    neighborhood = []
    center_point = P

    curr_frame = df.iloc[p_index]["frame"]
    
    for index, point in df.iterrows():
        if df.iloc[index]["frame"] == curr_frame:
            distance = get_distance(center_point['x'], center_point['y'], point['x'], point['y'])
            if distance < Eps:
                print("FOUND NEIGHBOUR")
                neighborhood.append(index)
            elif distance > CEps:
                 break
             
    return neighborhood
        
 
    
#cluster expanding
def expandCluster(P, N, CEps, Eps, MinPts, MaxId, df, p_index):
    
    Cp = []
    N2 = []
    
    Cp.append(p_index)
    
    for index in N:
        point = df.loc[index]
        df.loc[index]['visited'] = "visited"
        if index > MaxId:
            MaxId = index     
        N2 = getNeighbors(point, CEps, Eps, df, index) #find neighbors of neighbors of core point P   
        if len(N2) >= MinPts: #classify the points into current cluster based on definitions 3,4,5            
            N = N + N2
        if index not in Cp:
            Cp.append(index)
            
    return Cp, MaxId
            
#merge clusters
def mergeClusters(Cp):
     
     Buffer = {}     
     
     print("Merging...")
     for idx, val in Cp.items():         
         
         if not Buffer: #if buffer is empty add first item by default
             Buffer[idx] = val
             
         else: #compare last item in the buffer with Cp             
             if max(Buffer[list(Buffer.keys())[-1]]) <= min(Cp[idx]): #new cluster = new Buffer entry
                 Buffer[(list(Buffer.keys())[-1])+1] = Cp[idx]
             else: #merge last item in the buffer with Cp
                 Buffer[list(Buffer.keys())[-1]] += Cp[idx]
                             
     return Buffer
                 
             
#update dataframe             
def updateClusters(df, Cp):
    
    for idx, val in Cp.items():
        for index in val:
            df.loc[index, "cluster"] = idx
            
    return df
     
def get_distance(x1, x2, y1, y2):
    distance = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
    print(distance)
    return distance