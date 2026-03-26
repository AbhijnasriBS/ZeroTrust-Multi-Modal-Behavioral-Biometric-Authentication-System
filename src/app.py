from sklearn.metrics import roc_curve
from common.database import Database
from models.Client import Client
import csv
import os
from flask import Flask, render_template, request, session, make_response
import pandas as pd
from sklearn.svm import OneClassSVM
import numpy as np
np.set_printoptions(suppress=True)

app = Flask(__name__,
            template_folder='../templates',
            static_url_path='',
            static_folder='../static')
app.secret_key = "secret"
Database.initialize()
tempvalue = ''
tempvalue_reg = ''


@app.route('/')
def main_template():
    # return make_response(dep_show())
    return render_template('index.html')


@app.route('/userregis')
def client_regis_template(message=None):
    return render_template('clientRegis.html', message=message if message is not None else None)


@app.route('/home')
def redirect_home(message=None):
    return render_template('index.html', message=message if message is not None else None)


@app.route('/home_temp')
def redirect_home_temp(message=None):

    r1 = open('C:/Users/Dell/Desktop/CSVs/user.csv')  # Here your csv file
    r = csv.reader(r1)
    lines = list(r)
    lines[0][0] = tempvalue
    writer1 = open('C:/Users/Dell/Desktop/CSVs/user.csv', 'w', newline='')
    writer = csv.writer(writer1)
    writer.writerows(lines)
    writer1.close()
    r1.close()
    r1 = open("C:/Users/Dell/Desktop/CSVs/user.csv")
    fout = open(
        "C:/Users/Dell/Desktop/Software Implem/credit/Trial_fromt end/src/keystroke.trial.csv", "a")
    for line in r1:
        fout.write(line)
    fout.close()

    def evaluateEER(user_scores, imposter_scores):
        labels = [0] * len(user_scores) + [1] * len(imposter_scores)
        fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
        missrates = 1 - tpr
        farates = fpr
        dists = missrates - farates
        idx1 = np.argmin(dists[dists >= 0])
        idx2 = np.argmax(dists[dists < 0])
        x = [missrates[idx1], farates[idx1]]
        y = [missrates[idx2], farates[idx2]]
        a = (x[0] - x[1]) / (y[1] - x[1] - y[0] + x[0])
        eer = x[0] + a * (y[0] - x[0])
        return eer

    class SVMDetector:
        # just the training() function changes, rest all remains same.

        def __init__(self, subjects):
            self.u_scores = []
            self.i_scores = []
            self.mean_vector = []
            self.subjects = subjects

        def training(self):
            self.clf = OneClassSVM(kernel='rbf', gamma=26)
            self.clf.fit(self.train)

        def testing(self):
            self.u_scores = -self.clf.decision_function(self.test_genuine)
            self.i_scores = -self.clf.decision_function(self.test_imposter)
            self.u_scores = list(self.u_scores)
            self.i_scores = list(self.i_scores)

        def evaluate(self):
            eers = []

            for subject in subjects:
                genuine_user_data = data.loc[data.subject ==
                                             tempvalue, "H.period":"UD.l.Return"]

                imposter_data = data.loc[data.subject != tempvalue, :]

                self.train = genuine_user_data[-1:]
                self.test_genuine = genuine_user_data[:20]
                self.test_imposter = imposter_data.groupby("subject"). \
                    head(20).loc[:, "H.period":"UD.l.Return"]

                self.training()
                self.testing()
                eers.append(evaluateEER(self.u_scores,
                                        self.i_scores))
                break
            return np.mean(eers)

    path = "C:/Users/Dell/Desktop/Software Implem/credit/Trial_fromt end/src/keystroke.trial.csv"
    data = pd.read_csv(path)
    subjects = data["subject"].unique()
    print(subjects)
    print(SVMDetector(subjects).evaluate())
    if(SVMDetector(subjects).evaluate() < 0.4 and SVMDetector(subjects).evaluate() > 0.15):
        return render_template('clienthome.html', message=message if message is not None else None)
    else:
        return render_template('index.html', message=message if message is not None else None)


@app.route('/reg_captcha', methods=['GET'])
def redirect_reg_captcha(message=None):

    r1 = open('C:/Users/Dell/Desktop/CSV_reg/user.csv')  # Here your csv file
    r = csv.reader(r1)
    lines = list(r)
    for i in range(20):
        lines[i][0] = tempvalue_reg
    writer1 = open('C:/Users/Dell/Desktop/CSV_reg/user.csv', 'w')
    writer = csv.writer(writer1)
    writer.writerows(lines)
    writer1.close()
    r1.close()
    r1 = open("C:/Users/Dell/Desktop/CSV_reg/user.csv")
    fout = open(
        "C:/Users/Dell/Desktop/Software Implem/credit/Trial_fromt end/src/keystroke.trial.csv", "a")
    for line in r1:
        fout.write(line)
    fout.close()

    return render_template('index.html', message=message if message is not None else None)


