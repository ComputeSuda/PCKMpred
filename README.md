# Intro  
PCKMpred (PTM Cross-Talk/Mutation predictor) is a computational method that can accurately identify PTM cross-talk/mutation pairs in a given protein sequence or structure. we propose an algorithm to improve the prediction of PTM sites and PTM sites(PTM cross-talk) and to study the interaction between PTM sites and mutation
sites(PTM mutation). In addition to the basic network features of protein three-dimensional structure
and sequence features, the dynamic features based on ENMs (elastic network model) are also used to
improve the prediction ability of the algorithm. Through feature selection, we reserved 48 features and
developed a predictor for predicting PTM cross-talk and mutation. According to the evaluation based
on PTM cross-talk, the area under the curve of our best prediction model reaches 0.911, which exceeds
the state-of-art-model PCTpred. Based on the evaluation of PTM mutation, our prediction model is
highly reliable with an AUC score 0.935. Even with the removal of the distance, the performance of
our model is relatively stable.
![PCKMpred_framework](https://github.com/ComputeSuda/PCKMpred/blob/main/IMG/workflow.png)

# System requirement  
PCKMpred is develpoed under Linux environment with:  
* Ubuntu 18.04, CUDA: 10.1, Cudnn: 7.6.5    
* Python (3.7.0): keras==2.4.3, scikit-learn==0.24.2, numpy==1.19.5, tensorflow==2.4.1, biopython==1.78 and prody==2.0 modules    
* R (4.0.3): bio3d==2.4-1, igraph==1.2.6, and stringr==1.4.0 modules 

# Dataset and feature 
We provide the datasets, and pre-processed features here for those interested in reproducing our paper.  
The datasets, Cross-talk data and Mutation data, are stored in ./Dataprocess/Dataset/Cross-talk/Cross-talk.xlsx and ./Dataprocess/Dataset/Mutation/mutation.xlsx, which all include positive set and control(negative) dataset.   
In addition, we also store the pre-processed feature files in ./DataSet\_all\_cross-talk and ./Dataset\_all\_mutation. 
# Train with our data
If you want to use one model to experiment, first use generate\_set.py in folders ./DataSet\_all\_cross-talk and ./DataSet\_all\_mutation to generate samples for training and testing, and then execute main\_dl.py or main\_ml.py for training and testing. The results of each test exist in ./Result , if you want to get the total results of this experiment, execute ./get\_result.py, and the total results are stored in ./Final\_result.  
Note: attention the file path.

# Contact
Please feel free to contact us if you need any help: 20204227054@stu.suda.edu.cn
