from linear_regression import LinearRegression

def main():
    print("Welcome - Please wait a moment while we load, clean, process the data and train the model")
    model = LinearRegression()

    #Load data
    model.load_data()

    #Clean data
    model.clean_data()

    #Process data
    model.preprocess_data()

    #Split Data
    model.split_data()

    #Train the model
    model.train_model()

    #Evaluate
    r2, mae = model.evaluate_model()
    print(f"R2 : {r2:.3f}")
    print(f"MAE : {mae:.2f}")

    #Get user data to make a prediction
    making_prediction = True
    while making_prediction:
        while True:
            try:
                age = int(input("What is your age? "))
                if age <= 0:
                    print("Please enter a valid age")
                    continue
                break
            except ValueError:
                print("Please enter a valid numeric age")

        while True:
            try:
                bmi = float(input("What is your BMI? "))
                if bmi <= 0:
                    print("Please enter a valid BMI")
                    continue
                break
            except ValueError:
                print("Please enter a valid numeric BMI")

        while True:
            try:
                children = int(input("How many children do you have? "))
                if children < 0:
                    print("Please enter 0 or a positive integer")
                    continue
                break
            except ValueError:
                print("Please enter a valid numeric integer for children")

        while True:
            sex = input("Are you male or female? (male/female) ").lower()
            valid_input_for_sex = ["male", "female"]
            if sex not in valid_input_for_sex:
                print("Please enter either male or female")
                continue
            break

        while True:
            smoking_status = input("Do you smoke? (yes/no) ").lower()
            valid_input_for_smoking = ["yes", "no"]
            if smoking_status not in valid_input_for_smoking:
                print("Please enter either yes or no.")
                continue
            break

        while True:
            region = input("What region are you from? (NW, NE, SW, SE) ").lower()
            valid_input_for_region = ["nw", "ne", "sw", "se"]
            if region not in valid_input_for_region:
                print("Please enter a valid region: nw, ne, sw, se.")
                continue
            break

        outcome = model.make_prediction(age, bmi, children, sex, smoking_status, region)
        if outcome is None:
            print("No prediction made, try again")
            continue

        #Calcuate upper and lower range considering the MAE
        lower_range = outcome - mae
        if lower_range < 0:
            lower_range = 0
        upper_range = outcome + mae

        #Print prediction and the range
        print(f"Your predicted annual cost: ${outcome:.2f}\n")
        print(f"Your predicted annual cost range considering the MAE:\nLower bound: ${lower_range:.2f} \nUpper bound: ${upper_range:.2f}")
        model.describe_stats()
        model.prediction_range_plot(outcome, lower_range, upper_range)
        model.bmi_plot()
        model.smoker_vs_charges_bar_chart()

        #Does the user want to make another prediction?
        accepted = ["yes", "y"]
        again = input("\nWould you like to make another prediction? (yes/no) ").lower()
        if again.lower() in accepted:
            continue
        else:
            break

if __name__ == "__main__":
    main()