from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

#Read data
df_Homicide_Race = pd.read_csv('Homicide_Race_data.csv', sep=',')
df_Homicide_Age = pd.read_csv('Homicide_Age_data.csv', sep=',')
#Data frame
df_Homicide_Race = pd.DataFrame(df_Homicide_Race)
df_Homicide_Age = pd.DataFrame(df_Homicide_Age)
#Column Homicide Race
names_Homicide_Race = df_Homicide_Race.iloc[:, 0] #Pierwsza kolumna
data_Homicide_Race = df_Homicide_Race.iloc[:, 1] #Druga kolumna
#Column Homicide Age
names_Homicide_Age = df_Homicide_Age.iloc[:, 0]
data_Homicide_Age = df_Homicide_Age.iloc[:, 1]

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('indexlogged.html')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return '<body style="background: #23242a;"><h1 style="margin: auto; padding: auto; justify-content: center; align-items: center; color: #45f3ff; background: #23242a; text-align: center; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); margin: 0; padding: 20px;">Nazwa użytkownika już istnieje. Wybierz inną nazwę użytkownika!<br><a href="/" style="display: block; border: none; outline: none; background: #45f3ff; padding: 11px 25px; width: 100%; margin-top: 10px; border-radius: 4px; font-weight: 600; cursor: pointer; text-decoration: none; color: #23242a;">Powrót do strony głównej</a></h1></body>'

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/')

    return render_template('register.html')

@app.route('/wykres1', methods=['GET', 'POST'])
def wykres1():
    if 'username' in session:
        img = io.BytesIO()
        df_Line_Chart = pd.read_csv('DataLineChart.csv', sep=';')

        df_Line_Chart = pd.DataFrame(df_Line_Chart)
        Years = df_Line_Chart['series'].values
        Years_Data = df_Line_Chart['United states'].values.astype(float)
        fig0, ax0 = plt.subplots(figsize=(15, 9), dpi=100)
        ax0.plot(Years, Years_Data, marker = 'o', linestyle = '-')
        ax0.set_xlabel('Years')
        ax0.set_ylabel('Rate per 100,000 people per year')
        ax0.set_title('Rate of homicide offenses by population for years 2011-2021')
        fig0.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('result.html').format(plot_url)
    return render_template('index.html')

@app.route('/wykres2', methods=['GET', 'POST'])
def wykres2():
    if 'username' in session:
        img = io.BytesIO()
        df_Race_Data = pd.read_csv('PopulationAge2022.csv', sep=';')
        df_Race_Data = pd.DataFrame(df_Race_Data)
        df_Race_Data = df_Race_Data.dropna(axis=0)
        age = df_Race_Data['Age'].values.astype(str)
        age_percent = df_Race_Data['percent'].values.astype(float)
        fig01, ax01 = plt.subplots(figsize=(15, 9), dpi=100)
        ax01.bar(age, age_percent)
        ax01.set_xlabel('Age')
        ax01.set_ylabel('Percent')
        ax01.set_title('Population by age in 2022 (population - 333,287,557)')
        fig01.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('result.html').format(plot_url)

    return render_template('index.html')

@app.route('/wykres3', methods=['GET', 'POST'])
def wykres3():
    if 'username' in session:
        img = io.BytesIO()
        df_Race_Data = pd.read_csv('PopulationRace2022.csv', sep=';')
        df_Race_Data = pd.DataFrame(df_Race_Data)
        df_Race_Data = df_Race_Data.dropna(axis=0)
        Race = df_Race_Data['Race'].values.astype(str)
        Race_percent = df_Race_Data['percent'].values.astype(float)
        fig02, ax02 = plt.subplots(figsize=(15, 9), dpi=100)
        ax02.bar(Race, Race_percent)
        ax02.set_xlabel('Race')
        ax02.set_ylabel('Percent')
        ax02.set_title('Population by race in 2022 (population - 333,287,557)')
        ax02.set_xticklabels(Race, rotation=10)
        
        fig1, ax1 = plt.subplots(figsize=(15, 9), dpi=100)
        ax1.bar(names_Homicide_Race, data_Homicide_Race)
        ax1.set_xlabel('Race')
        ax1.set_ylabel('Number of offenders')
        ax1.set_title('Homicide Race')

        fig2, ax2 = plt.subplots(figsize=(15, 9), dpi=100)
        ax2.bar(names_Homicide_Age, data_Homicide_Age)
        ax2.set_xlabel('Age')
        ax2.set_ylabel('Number of offenders')
        ax2.set_title('Homicide Age')
        fig02.savefig('Static/1.png')
        fig1.savefig('Static/2.png')
        fig2.savefig('Static/3.png')
        return render_template('result2.html')

    return render_template('index.html')

@app.route('/wykres4', methods=['GET', 'POST'])
def wykres4():
    if 'username' in session:
        img = io.BytesIO()
        df_Rape_Race = pd.read_csv('Offender_Race_05-28-2023_Rape.csv', sep=',')
        df_Rape_Race = pd.DataFrame(df_Rape_Race)
        names_Rape_Race = df_Rape_Race.iloc[:, 0] #Pierwsza kolumna
        data_Rape_Race = df_Rape_Race.iloc[:, 1] #Druga kolumna

        fig3, ax3 = plt.subplots(figsize=(15, 9), dpi=100)
        ax3.bar(names_Rape_Race, data_Rape_Race)
        ax3.set_xlabel('Race')
        ax3.set_ylabel('Number of offenders')
        ax3.set_title('Rape Race')
        fig3.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('result.html').format(plot_url)

    return render_template('index.html')

