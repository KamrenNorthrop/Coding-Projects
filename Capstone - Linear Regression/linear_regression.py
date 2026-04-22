'''
D964 - Capstone
Name: Kamren Northrop
Student ID: 011338614 
'''
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
        #Check if loaded
        if self.df is None:
            print("No Data Loaded")
            return None
        
        #Remove missing values, and duplicates
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()

        return self.df
    
    def preprocess_data(self, target_column="charges"):
        #Check if loaded
        if self.df is None:
            print("No Data Loaded")
            return None
        
        #separate charges from other variables
        self.x = self.df.drop(columns=[target_column])
        self.y = self.df[target_column]

        #Converting categories into numerical indecators (One-hot)
        self.x = pd.get_dummies(self.x, drop_first=True)

    def split_data(self, test_size=0.2):
        #Check if data is loaded and preprocessed
        if self.x is None or self.y is None:
            print("Please preprocess the data")
            return None
        
        #Split: 80% train, 20% test
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=test_size, random_state=42, shuffle=True)

    def train_model(self):
        #Check if data loaded, preprocessed, and split
        if self.x_train is None or self.y_train is None:
            print("Please process and split data")
            return None

        #Initialize the model
        #Use model.fit() with training data
        self.model = SkLinearRegression()
        self.model.fit(self.x_train, self.y_train)

        print("Model trained\n")

    def evaluate_model(self):
        #Check to see if a model is initiated and trained
        if self.model is None:
            print("Please train the model")
            return None

        #Checking to see if data is preprocessed
        if self.x_test is None or self.y_test is None:
            print("Please preprocess and split data")
            return None
        
        #Make test prediction
        pred = self.model.predict(self.x_test)

        #Get evaluation metrics, Target: R2 >= 0.7, MAE <= 5000
        r2 = r2_score(self.y_test, pred)
        mae = mean_absolute_error(self.y_test, pred)

        return r2, mae

    def make_prediction(self, age, bmi, children, sex, smoking_status, region):
        #Check to see if a model is initiated and trained
        if self.model is None:
            print("Model is not  trained")
            return None
        
        #Store user input, normalize sex, smoker, region
        user_data = {
            "age" : age,
            "bmi" : bmi,
            "children" : children,
            "sex" : sex.lower(),
            "smoker" : smoking_status.lower(),
            "region" : region.lower()
        }

        #Create new dataframe with user data
        #Encode user dataframe
        user_df = pd.DataFrame([user_data])
        user_df = pd.get_dummies(user_df, drop_first=True)

        #Fill in possible empty columns
        for col in self.x.columns:
            if col not in user_df.columns:
                user_df[col] = 0

        #Make sure columns are in order
        user_df = user_df[self.x.columns]

        #Make the prediction with the user dataframe
        #Return prediction
        pred = self.model.predict(user_df)
        return pred[0]
    
    def describe_stats(self):
        #Show data statistics
        print(self.df.describe())
    
    #Visualization #1
    #Show prediction and MAE range
    def prediction_range_plot(self, prediction, lower, upper):
        #Check to make sure there are charges to show
        if self.y is None:
            print("Data is not available")
            return None
        
        #Correcting lower range that might dip below 0
        if lower < 0:
            lower = 0
        
        #Create new chart
        plot.figure()

        #Show line for: prediction, upperbound, and lower bound compared to the actual data
        plot.hist(self.y, bins=15)
        plot.axvline(prediction, color="green", linestyle='dashed', linewidth=3, label="Prediction")
        plot.axvline(lower, color="red", linestyle="dashed",linewidth=3, label="Lower Bound")
        plot.axvline(upper, color="red", linestyle="dashed",linewidth=3, label="Upper Bound")

        #Title, x = charges, y = frequency count
        plot.title("Your Prediction vs Real Data")
        plot.xlabel("Charges")
        plot.ylabel("Frequency")

    #Visualization #2
    #How does BMI change charges?
    def bmi_plot(self):
        #Is there a data frame?
        if self.df is None:
            print("Data not loaded")
            return None
        
        #Create BMI groups using 6 bins
        #Calculate the average charges for each BMI range to get an idea of how cost changes 
        bmi_groups = pd.cut(self.df["bmi"], bins=6)
        average = self.df.groupby(bmi_groups, observed=False)["charges"].mean()

        #Create new chart
        plot.figure()

        #Plot average charges using a line chart
        #Add Title, x = BMI ranges, y = average charges per bin
        average.plot(kind="line", marker="X", color="red")
        plot.title("Average Charges By BMI Range")
        plot.xlabel("BMI Range")
        plot.ylabel("Average Charges")

    #Visulization #3
    #How does smoking change charges?
    def smoker_vs_charges_bar_chart(self):
        #Does dataframe exist?
        if self.df is None:
            print("Data not loaded")
            return None
        
        #Group by smoking status and calculate average charges by group
        avg_charges = self.df.groupby("smoker")["charges"].mean()

        #Create new chart
        plot.figure()
        
        #Plot using bar chart to clearly show difference between average charges between non-smokers and active smokers
        #Add title, x = smoking status, y = average charges by group
        avg_charges.plot(kind="bar")
        plot.title("Average Insurance Charges By Smoking Status")
        plot.xlabel("Smoking status")
        plot.ylabel("Average Charges")