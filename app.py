from flask import Flask,render_template,request #import the libraries
import pickle
from flask_mail import Mail,Message


app=Flask(__name__)	#initialize the flask app
app.config["MAIL_SERVER"]="smtp.gmail.com"	#gmail
app.config["MAIL_PORT"]=587	#port no	
app.config["MAIL_USERNAME"]="tester.insurepro@gmail.com"
app.config["MAIL_PASSWORD"]="Tester@4567!!!" #passwd
app.config["MAIL_USE_TLS"]=True #transport layer security
app.config["MAIL_USE_SSL"]=False #secure sockets layer

mail=Mail(app) #instantiate the Mail class
#home page
@app.route("/")
def home():
	return render_template("index.html")
#after pressing predict option
@app.route("/get",methods=["POST"])
def get():
	smk=request.form.get("smk") #smoking or not?
	print(smk)
	fname=request.form["fname"] #accept the fname
	if not(fname.isalpha()) or len(fname)<2:	#validation for fname
	    return render_template("home.html",msg="First name should contain alphabets only")
	lname=request.form["lname"] #likewise for lname
	if not(lname.isalpha()) or len(lname)<2:
	    return render_template("home.html",msg="Last name should contain alphabets only")
	name=fname+" "+lname #concat into full name
	sex=request.form.get("sex") #accept sex
	hf=int(request.form["hf"])  #height in ft
	hi=int(request.form["hi"])  #height in inches
	wt=float(request.form["wt"]) #weight in kg -- > all for the bmi
	height=0.3048*hf+0.0254*hi #convert ft inches to metres
	bmi=round((wt/height**2),0)  #round the value of bmi to 0 places
	pk=""
	if bmi<=26:
		pk="you are at low risk" 
	else:
	   pk="you are at high risk"
	em=request.form["em"]  #accepting the email from user
	age=float(request.form["age"]) #age
	smk= int(request.form.get("smk")) #smoking or not?
	with open("ic.model","rb") as f: #using the saved model
		model=pickle.load(f)
	data=[[bmi,age,smk]] 
	res=model.predict(data);	ans=round(res[0],0) #prediction
	msg=Message("Report for the medical insurance",sender="tester.insurepro@gmail.com",recipients=[em]) #the body of mail to be sent
	msg.body="Hey "+str(name).title()+"\n"+"Thanks for using InsurePro. Your medical insurance cost for this month is Rs."+str(ans)+" Your BMI is "+str(bmi)+" which means "+str(pk)
	mail.send(msg) #send the mail
	return render_template("index.html",msg="Thanks for using this! You will receive a mail shortly.") #show it on the webpage

if __name__=="__main__":  #run the app
	app.run(debug=True,use_reloader=True)  #it can be debugged as well as reloaded whenever needed
