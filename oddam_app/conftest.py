import pytest

from oddam_app.models import Institution
from user.models import CustomUser


@pytest.fixture
def create_user():
    return CustomUser.objects.create_user(email='fix@email.com', password='test123', first_name='test_first',
                                          last_name='test_last', username='test_normal', is_active=True)


@pytest.fixture
def create_institution():
    return Institution.objects.create(name='test_institution', description='fixture institution description',
                                      type='fundacja')
