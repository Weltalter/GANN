import pandas as pd
import numpy as np


class DS(object):
    def __init__(self):
        pd.set_option('mode.chained_assignment', None)
        pd.set_option('display.max_columns', None)
        pd.set_option("styler.render.max_elements", 1048576)

        self.__input_train_data = None
        self.__output_train_data = None
        self.__input_test_data = None
        self.__output_test_data = None

        self.__style_dataset = None
        self.__output_column = None

        self.__dataset = None
        self.__dataset_save = None

    def read_dataset(self, dataset):
        tmp = pd.read_csv(dataset)
        tmp.convert_dtypes()
        self.__dataset = tmp.copy(deep=True)
        self.__dataset_save = tmp.copy(deep=True)

    @property
    def output_column(self):
        return self.__output_column

    @output_column.setter
    def output_column(self, output_column):
        if output_column is not None:
            if output_column >= 0:
                self.__output_column = output_column

    @property
    def dataset(self):
        def color_output_data(val):
            return f'background-color: rgb(100, 10, 100, 0.5)'

        if self.__output_column is None:
            return self.__dataset.head(25)
        else:
            return self.__dataset.head(25).style.map(color_output_data,
                                                     subset=[self.__dataset.columns[self.__output_column]])

    @property
    def dataset_save(self):
        return self.__dataset_save

    @property
    def output_train_data(self):
        return self.__output_train_data

    @property
    def input_train_data(self):
        return self.__input_train_data

    @property
    def output_test_data(self):
        return self.__output_test_data

    @property
    def input_test_data(self):
        return self.__input_test_data

    def set_data(self):
        if self.__output_column is not None:
            if self.__output_column >= 0:
                from sklearn.model_selection import train_test_split
                x = self.__dataset.drop(self.__dataset.columns[self.__output_column], axis=1)
                y = self.__dataset[self.__dataset.columns[self.__output_column]]
                x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                                    test_size=0.3,
                                                                    random_state=57)

                self.__output_train_data = np.array(y_train.tolist())
                self.__output_test_data = np.array(y_test.tolist())
                self.__input_train_data = np.array(list(list(row) for row
                                                        in zip(*[x_train[column].tolist()
                                                                 for column
                                                                 in x_train.columns])))
                self.__input_test_data = np.array(list(list(row) for row
                                                       in zip(*[x_test[column].tolist()
                                                                for column
                                                                in x_test.columns])))

    def get_column(self, column):
        return self.__dataset[column]

    def delete_column(self, redact_column):
        self.__dataset.drop(columns=redact_column, inplace=True)

    def ordinal_encoder_column(self, redact_column):
        from sklearn.preprocessing import OrdinalEncoder
        enc = OrdinalEncoder()
        self.__dataset[redact_column] = enc.fit_transform(self.__dataset[[redact_column]])

    def one_hot_encoder_column(self, redact_column):
        from sklearn.preprocessing import OneHotEncoder
        enc = OneHotEncoder()
        res = enc.fit_transform(self.__dataset[[redact_column]])

        categories = []
        for c in enc.categories_[0]:
            categories.append('<' + redact_column + '> ' + str(c))

        self.__dataset[categories] = res.toarray()
        del self.__dataset[redact_column]

    def normalized_dataset(self, param):
        from sklearn.preprocessing import MinMaxScaler  # StandardScaler
        scaler_mm = MinMaxScaler()
        self.__dataset[list(self.__dataset.columns)] = scaler_mm.fit_transform(
            self.__dataset[list(self.__dataset.columns)])

    def recover_dataset(self):
        self.__dataset = self.__dataset_save.copy(deep=True)

    def delete_void_dataset(self, column):
        self.__dataset.dropna(subset=[column], inplace=True)

    def mean_void_dataset(self, column):
        self.__dataset[column] = self.__dataset[column].fillna(self.__dataset[column].mean())

    def delete_anomalies_dataset(self, column, min_value, max_value):
        self.__dataset.drop(list(self.__dataset[self.__dataset[column] > max_value].index), axis=0, inplace=True)
        self.__dataset.drop(list(self.__dataset[self.__dataset[column] < min_value].index), axis=0, inplace=True)

    @property
    def input_columns(self):
        return list(self.__dataset.columns)

    @property
    def count_input_row(self):
        return len(self.__dataset)

    def get_count_unique_output_row(self):
        return len(self.__dataset[self.__dataset.columns[self.__output_column]].unique())
