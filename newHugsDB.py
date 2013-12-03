import pickle

hugs = {"hubbeking":[0,0]}
filename = "hugs/hugs.pkl"
with open(filename, "wb") as pkl_file:
    pickle.dump(hugs, pkl_file)