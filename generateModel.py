import pandas as pd
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

data = pd.read_csv("data.csv")

allData = pd.read_csv('data.csv').set_index("ID")
X = allData.drop('eloChange', axis=1)
y = allData['eloChange']

clf = Sequential()

clf.add(Dense(units = 6, input_dim = 3))
clf.add(Dense(units = 4))
clf.add(Dense(units = 4))
clf.add(Dense(units = 3))
clf.add(Dense(units = 2))
clf.add(Dense(units = 2))
clf.add(Dense(units = 1))

clf.compile(optimizer = "Adam", loss = "mse")
clf.fit(X, y, epochs = 50)

ans = input("Save model? (Y/N): ")
if(ans == "Y" or ans == "y"):
    clf.save("tfModel")
    print("Model saved!")
elif(ans == "N" or ans == "n"):
    print("Model not saved!")
else:
    print("Invalid input. Model not saved!")


# RUN FOLLOWING COMMAND IN BASH AFTER DE-COMMENTING
# tensorflowjs_converter \
#     --input_format=tf_saved_model \
#     ./tfModel \
#     ./tfjsModel/