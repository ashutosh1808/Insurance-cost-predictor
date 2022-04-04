from flask import Flask,render_template,request #import the libraries
import pickle
from flask_mail import Mail,Message


app=Flask(__name__)	#initialize the flask app
app.config["MAIL_SERVER"]="smtp.gmail.com"	#gmail
app.config["MAIL_PORT"]=587	#port no	
app.config["MAIL_USERNAME"]="tester.insurepro@gmail.com"
app.config["MAIL_PASSWORD"]="Tester@4567!!!" #passwd
app.config["MAIL_USE_TLS"]=True #transport 
app.config["MAIL_USE_SSL"]=False #

mail=Mail(app)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/get",methods=["POST"])
def get():
	fname=request.form["fname"]
	if not(fname.isalpha()) or len(fname)<2:
	    return render_template("home.html",msg="First name should contain alphabets only")
	lname=request.form["lname"]
	if not(lname.isalpha()) or len(lname)<2:
	    return render_template("home.html",msg="Last name should contain alphabets only")
	name=fname+" "+lname
	sex=request.form.get("sex")
	hf=int(request.form["hf"])
	hi=int(request.form["hi"])
	wt=float(request.form["wt"])
	height=0.3048*hf+0.0254*hi
	bmi=round((wt/height**2),0)
	pk=""
	if bmi<=26:
		pk="you are at low risk"
	else:
	   pk="you are at high risk"
	em=request.form["em"]
	age=float(request.form["age"])
	smk=request.form.get("smk")
	with open("ic.model","rb") as f:
		model=pickle.load(f)
	data=[[bmi,age,smk]]
	res=model.predict(data);	ans=round(res[0],0)
	msg=Message("Report for the medical insurance",sender="tester.insurepro@gmail.com",recipients=[em])
	msg.body="Hey "+str(name).title()+"\n"+"Thanks for using InsurePro. Your medical insurance cost for this month is Rs."+str(ans)+" Your BMI is "+str(bmi)+" which means "+str(pk)
	mail.send(msg)
	return render_template("home.html",msg="Thanks for using this! You will receive a mail shortly.")

if __name__=="__main__":
	app.run(debug=True,use_reloader=True)
