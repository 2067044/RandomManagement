from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from project_management.kris.kris_models import Task, Message, File
from project_management.models import Project

from datetime import date
from pip._vendor.requests.models import Response

# Create your tests here.

class ModelsTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("user1", "user1@user.com", "pass")
        self.owner1 = User.objects.create_user("owner1", "ownder1@user.com", "pass")
        self.project1 = Project.objects.create(name = 'project 1', description = "first project ", owner = self.owner1)
        self.task = Task(title = "imeto be", description ="let's see if the the test works", due_date = date.today(), project = self.project1)
        self.message = Message(title = "first test", description = "first test description", task = self.task, user = self.user1, date = date.today())
        
    def test_ensure_name_is_not_blank(self):        
        self.assertEqual( (len(self.task.title)>0 and len(self.task.description) > 0), True)
                         
    def test_slug_line_creation(self):
        self.assertEqual(self.project1.slug, 'project-1')
    
    def test_message(self):
       
        self.assertEqual(self.message.title, "first test")
        self.assertEqual(self.message.description, "first test description" )
    
    def test_message_user(self):
#         message = Message(title = "first test", description = " first test description", task = self.task, user = self.user1, date = date.today())
        self.assertEqual(self.message.user, self.user1)
        
