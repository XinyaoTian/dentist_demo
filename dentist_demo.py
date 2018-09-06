from app import application
from app.FunctionalModels.PredictionAnalysis import PredictionAnalysis

if __name__ == '__main__':
    application.run(host='0.0.0.0',port=5000,debug=False)