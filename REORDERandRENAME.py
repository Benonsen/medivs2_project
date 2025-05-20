import os
import sys
import csv
from dataclasses import field

import pandas as pd

class outputfile:
    def __init__(self, filename, es, x, y, ef, esv, edv, split):
        self.filename = filename
        self.es = es
        self.x = x
        self.y = y
        self.ef = ef
        self.edv = edv
        self.esv = esv
        self.split = split

    def to_dict(self):
        return {
            "FileName": self.filename,
            "ES": self.es,
            "x": self.x,
            "y": self.y,
            "EF": self.ef,
            "EDV": self.edv,
            "ESV": self.esv,
            "Split": self.split
        }


if __name__ == '__main__':
    inputcsvPath = "./csvs/transformed.csv"
    df_fileList = pd.read_csv(inputcsvPath)

    #valid
    valid_path = "C:/Users/leonh/Downloads/echonet/archive/Echonet-Frames-Masks-Dataset/valid/frames"
    files_valid = os.listdir(valid_path)
    files_valid = [item.removesuffix(".png") for item in files_valid]
    results_valid = df_fileList.loc[df_fileList["FileName"].isin(files_valid)].copy()
    results_valid.FileName = results_valid.FileName.map(lambda x: "/valid/frames/"+x)
    results_valid.Split= "VAL"
    print(results_valid.index.size)

    #train
    train_path = "C:/Users/leonh/Downloads/echonet/archive/Echonet-Frames-Masks-Dataset/train/frames"
    files_train = os.listdir(train_path)
    files_train = [item.removesuffix(".png") for item in files_train]
    results_train = df_fileList.loc[df_fileList["FileName"].isin(files_train)].copy()
    results_train.FileName = results_train.FileName.map(lambda x: "/train/frames/"+x)
    results_train.Split= "TRAIN"
    print(results_train.index.size)

    #test
    test_path = "C:/Users/leonh/Downloads/echonet/archive/Echonet-Frames-Masks-Dataset/test/frames"
    files_test = os.listdir(test_path)
    files_test = [item.removesuffix(".png") for item in files_test]
    results_test = df_fileList.loc[df_fileList["FileName"].isin(files_test)].copy()
    results_test.FileName = results_test.FileName.map(lambda x: "/test/frames/"+x)
    results_test.Split= "TEST"
    print(results_test.index.size)


    results = pd.concat([results_valid, results_train, results_test])

    results.to_csv("./csvs/results.csv", index=False)
