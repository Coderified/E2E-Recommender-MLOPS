from flask import Flask,render_template,request
from pipeline.prediction_pipeline import hybrid_recommendation

app = Flask(__name__)

@app.route('/' , methods=['GET','POST'])
def home():
    recommendations = None

    if request.method == 'POST':
        try:
            print("Entering Try block")
            user_id = int(request.form["userID"])
            print("User ID is ",user_id)  # Debug print
            recommendations = hybrid_recommendation(user_id)
            print("recoms",recommendations)  # Debug print

        except Exception as e:
            print("Error occured....")

    return render_template('index.html' , recommendations=recommendations)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)