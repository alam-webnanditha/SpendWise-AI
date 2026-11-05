
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training examples for the AI model
descriptions = [
    "pizza burger restaurant lunch dinner food groceries",
    "amazon clothes shoes shopping mall dress",
    "uber ola bus train petrol travel transport",
    "college books textbook course tuition fees",
    "electricity water internet mobile bill",
    "movie cinema games entertainment",
    "medicine doctor hospital pharmacy health",
    "monthly salary income paycheck",
]

categories = [
    "Food",
    "Shopping",
    "Transport",
    "Education",
    "Bills",
    "Entertainment",
    "Health",
    "Salary",
]

# Convert text into numerical features
vectorizer = CountVectorizer()

X = vectorizer.fit_transform(descriptions)

# Train the machine-learning model
model = MultinomialNB()
model.fit(X, categories)


def predict_category(description):
    description_vector = vectorizer.transform([description])
    prediction = model.predict(description_vector)

    return prediction[0]
