import pickle

headcanon = ["Symphony is a cyborg."]
filename = "headcanon/headcanon.pkl"
with open(filename, "wb") as pkl_file:
    pickle.dump(headcanon, pkl_file)
