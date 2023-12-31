import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from ToyTorch.data import Dataset


class StockDataset(Dataset):
    def __init__(
        self,
        stock_file: str = "dataset.csv",
        past_history: int = 60,
        forward_look: int = 1,
        transform=None,
        target_transform=None,
    ):
        super().__init__()
        self.stock_file = stock_file
        self.past_history = past_history
        self.forward_look = forward_look

        self.stock_data = pd.read_csv(stock_file)
        self.stock_data = self.stock_data[["Close"]]
        self.stock_data = self.stock_data.tail(1000)

        scaler = MinMaxScaler(feature_range=(-1, 1))
        self.transformed_data = scaler.fit_transform(self.stock_data.values.reshape(-1, 1))
        self.transformed_data = np.squeeze(np.array(self.transformed_data))
        self.range = (scaler.data_max_, scaler.data_min_)

    def __len__(self):
        return len(self.transformed_data) - 2*self.past_history

    def __getitem__(self, idx):
        idx = idx+self.past_history
        arr = []
        for i in range(self.past_history):
            x = i-self.past_history
            arr.append(self.transformed_data[idx+x:idx+self.past_history+x])
        narr = np.array(arr)

        return (narr, self.transformed_data[idx+self.past_history])

if __name__ == "__main__":
    dataset = StockDataset()
    print(dataset[0])
    print(dataset[len(dataset)-1])
    print(len(dataset))

