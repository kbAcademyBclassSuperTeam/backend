import joblib



def model_predict(texts):
        
    transformer = joblib.load('corpus_transformer.pkl') 

    model = joblib.load('corpus.pkl')


    ex = transformer.transform({texts})
    y_pred = model.predict(ex)

    return y_pred[0]

# if __name__ == "__main__":
    # print(model_predict('현금 인출 하러 왔습니다.'))
