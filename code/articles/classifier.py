from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from articles.models import Article
from functools import reduce
import operator


def run_classifier():
    data = Article.objects.all()

    texts = [item.annotation for item in data]
    labels = [item.label for item in data]
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

    # Преобразование текста в TF-IDF векторы
    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Инициализация и обучение модели наивного Байеса
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train_vectorized, y_train)

    # Прогнозирование меток на тестовом наборе
    y_pred = nb_classifier.predict(X_test_vectorized)

    # Оценка точности
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

