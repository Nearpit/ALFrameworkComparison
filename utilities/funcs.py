import json 
import torch
from torcheval import metrics

from argparse import ArgumentParser
from utilities import constants as cnst

def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-d", "--dataset", help="What dataset to train on", required=True, choices=["dna", "toy"])
    parser.add_argument("-tm", "--tuned_model", help="What model to tune", default="MLP", choices=["MLP", "AE"])
    parser.add_argument("-a", "--algorithm", help="What active learning algorithm to evaluate", choices=["random", 
                                                                                                         "cheating",
                                                                                                         "bald", 
                                                                                                         "coreset",
                                                                                                         "entropy"])
    return parser.parse_args()

def get_configs(dataset_name):
    with open(f"configs/{dataset_name}.json", "r") as openfile:
        configs = json.load(openfile)
    return configs

def train(model, train_loader, val_loader, criterion, optimizer, metric, DEVICE):
        total_loss_train = 0
        total_loss_val = 0
        model = model.to(DEVICE)

        train_metric =  getattr(metrics, metric)(device=DEVICE)
        val_metric =  getattr(metrics, metric)(device=DEVICE)

        for train_input, train_label in train_loader:

            train_label = train_label.to(DEVICE)
            train_input = train_input.to(DEVICE)

            output = model(train_input.float())
            output = output.to(DEVICE)
            
            batch_loss = criterion(output, train_label)
            total_loss_train += batch_loss.item()

            train_metric.update(input=output.squeeze(), target=train_label.squeeze())
            model.zero_grad()
            batch_loss.backward()
            optimizer.step()
        
        total_acc_train = train_metric.compute()

        

        with torch.no_grad():

            for val_input, val_label in val_loader:

                val_label = val_label.to(DEVICE)
                val_input = val_input.to(DEVICE)

                output = model(val_input)
                output = output.to(DEVICE)


                batch_loss = criterion(output, val_label)
                total_loss_val += batch_loss.item()
                val_metric.update(input=output.squeeze(), target=val_label.squeeze())
                
        
        total_acc_val = val_metric.compute()
        # print(f"Train: Loss - {total_loss_train:.3f}, Acc - {total_acc_train:.3%} Val: Loss - {total_loss_val:.3f}, Acc - {total_acc_val:.3%}")
        return total_loss_val, total_acc_val, model

