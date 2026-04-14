import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression as SkLinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plot

class LinearRegression:
    def __init__(self):
        self.df = None
        self.x = None
        self.y = None
        self.x_test = None
        self.x_train = None
        self.y_test = None
        self.y_train = None
        self.model = None

    #IMPORTANT: Update your file path here!!!!
    def load_data(self):
        #Load data into DF
        file_path = r"C:\Users\nkamr\OneDrive\Desktop\insurance.csv"

        try:
            self.df = pd.read_csv(file_path)
            return self.df
        except FileNotFoundError:
            print("File was not found. Please check the file path and try again.")
            return None
    
    def clean_data(self):
        if self.df is None:
            print("No Data Loaded")
            return None
        
        #Remove missing values, and duplicates
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()

        return self.df
    
    def preprocess_data(self, target_column="charges"):
        if self.df is None:
            print("No Data Loaded")
            return None
        
        #separate features from charges
        self.x = self.df.drop(columns=[target_column])
        self.y = self.df[target_column]

        #Convert columns into numeric data
        self.x = pd.get_dummies(self.x, drop_first=True)

    def split_data(self, test_size=0.2):
        if self.x is None or self.y is None:
            print("Please preprocess the data")
            return None
        
        #Split: 80% train, 20% test
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=test_size, random_state=42, shuffle=True)

    def train_model(self):
        if self.x_train is None or self.y_train is None:
            print("Please process and split data")
            return None

        self.model = SkLinearRegression()
        self.model.fit(self.x_train, self.y_train)

        print("Model trained\n")

    def evaluate_model(self):
        if self.model is None:
            print("Please train the model")
            return None

        if self.x_test is None or self.y_test is None:
            print("Please preprocess and split data")
            return None
        
        #Make test prediction
        pred = self.model.predict(self.x_test)

        #Target: R2 > 0.7, MAE < 5000
        r2 = r2_score(self.y_test, pred)
        mae = mean_absolute_error(self.y_test, pred)

        return r2, mae

    def make_prediction(self, age, bmi, children, sex, smoking_status, region):
        if self.model is None:
            print("Model is not  trained")
            return None
        
        user_data = {
            "age" : age,
            "bmi" : bmi,
            "children" : children,
            "sex" : sex.lower(),
            "smoker" : smoking_status.lower(),
            "region" : region.lower()
        }

        #Create new dataframe with user data
        user_df = pd.DataFrame([user_data])
        user_df = pd.get_dummies(user_df, drop_first=True)

        #Fill in possible empty columns
        for col in self.x.columns:
            if col not in user_df.columns:
                user_df[col] = 0

        user_df = user_df[self.x.columns]

        pred = self.model.predict(user_df)
        return pred[0]
    
    def describe_stats(self):
        print(self.df.describe())
    
    def prediction_range_plot(self, prediction, lower, upper):
        if self.y is None:
            print("Data is not available")
            return None
        
        if lower < 0:
            lower = 0
        
        plot.figure()

        #Show line for: prediction, upperbound, and lower bound compared to the actual data
        plot.hist(self.y, bins=15)
        plot.axvline(prediction, color="green", linestyle='dashed', linewidth=3, label="Prediction")
        plot.axvline(lower, color="red", linestyle="dashed",linewidth=3, label="Lower Bound")
        plot.axvline(upper, color="red", linestyle="dashed",linewidth=3, label="Upper Bound")

        plot.title("Your Prediction vs Real Data")
        plot.xlabel("Charges")
        plot.ylabel("Frequency")

    def bmi_plot(self):
        if self.df is None:
            print("Data not loaded")
            return None
        
        bmi_groups = pd.cut(self.df["bmi"], bins=6)
        average = self.df.groupby(bmi_groups)["charges"].mean()

        plot.figure()
        average.plot(kind="line", marker="X", color="red")
        plot.title("Average Charges By BMI Range")
        plot.xlabel("BMI Range")
        plot.ylabel("Average Charges")

    def smoker_vs_charges_bar_chart(self):
        if self.df is None:
            print("Data not loaded")
            return None
        
        avg_charges = self.df.groupby("smoker")["charges"].mean()

        plot.figure()
        avg_charges.plot(kind="bar")
        plot.title("Average Insurance Charges By Smoking Status")
        plot.xlabel("Smoking status")
        plot.ylabel("Average Charges")