@app.route('/about', methods=['GET'])
def redirect_about(message=None):
    return render_template('about.html', message=message if message is not None else None)


@app.route('/post', methods=['GET'])
def redirect_post(message=None):
    return render_template('post.html', message=message if message is not None else None)


@app.route('/contact', methods=['GET'])
def redirect_contact(message=None):
    return render_template('contact.html', message=message if message is not None else None)


@app.route('/client_home', methods=['GET'])
def redirect_client_home(message=None):
    return render_template('clienthome.html', message=message if message is not None else None)


@app.route('/client_transactions', methods=['GET'])
def redirect_client_transaction(message=None):
    return render_template('clienttransactions.html', message=message if message is not None else None)


@app.route('/client_fund_transfer', methods=['GET', 'POST'])
def redirect_client_fundtransfer(message=None):
    if request.method == 'GET':
        return render_template('client_fundtransfer.html', message=message if message is not None else None)
    else:
        self_acc = request.form['self_Client_acc']
        recieving_acc = request.form['Recieving_Client_acc']
        recieving_phone = request.form['Recieving_Client_phone']
        Amount = request.form['Recieving_Client_Amount']
        Desc = request.form['Recieving_Cient_Description']
        Client.transfer_fund(self_acc, recieving_acc,
                             recieving_phone, int(Amount), Desc)
        return render_template("client_fundtransfer.html")


@app.route('/client_account_summary', methods=['GET'])
def redirect_client_account_summary(message=None):
    client = Client.from_email(session['email'])
    print(client)
    return render_template('client_accountsummary.html', message=message if message is not None else None, client=client)


@app.route('/client_log_files', methods=['GET'])
def redirect_client_logfiles(message=None):
    return render_template('client_logfile.html', message=message if message is not None else None)


@app.route('/adminlogin')
def admin_login_template(message=None):
    return render_template('adminlogin.html', message=message if message is not None else None)


@app.route('/userlogin')
def user_login_template(message=None):
    return render_template('userlogin.html', message=message if message is not None else None)


@app.route('/clientlogin', methods=['POST'])
def login_client():
    name = request.form['Client_name']
    password = request.form['Client_pass']
    client = Client.from_name(name)
    global tempvalue
    tempvalue = name
    # print(User.login_vaild(email,password))
    if client is not None:
        if client.password == password:
            session['email'] = client.email
            return render_template('login_captcha.html', target="blank")

    else:
        session['email'] = None
    return render_template('home.html', target="blank")


@app.route('/admin_login', methods=['POST'])
def login_admin():
    name = request.form['admin_name']
    password = request.form['admin_pass']
    if name == "Saksham":
        if password == "Saini":
            return render_template('home-admin.html')
    else:
        session['email'] = None
    return render_template('index.html')


@app.route('/Client_add', methods=['POST', 'GET'])
def emp_add():
    if request.method == 'GET' and session['email'] != None:
        return render_template('clientRegis.html')
    else:
        # _id, password, name, contact_number, gender, email, date_of_birth, date_of_joining = None, money = None, desc = None
        name = request.form['Client_name']
        global tempvalue_reg
        tempvalue_reg = name
        password = request.form['Client_pass']
        Gender = request.form['Client_gender']
        Contact_number = request.form['Client_pno']
        _id = request.form['Client_ID']
        Date_of_Birth = request.form['Client_DoB']
        email = request.form['Client_mail']
        client = Client(_id, password, name, Contact_number,
                        Gender, email, Date_of_Birth)
        client.save_to_mongo()
        # message = "Successful"
        return render_template('reg_captcha.html', message="Successfull")


@app.route('/view_clients')
def admin_view_clients_templateas(message=None):
    clients = Client.all_clients()
    return render_template('viewclients.html', message=message if message is not None else None, clients=clients)


@app.route('/manage_clients')
def admin_manage_clients_template(message=None):
    return render_template('manageclientdetails.html', message=message if message is not None else None)


@app.route('/delete_clients')
def admin_delete_clients_template(message=None):
    return render_template('delete-client.html', message=message if message is not None else None)


@app.route('/admin_log_files')
def admin_log_files_template(message=None):
    return render_template('adminlogfile.html', message=message if message is not None else None)


@app.route('/admin_home')
def admin_home_template(message=None):
    return render_template('home-admin.html', message=message if message is not None else None)


@app.route('/view_indi_clients')
def view_clients_templateas(message=None):
    client = Client.from_email(session['email'])
    return render_template('client_accountsummary.html', message=message if message is not None else None, client=client)


@app.route('/enter_delete_client', methods=['POST'])
def delete_client():
    name = request.form['Client_name']
    account = request.form['Client_account']
    pno = request.form['Client_pno']

    client = Client.from_id(name)
    client.delete_client(name)
    # print(User.login_vaild(email,password))
    if client is not None:
        if client.account_number == account:

            client.delete_client(name)
            session['email'] = client.email
            return render_template('delete-client.html')
    else:
        session['email'] = None

    return render_template('delete-client.html', message="Failed")


if __name__ == '__main__':
    app.run(port=4990)
