from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient("mongodb+srv://prithik:Indian@cluster0.gyp783r.mongodb.net/?retryWrites=true&w=majority&appName=cluster0")
db = client["anokha"]
users = db["users"]

UPLOAD_FOLDER = './'  # Set the upload folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user = users.find_one({"email": username, "password": password})
        
        if user:
            users.update_one({"admin_email": "yukthi@gmail.com"}, {"$set": {"current_user": username}}, upsert=True)
            return jsonify({"response": "success"}), 200  # Respond with success
        return jsonify({"response": "nologin"}), 200
    
    return render_template("login.html")

# SignUp Page
@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    return render_template("signup.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['filcs']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.csv'):
        filename = 'main.csv'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        import pandas as pd
        from sklearn.model_selection import train_test_split, GridSearchCV
        from sklearn.preprocessing import LabelEncoder
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.linear_model import LinearRegression

        # data_hydro = pd.read_csv('hydro.csv')
        # label_encoder_hydro = LabelEncoder()
        # data_hydro['Type'] = label_encoder_hydro.fit_transform(data_hydro['Type'])

        # X_hydro = data_hydro[['Type', 'Year']]
        # y_hydro = data_hydro[['Cost for Installation', 'Cost of Production', 'Cost of Transport', 'Sell Price', 'Efficiency','Cost of Additional Power AC']]

        # X_train_hydro, X_test_hydro, y_train_hydro, y_test_hydro = train_test_split(X_hydro, y_hydro, test_size=0.2, random_state=42)

        # xgb_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)

        # param_grid = {
        #     'n_estimators': [100, 200, 300],
        #     'learning_rate': [0.01, 0.1, 0.2],
        #     'max_depth': [3, 5, 7],
        #     'subsample': [0.6, 0.8, 1.0],
        #     'colsample_bytree': [0.6, 0.8, 1.0]
        # }

        # grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
        # grid_search.fit(X_train_hydro, y_train_hydro)

        # best_model_hydro = grid_search.best_estimator_

        # y_pred_hydro = best_model_hydro.predict(X_test_hydro)
        # r2_hydro = r2_score(y_test_hydro, y_pred_hydro)
        # # print(f'R2 Score Hydro: {r2_hydro * 100:.2f}%')

        data = pd.read_csv('hydro.csv')

        # Encode the 'Type' column
        label_encoder = LabelEncoder()
        data['Type'] = label_encoder.fit_transform(data['Type'])

        # Separate features and targets
        X = data[['Type', 'Year']]
        y = data[['Cost for Installation', 'Cost of Production', 'Cost of Transport', 'Sell Price', 'Efficiency']]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the Random Forest Regressor model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)

        def predict_values_hydro(Type, Year):
            Type_encoded = label_encoder.transform([Type])[0]
            input_data = pd.DataFrame([[Type_encoded, Year]], columns=['Type', 'Year'])
            predictions = model.predict(input_data)
            HYDRO_CAPACITY_KW = 50000
            HYDRO_INSTALL_COST_PER_KW = predictions[0, 0]
            ANNUAL_HYDRO_PRODUCTION = 10000000

            HYDRO_REVENUE_PER_KG = predictions[0,3]
            PRODUCTION_COST_PER_KG = predictions[0, 1]
            TRANSPORT_COST_PER_KG = predictions[0, 2]
            installation_cost = HYDRO_CAPACITY_KW * HYDRO_INSTALL_COST_PER_KW
            
            annual_production_cost = ANNUAL_HYDRO_PRODUCTION * PRODUCTION_COST_PER_KG
            annual_transport_cost_hydro = ANNUAL_HYDRO_PRODUCTION * TRANSPORT_COST_PER_KG
            total_annual_hydro_cost = annual_production_cost + annual_transport_cost_hydro
            
            total_hydro_cost_over_lifespan = total_annual_hydro_cost * CCS_LIFESPAN + installation_cost
            
            total_revenue_hydro_over_lifespan = ANNUAL_HYDRO_PRODUCTION * HYDRO_REVENUE_PER_KG * CCS_LIFESPAN
            
            net_hydro_cost = total_hydro_cost_over_lifespan - total_revenue_hydro_over_lifespan
            
            return net_hydro_cost

        data_carbon = pd.read_csv('carbon.csv')
        label_encoder_carbon = LabelEncoder()
        data_carbon['Type'] = label_encoder_carbon.fit_transform(data_carbon['Type'])

        X_carbon = data_carbon[['Type', 'Year']]
        y_carbon = data_carbon[['Cost for capture', 'Cost of Transport', 'Cost of Storage', 'Effective Sale Price','Cost of Additional Power AC']]

        X_train_carbon, X_test_carbon, y_train_carbon, y_test_carbon = train_test_split(X_carbon, y_carbon, test_size=0.2, random_state=42)

        model_carbon = LinearRegression()
        model_carbon.fit(X_train_carbon, y_train_carbon)

        y_pred_carbon = model_carbon.predict(X_test_carbon)
        mae_carbon = mean_absolute_error(y_test_carbon, y_pred_carbon)
        r2_carbon = r2_score(y_test_carbon, y_pred_carbon)
        # print(f'MAE Carbon: {mae_carbon:.2f}')
        # print(f'R2 Score Carbon: {r2_carbon * 100:.2f}%')

        def predict_values_carbon(Type, Year):
            Type_encoded = label_encoder_carbon.transform([Type])[0]
            input_data = pd.DataFrame([[Type_encoded, Year]], columns=['Type', 'Year'])
            predictions = model_carbon.predict(input_data)
            CAPTURE_COST_PER_TONNE = predictions[0, 0]
            TRANSPORT_COST_PER_TONNE = predictions[0, 1]
            STORAGE_COST_PER_TONNE = predictions[0, 2]
            eff_sale = predictions[0,3]
            annual_capture_cost = ANNUAL_CO2_CAPTURE * CAPTURE_COST_PER_TONNE
            annual_transport_cost = ANNUAL_CO2_CAPTURE * TRANSPORT_COST_PER_TONNE
            annual_storage_cost = ANNUAL_CO2_CAPTURE * STORAGE_COST_PER_TONNE
            total_annual_ccs_cost = annual_capture_cost + annual_transport_cost + annual_storage_cost
            
            total_ccs_cost_over_lifespan = total_annual_ccs_cost * CCS_LIFESPAN

            total_revenue_ccs_over_lifespan = ANNUAL_CO2_CAPTURE * eff_sale * CCS_LIFESPAN
            
            net_ccs_cost = total_ccs_cost_over_lifespan - total_revenue_ccs_over_lifespan
            
            return net_ccs_cost

        file_path = 'main.csv'
        df = pd.read_csv(file_path)

        row = df.iloc[0]
        C_lifespan = row['C_lifespan']
        ANNUAL_CO2_CAPTURE = row['CO2E'] * 1000000

        if row['RRY']:
            CCS_LIFESPAN = C_lifespan - row['RRY']
        elif row['RRL']:
            CCS_LIFESPAN = 2024 + row['RRL'] - C_lifespan
        else:
            CCS_LIFESPAN = C_lifespan - 2024

        if C_lifespan :
            RE_CO2 = row['RE_CO2']
            
            if RE_CO2 > 0:
                if row['RRL']:
                    yr = 2024 + row['RRL']
                else:
                    yr = row['RRY']

                decom_cost_ui = row['PDWell1_D'] * row['PDWell 1']

                hy_cost_ui_alk = predict_values_hydro('Alkaline', yr)
                hy_cost_ui_pem = predict_values_hydro('PEM', yr)
                
                co_cost_ui_off = predict_values_carbon('Onshore', yr)
                co_cost_ui_on = predict_values_carbon('Offshore', yr)
                lo = [decom_cost_ui,hy_cost_ui_alk,hy_cost_ui_pem,co_cost_ui_off,co_cost_ui_on]
                ki = ["Anokha is an advanced application designed to guide asset owners in determining whether depleting oil and gas assets can be repurposed for hydrogen generation, transmission, or carbon capture facilities, utilizing allocated decommissioning funds for optimal financial and environmental outcomes."]
                return render_template('result.html',lo =lo,ki =ki)
                
            if row['PDW1_LS'] > 0 and row['PDW2_LS'] > 0:
                PDWell1_LS = row['PDW1_LS']
                PDWell2_LS = row['PDW2_LS']
                
                lok = min(PDWell1_LS, PDWell2_LS)
                gre = max(PDWell1_LS, PDWell2_LS)
                
                decomp_cost_lok = row['PDWell2_D']
                reinstall_lok = row['PDWell2_I']
                
                hy_cost_lok_alk = predict_values_hydro('Alkaline', lok + 2024)
                hy_cost_lok_pem = predict_values_hydro('PEM', lok + 2024)

                co_cost_lok_off = predict_values_carbon('Onshore', 2024 + lok)
                co_cost_lok_on = predict_values_carbon('Offshore', 2024 + lok)
                
                decom_cost_gre = row['PDWell1_D'] + row['PDWell2_D']
                reinstall_gre = row['PDWell1_I'] + row['PDWell2_I']
                
                hy_cost_gre_alk = predict_values_hydro('Alkaline', 2024 + gre)
                hy_cost_gre_pem = predict_values_hydro('PEM', 2024 + gre)

                co_cost_gre_off = predict_values_carbon('Onshore', 2024 + gre)
                co_cost_gre_on = predict_values_carbon('Offshore', 2024 + gre)
                
                lo = [decomp_cost_lok,reinstall_lok,hy_cost_lok_alk,hy_cost_lok_pem,co_cost_lok_off,co_cost_lok_on]
                ki = ["In this facility, the netcost of H2 generation is negative which means more the profit."]
                return render_template('result.html',lo=lo,ki =ki)
                # print(decom_cost_gre,reinstall_gre,hy_cost_gre_alk,hy_cost_gre_pem,co_cost_gre_off,co_cost_gre_on)

            elif row['PDW1_LS'] > 0 or row['PDW2_LS'] > 0:
                if row['PDW1_LS'] > 0:
                    lok = row['PDW1_LS']
                    decomp_cost_lok = row['PDW1_D']
                    reinstall_lok = row['PDW1_I']

                    hy_cost_lok_alk = predict_values_hydro('Alkaline', lok + 2024)
                    hy_cost_lok_pem = predict_values_hydro('PEM', lok + 2024)

                    co_cost_lok_off = predict_values_carbon('Onshore', 2024 + lok)
                    co_cost_lok_on = predict_values_carbon('Offshore', 2024 + lok)
                    lo =[decomp_cost_lok,reinstall_lok,hy_cost_lok_alk,hy_cost_lok_pem,co_cost_lok_off,co_cost_lok_on]
                    return render_template('result.html',lo = lo)

                elif row['PDW2_LS']:
                    lok = row['PDW2_LS']
                    decomp_cost_lok = row['PDWell2_D']
                    reinstall_lok = row['PDWell2_I']

                    hy_cost_lok_alk = predict_values_hydro('Alkaline', lok + 2024)
                    hy_cost_lok_pem = predict_values_hydro('PEM', lok + 2024)
                    
                    co_cost_lok_off = predict_values_carbon('Onshore', 2024 + lok)
                    co_cost_lok_on = predict_values_carbon('Offshore', 2024 + lok)
                    lo =[decomp_cost_lok,reinstall_lok,hy_cost_lok_alk,hy_cost_lok_pem,co_cost_lok_off,co_cost_lok_on]
                    return render_template('result.html',lo = lo)

                else:
                    print('properly')
            
            else:
                if C_lifespan < 2024:
                    C_lifespan += 2024

                if row['RRL']:
                    yr = 2024 + row['RRL']
                else:
                    yr = row['RRY']
                
                decom_cost_dum = row['PDWell1_D'] * row['PDWell 1']
                
                hy_cost_dum_alk = predict_values_hydro('Alkaline', yr)
                hy_cost_dum_pem = predict_values_hydro('PEM', yr)
                
                co_cost_dum_off = predict_values_carbon('Onshore', yr)
                co_cost_dum_on = predict_values_carbon('Offshore', yr)
                lo =[decom_cost_dum,hy_cost_dum_alk,hy_cost_dum_pem,co_cost_dum_off,co_cost_dum_on]
                ki=["In this facility, the netcost of H2 generation is negative which means more the profit."]
                return render_template('result.html', lo =lo , ki =ki)

        else:
            print('Enter The lifetime correctly')

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json    
    username = data.get('username')
    password = data.get('password')
    phone_number = data.get('phoneNumber')
    email = data.get('email')
    
    if users.find_one({'email': email}):
        return jsonify({"response": "Mail ID already registered"})
    
    user_data = {
        'Name': username, 
        'password': password,  
        "phone_number": phone_number, 
        "email": email
    }
    users.insert_one(user_data)
    
    users.update_one({"admin_email": "yukthi@gmail.com"}, {"$set": {"current_user": username}}, upsert=True)
    
    return jsonify({"response": "signup"})

# Home Page
@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)