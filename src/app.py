import gradio as gr
import pandas as pd
import joblib

# Load your churn prediction model
model = joblib.load('Model\\best_model.pkl')

# Create a Gradio interface
def predict_churn(SeniorCitizen, Partner, Dependents, tenure, InternetService,
                  OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
                  StreamingTV, StreamingMovies, Contract, PaperlessBilling,
                  PaymentMethod, MonthlyCharges, TotalCharges):
    
    # Create a dictionary with input features
    input_data = {
        'SeniorCitizen': SeniorCitizen,
        'Partner': Partner,
        'Dependents': Dependents,
        'tenure': tenure,
        'InternetService': InternetService,
        'OnlineSecurity': OnlineSecurity,
        'OnlineBackup': OnlineBackup,
        'DeviceProtection': DeviceProtection,
        'TechSupport': TechSupport,
        'StreamingTV': StreamingTV,
        'StreamingMovies': StreamingMovies,
        'Contract': Contract,
        'PaperlessBilling': PaperlessBilling,
        'PaymentMethod': PaymentMethod,
        'MonthlyCharges': MonthlyCharges,
        'TotalCharges': TotalCharges
    }
    
    # Create a DataFrame from the input data
    input_df = pd.DataFrame([input_data])
    
    # Make predictions
    prediction = model.predict(input_df)
    
    
    # Determine the churn prediction
    if prediction[0] == 0:
        churn_result = '<span style="color: limegreen;font-size:20px;">Customer will not churn</span>'
    else:
        churn_result = '<span style="color: red;font-size:20px;">Customer will churn</span>'
    
    return churn_result

# Define Gradio components
with gr.Blocks(theme=gr.themes.Base(primary_hue="stone",neutral_hue="stone")) as block:
    gr.Markdown(
        """# 👋 Welcome to Team Cape Cod's Churn Prediction App

                This App predicts whether a customer will churn or not""")
    
    with gr.Row():
        with gr.Column():
            SeniorCitizen = gr.Radio(["Yes", "No"], label="Are you a Senior Citizen?")
            Partner = gr.Radio(["Yes", "No"], label="Do you have a partner?")
            Dependents = gr.Radio(["Yes", "No"], label="Do you have dependents?")
            tenure = gr.Number(label="Tenure (months): How long have you been at the company")
            InternetService = gr.Radio(["DSL", "Fiber optic", "No"], label="What Internet Service Do You Use?")
            OnlineSecurity = gr.Radio(["Yes", "No", "No internet service"], label="Do You Have Online Security?")
            
        with gr.Column():
            OnlineBackup = gr.Radio(["Yes", "No", "No internet service"], label="Do You Have Any Online Backup Service?")
            DeviceProtection = gr.Radio(["Yes", "No", "No internet service"], label="Do You Use Any Device Protection?")
            TechSupport = gr.Radio(["Yes", "No", "No internet service"], label="Do You Use TechSupport?")
            StreamingTV = gr.Radio(["Yes", "No", "No internet service"], label="Do You Stream TV?")
            StreamingMovies = gr.Radio(["Yes", "No", "No internet service"], label="Do You Stream Movies?")
            
        with gr.Column():
            Contract = gr.Radio(["Month-to-month", "One year", "Two year"], label="What Is Your Contract Type?")
            PaperlessBilling = gr.Radio(["Yes", "No"], label="Do You Use Paperless Billing?")
            PaymentMethod = gr.Dropdown(["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], label="What Payment Method Do You Use?")
            MonthlyCharges = gr.Number(label="What is your Monthly Charge?")
            TotalCharges = gr.Number(label="What are your Total Charges?")
            

            #create a variable that clear button will clear
            input_components = [SeniorCitizen, Partner, Dependents, tenure,
                                InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
                                TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling,
                                PaymentMethod, MonthlyCharges, TotalCharges]
            
             #Create a button user will click to clear inputs selected
            gr.ClearButton(input_components)           
    
    #create markdown for ouput
    text = gr.Markdown("## Churn Status")
    
    # Define Gradio outputs
    output = gr.HTML("Awaiting Prediction")

    # Create a button
    button = gr.Button("Predict")

    # Create Gradio interface
    button.click(fn=predict_churn,inputs=input_components, outputs=output)
    
    #create an example dataframe
    gr.Markdown("## Input Examples")

    gr.Examples([['No', 'No', 'No', '12', 'Fiber optic', 'No', 'No', 'No', 'No', 'Yes', 'No', 'Month-to-month', 'Yes', 'Electronic check', '84.45', '1059.55'],
                 
                      ['No', 'No', 'No', '9', 'No', 'No internet service', 'No internet service', 'No internet service', 'No internet service', 'No internet service', 'No internet service', 'Month-to-month', 'No', 'Mailed check', '20.40', '181.80'],
                      
                      ['No', 'No', 'No', '27', 'DSL', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'One year', 'No', 'Electronic check', '81.70', '2212.55']],
                      
                      inputs=input_components)

#start gradio app
block.launch(
    auth=("azubiafrica", "teamcapecod"),
    auth_message="Enter the username 'azubiafrica' and password 'teamcapecod' for this demo app"
)

