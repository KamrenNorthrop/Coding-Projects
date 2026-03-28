from linear_regression import LinearRegression

def main():
    print("Welcome - Please wait a moment while we load, clean, process the data and train the model")
    model = LinearRegression()

    #Load data
    model.load_data()

    #Clean data
    model.clean_data()

    #Process data for encoding
    model.preprocess_data()

    #Split Data
    model.split_data()

    #Train the model
    model.train_model()

    #Evaluate
    r2, mae = model.evaluate_model()
    print(f"R2 is {r2:.3f}")
    print(f"MAE is {mae:.2f}")

    

if __name__ == "__main__":
    main()