# lets create a util function here
# accepts raw input of 4041 length list

# def predict

# loads our model and our trained weights.
# predict 
# output of predict is a tensor of size 3 x 1 
# output the index wih the highest value
import torch

def predict(inputs_list):
    # inputs_list should be list of 4041 length

    model = torch.load('nn_weights')

    torch.tensor(inputs_list)
    pred = model(X)
    return torch.argmax(pred)