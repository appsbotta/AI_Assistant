import time
from flask import Flask,render_template,url_for,request,redirect
from bot.pipeline.prediction import PredictionPipeline
from bot.pipeline.training import TrainingPipeline

prediction_pipeline = PredictionPipeline()
training_pipeline = TrainingPipeline()
retriever_chain = prediction_pipeline.chain()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    training_pipeline.train()
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            start = time.process_time()
            # Invoke the retrieval chain with the prompt
            res = retriever_chain.invoke({"input": prompt})
            elapsed = time.process_time() - start
            print("Response Time:", elapsed)
            answer = res['answer']
    return render_template('index.html', answer=answer)

@app.route('/train',methods=["GET"])
def train():
    training_pipeline.train()
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug = True)