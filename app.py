from transformers import pipeline

model = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
print(model("이거 너무 좋아요!"))
