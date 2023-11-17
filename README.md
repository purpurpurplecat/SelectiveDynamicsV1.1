# SelectimicsV1.1
1.For input File: 
(1)Input file must be a .vasp file .
(2)Input str must be 'Cartesian'.

2.Before you use this code, you should know an approximate distance between two layers which need to be divided:
(1)For example, in order to figure out how many C layers are in slab-dia-model,we can get an approximate distance between two C via Vesta.

![image](https://github.com/purpurpurplecat/SelectiveDynamicsV1.1/assets/91890059/0f1a7992-20aa-44ed-9799-a30c4cbfa7a5)

We could get Dis from Vesta:
Dis = |Height1 -Height2|

In terms of Input_Dis, it's recommeded that :
Dis < Input_Dis < 2Dis

3.Special situation:
(1)If you want to fix all atoms input 1 in min_fix_layers and max in max_fix_layers.
(2)If you want to move all atoms input 0 in min_fix_layers and 0 in max_fix_layers.
