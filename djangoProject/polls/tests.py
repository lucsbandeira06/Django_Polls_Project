import datetime
from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from .models import Question, Choice
from django.contrib.auth.models import User



class AuthenticationTestCase(TestCase):
    """
    On this class I am testing if a user can login and logout the application. By creating a test user using the method
     User.objects.create_user and then call the client using the login path. If the login is successful, the user is
     redirected to the home page.
       """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

    def test_login(self):
        # Try to log in with correct credentials
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass',
        })
        # Check that the login was successful
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        """
        Below is the function to test if a user can log out the application successfully. By importing a model
         from Django view for logout, the user can exit the application which will then be redirected to the home
         page. 
         In order to test these functions, you can generate a failure by simply changing the url paths that I defined. 
        """
    def test_logout(self):
        # Log in as the test user
        self.client.login(username='testuser', password='testpass')
        # Try to log out
        response = self.client.get('/logout/')
        # Check that the logout was successful
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertFalse('_auth_user_id' in self.client.session)


class DatabaseTestCase(TestCase):
    def setUp(self):
        """
        Create some sample data for testing. This class creates a question object sample for testing.
        You should expect a warning on this test. The reason behind this warning is the fact that on the variable
         below, we are receiving a native datetime while time zone support is active. To fix that issue, I could have
         used deltatime instead.
        """
        self.question = Question.objects.create(
            question_text='Who is your favorite super-hero?',
            pub_date='2022-03-27 14:30:05'
        )
        self.choice1 = Choice.objects.create(
            question=self.question,
            choice_text='Spider-man',
            votes=1
        )
        self.choice2 = Choice.objects.create(
            question=self.question,
            choice_text='Batman',
            votes=0
        )


    def test_choice_votes(self):
        """
        Test that the votes attribute of the Choice model is incremented
        correctly. As we can see, choice1 is equal to 3, and choice2 is equal to 2. Therefore, when we run this test
        it will fail since we called the method self.assertEqual(self.choice1.votes, 1) which values don't match.

        """
        self.choice1.votes += 2
        self.choice1.save()
        self.choice2.votes += 2
        self.choice2.save()
        self.assertEqual(self.choice1.votes, 1)
        self.assertEqual(self.choice2.votes, 2)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future. In this case, the test will be successful since this test is using real time to publish.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed. In this case the message will not be displayed since
         I created a question test before running this class.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page. We can see that this function is pulling data from 30 days ago.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page. Below is a representation of a question created a month in the future. Because of that,
        this function returns null.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed. In this case, we can see that we are only asserting the query for the past questions.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions. On this test case, it becomes more clear how the queries
        are defined after calling both questions with publish dates in the past.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found. This test will fail as the publish date of future_question is in the future. Instead
        of using port 404 to pass the message, port 200 should have been applied to pass the response.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text. This is simply testing if past_question contains any attributes, which in this
        case will be true, as the question contains text and date values.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)