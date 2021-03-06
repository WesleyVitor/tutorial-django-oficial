
from ast import arg
from http import client
from unittest import TestResult
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from polls.models import Question
from django.test import Client
from datetime import timedelta

# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        
        #Return false if pub_date is in future
        time = timezone.now() + timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):

        time = timezone.now() - timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - timedelta(hours=23)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
class QuestionIndexViewTests(TestCase):
    client = Client()
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question("Past Question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
    
    def test_future_question(self):
        create_question("Future Question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
    
class QuestionDetailsViewTests(TestCase):
    client = Client()
    def test_future_question(self):

        future_question = create_question(question_text="Future Question", days=5)
        url = reverse("polls:details", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):

        past_question = create_question(question_text="Past Question", days=-5)
        url = reverse("polls:details", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        