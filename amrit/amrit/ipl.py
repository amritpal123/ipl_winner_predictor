import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as mlt; mlt.rcdefaults()
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import joblib


def training():

    matches=pd.read_csv('C:/Users/Amritpal Singh/PycharmProjects/amrit/amrit/amrit/matches.csv')
    matches['winner'].fillna('Draw', inplace=True)
    
    matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                     'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                     'Sunrisers Hyderabad','Rising Pune Supergiant','Kochi Tuskers Kerala','Pune Warriors','Delhi Capitals']
                    ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','DD'],inplace=True)
    
    
    matches['city'].fillna('Dubai',inplace=True)
    
    
    
    matches1 = matches[['team1', 'team2', 'toss_winner', 'venue', 'winner', 'toss_decision']]
    df = pd.DataFrame(matches1)

    
    var_mod = ["team1","team2", "toss_winner", "venue","toss_decision","winner"]
    le = LabelEncoder()
    for i in var_mod:
        temp = le.fit_transform(df[i])
        l = le.classes_
        filename="C:/Users/Amritpal Singh/PycharmProjects/amrit/amrit/amrit/"+i+"01.sav"
        joblib.dump(le,filename)
        df[i]=temp 
        
        
    X=df.iloc[:,[0,1,2,3,5]]

    y=df.iloc[:,[4]]

    model = RandomForestClassifier(n_estimators = 100)

    model.fit(X, y)
    
    joblib.dump(model,'C:/Users/Amritpal Singh/PycharmProjects/amrit/amrit/amrit/iplmodel.sav')
    predictions = model.predict(X)
    print(predictions)
    accuracy = metrics.accuracy_score(predictions, y)
    print('Accuracy : %s' % '{0:.3%}'.format(accuracy))


training()

def predict_winner(test):

    temp={}
    
    
    var_mod = ['team101.sav', 'team201.sav', 'toss_winner01.sav', 'venue01.sav', 'toss_decision01.sav']

    for p in range(len(var_mod)):

        var_mod[p]="C:/Users/Amritpal Singh/PycharmProjects/amrit/amrit/amrit/"+var_mod[p]

    t=['team1', 'team2', 'toss_winner', 'venue', 'toss_decision']
    for i,k in zip(var_mod,t):
        
        le=joblib.load(i)
        
        temp[i] = int(le.transform([test[k]]))

    
    model=joblib.load('C:/Users/Amritpal Singh/PycharmProjects/amrit/amrit/amrit/iplmodel.sav')
    
    
    
    X_pred=list(temp.values())
    
    out = model.predict([X_pred])
    
    
    win=joblib.load('C:/Users/Amritpal Singh/PycharmProjects/amrit/amrit/amrit/winner01.sav')


    out = win.inverse_transform([out])

    out=out[0]

    return out








#
#test={'team1':'MI','team2':'SRH','venue':'Holkar Cricket Stadium','toss_winner':'SRH','toss_decision','0'}