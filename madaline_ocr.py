import argparse

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

from network import dataloader, neuron


class Network:

    def __init__(self, plot_results: bool = False):
        self.neurons = []
        self.plot_results = plot_results

    def train(self, training_set: dict):
        data = training_set[0]
        for label, x in data.items():
            self.neurons.append(neuron.SingleNeuron(x, label))

    def predict(self, test_set):
        test_data = test_set[0]
        noise_levels = test_set[1]
        result  =  {}
        for label, x in test_data.items():
            best_neuron = None
            confidence = 0
            for idx, neuron in enumerate(self.neurons):
                current_value = self.neurons[idx].forward(x)
                if current_value > confidence:
                    confidence = current_value
                    best_neuron = self.neurons[idx]
            result[label] = [best_neuron.labels, confidence[0][0], noise_levels[label]]
            print(f'Letter: {label} -> {best_neuron.labels}, fidelity: {round(confidence[0][0],3)}, noise level: {noise_levels[label]}%')
        total_accuracy = sum([True for y, y_pred in result.items() if y == y_pred[0]])/len(result)
        print(f'Total accuracy: {round(total_accuracy,3)}') 
        if self.plot_results:
            self.plot_cm(result,  total_accuracy, noise_levels= noise_levels.values())   


    def plot_cm(self, result_dict: dict, total_accuracy: float, noise_levels: float):

        sns.set(rc={'figure.figsize':(20,20)})
        sns.set(font_scale=2)
        y_true = [x for x in result_dict.keys()]
        y_pred = [x[0] for x in result_dict.values()]
        fidelities = [x[1] for x in result_dict.values()]
        cm = confusion_matrix(y_true, y_pred)
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=False, ax=ax, cmap='Blues', cbar=False, fmt='g')
        ax.set_xticklabels([x[-1] for x in result_dict.keys()])
        ax.set_yticklabels([x[-1] for x in result_dict.keys()])
        ax.set_title(f'Confusion Matrix, total accuracy: {total_accuracy:.2%}', fontsize=30)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('True')
        plt.savefig('confusion_matrix.png')



if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--train_path', help='Path to training data', required=True)
    argparser.add_argument('--test_path', help='Path to test data', required=True)
    argparser.add_argument('--plot_results', action='store_true', help='Plot confusion matrix', required=False, default=False)
    args = argparser.parse_args()
    dataset = dataloader.DataLoader(args.train_path)
    net = Network(args.plot_results)
    net.train(dataset.load_data())
    test_set = dataloader.DataLoader(args.test_path)
    net.predict(test_set.load_data())
