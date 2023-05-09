from django_tenants.test.client import TenantClient
from django_tenants.test.cases import TenantTestCase
from faker import Faker
from django.urls import reverse
from branches.models import Branch
from users.models import User

fake = Faker()


class BrancheModelTest(TenantTestCase):
    def setup(self):
        self.c = TenantClient(self.tenant)
        self.fake = Faker()
        self.user = User.objects.create_user(username=self.fake.user_name(), password=self.fake.password())

    def test_branch_create(self):
        data = {
            'name': self.fake.company(),
            'address': self.fake.address(),
            'phone': self.fake.random_number(digits=10),
            'description': self.fake.paragraph(),
            'image': self.fake.image_url(),
            'manager': self.user.pk,
            'state': True,
        }

        response = self.c.post(reverse('create_branch'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Branch.objects.filter(name=data['name']).exists())