@app.route('/wykres5', methods=['GET', 'POST'])
def wykres5():
    if 'username' in session:
        img = io.BytesIO()
        df_Rape_Age_Data = pd.read_csv('Offender_Age_05-28-2023_Rape.csv', sep=',')
        df_Rape_Age = pd.DataFrame(df_Rape_Age_Data)
        names_Rape_Age = df_Rape_Age.iloc[:, 0]
        data_Rape_Age = df_Rape_Age.iloc[:, 1]

        fig4, ax4 = plt.subplots(figsize=(15, 9), dpi=100)
        ax4.bar(names_Rape_Age, data_Rape_Age)
        ax4.set_xlabel('Age')
        ax4.set_ylabel('Number of offenders')
        ax4.set_title('Rape Age')

        fig4.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('result.html').format(plot_url)

    return render_template('index.html')
    
@app.route('/wykres6', methods=['GET', 'POST'])
def wykres6():
    if 'username' in session:
        img = io.BytesIO()
        df_Robbery_Race_Data = pd.read_csv('Offender_Race_05-28-2023_Robbery.csv', sep=',')
        df_Robbery_Race = pd.DataFrame(df_Robbery_Race_Data)
        names_Robbery_Race = df_Robbery_Race.iloc[:, 0]
        data_Robbery_Race = df_Robbery_Race.iloc[:, 1]

        fig5, ax5 = plt.subplots(figsize=(15, 9), dpi=100)
        ax5.bar(names_Robbery_Race, data_Robbery_Race)
        ax5.set_xlabel('Race')
        ax5.set_ylabel('Number of offenders')
        ax5.set_title('Robbery Race')
        fig5.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('result.html').format(plot_url)

    return render_template('index.html')

@app.route('/wykres7', methods=['GET', 'POST'])
def wykres7():
    if 'username' in session:
        img = io.BytesIO()
        df_Robbery_Age_Data = pd.read_csv('Offender-Age_05-28-2023_Robbery.csv', sep=',')
        df_Robbery_Age = pd.DataFrame(df_Robbery_Age_Data)
        names_Robbery_Age = df_Robbery_Age.iloc[:, 0]
        data_Robbery_Age = df_Robbery_Age.iloc[:, 1]

        fig6, ax6 = plt.subplots(figsize=(15, 9), dpi=100)
        ax6.bar(names_Robbery_Age, data_Robbery_Age)
        ax6.set_xlabel('Age')
        ax6.set_ylabel('Number of offenders')
        ax6.set_title('Robbery Age')

        fig6.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('result.html').format(plot_url)

    return render_template('index.html')

@app.route('/wykres8', methods=['GET', 'POST'])
def wykres8():
    if 'username' in session:
        img = io.BytesIO()
        df_Assault_Age_Data = pd.read_csv('Offender-Age_05-28-2023_Aggravated_Assault.csv', sep=',')
        df_Assault_Age = pd.DataFrame(df_Assault_Age_Data)
        names_Assault_Age = df_Assault_Age.iloc[:, 0]
        data_Assault_Age = df_Assault_Age.iloc[:, 1]
        fig7, ax7 = plt.subplots(figsize=(15, 9), dpi=100)
        ax7.bar(names_Assault_Age, data_Assault_Age)
        ax7.set_xlabel('Age')
        ax7.set_ylabel('Number of offenders')
        ax7.set_title('Aggravated assault Age')
        fig7.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('result.html').format(plot_url)

    return render_template('index.html')

@app.route('/wykres9', methods=['GET', 'POST'])
def wykres9():
    if 'username' in session:
        img = io.BytesIO()
        df_Assault_Race_Data = pd.read_csv('Offender-Race_05-28-2023_Aggravated_Assault.csv', sep=',')
        df_Assault_Race = pd.DataFrame(df_Assault_Race_Data)
        names_Assault_Race = df_Assault_Race.iloc[:, 0]
        data_Assault_Race = df_Assault_Race.iloc[:, 1]
        fig8, ax8 = plt.subplots(figsize=(15, 9), dpi=100)
        ax8.bar(names_Assault_Race, data_Assault_Race)
        ax8.set_xlabel('Race')
        ax8.set_ylabel('Number of offenders')
        ax8.set_title('Aggravated assault Race')
        fig8.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('result.html').format(plot_url)

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = user.username
            return redirect('/')
        return '<body style="background: #23242a;"><h1 style="margin: auto; padding: auto; justify-content: center; align-items: center; color: #45f3ff; background: #23242a; text-align: center; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); margin: 0; padding: 20px;" class="error">Nieprawidłowa nazwa użytkownika lub hasło!<br><a href="/" style="display: block; border: none; outline: none; background: #45f3ff; padding: 11px 25px; width: 100%; margin-top: 10px; border-radius: 4px; font-weight: 600; cursor: pointer; text-decoration: none; color: #23242a;">Powrót do strony głównej</a></h1></body>'

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run()
