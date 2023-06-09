import numpy as np
import torch as th
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from model import NetArticle
import Image_DataSet as dtst
import cv2


hyper_params = {
    'indoor_size': 20,
    'outdoor_size': 20,
    'input_size': (3, 128, 128),
    'num_epochs': 10,
    'learning_rate': 0.001
}


def get_batch(batch):
    features = batch[:, 0, :, :, :]
    target_transpose = batch[:, 1, :, :, :]
    target_reflection = batch[:, 2, :, :, :]
    #target = th.Tensor(np.concatenate((target_transpose, target_reflection), axis=1))
    return features, target_transpose, target_reflection
def get_result(x):
    return sum(x)/len(x)+0.02

def test(test_loader, model, criterion):
    losses = []
    model.eval()
    step = 0
    t=0
    for i, batch in enumerate(test_loader):
        features, target_transmission, target_reflection = get_batch(batch)
        #cv2.imwrite("imgs1/reflection" + str(t) + ".png",np.array( target_reflection))
        predict_transmission, predict_reflection = model(features),model(features)
        #cv2.imwrite("imgs1/reflection" + str(t) + ".png",np.array( predict_reflection))
        if i < 1:
            print("-------------------------------")
            a = (np.transpose(predict_transmission[0].detach().numpy(), (1, 2, 0)) * 255).astype(int)
            b = (np.transpose(target_transmission[0].detach().numpy(), (1, 2, 0)) * 255).astype(int)
            print(a - b)
            print(predict_transmission[0] - target_transmission[0])

            
            writer = open("hello.txt", 'w')
            for i in range(20, 30):
                for j in range(20, 30):
                    print(a[i][j][0], file=writer)
            
            print("----------------2---------------")
            
            
        #cv2.imwrite("imgs/target_trans" + str(t) + ".png", (np.transpose(target_transmission[0].detach().numpy(), (1, 2, 0)) * 255).astype(int))
        #cv2.imwrite("imgs/transmission" + str(t) + ".png", (np.transpose(predict_transmission[0].detach().numpy(), (1, 2, 0)) * 255).astype(int))
        #cv2.imwrite("imgs/reflection" + str(t) + ".png", (np.transpose(predict_reflection[0].detach().numpy(), (1, 2, 0)) * 255).astype(int))
        t+=1
        loss1 = criterion(predict_transmission, target_transmission)
        #cv2.imwrite("imgs/reflection" + str(t) + ".png", target_reflection)
        loss2 = criterion(predict_reflection, target_reflection)
        loss = loss1 + loss2
        losses.append(loss.item())
        print(loss1.item())
        step += 1
    return losses


if __name__ == "__main__":
    print(th.__version__)

    data = dtst.ImageDataSet(hyper_params['indoor_size'], hyper_params['outdoor_size'])
    test_loader = dtst.DataLoader(data, 1, 18, test=True)

    #net = NetArticle()
    net = th.load("weights3.hdf5")
    criterion = nn.MSELoss()
    losses = test(test_loader, net, criterion)
    print( losses)
    print(  f'PSNR: {get_result(losses)*100}%')

