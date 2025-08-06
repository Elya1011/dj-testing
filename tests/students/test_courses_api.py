import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_receiving_the_first_course(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    for i, c in enumerate(data):
        assert c['name'] == course[i].name

@pytest.mark.django_db
def test_receiving_the_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/?id=1')
    assert response.status_code == 200
    data = response.json()
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name

@pytest.mark.django_db
def test_course_list_filter_by_id(client, course_factory):
    courses = course_factory(_quantity=15)
    response = client.get('/api/v1/courses/?id=3')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) and len(data) == 1
    assert data[0]['id'] == 3
    assert data[0]['id'] == courses[2].id

@pytest.mark.django_db
def test_course_list_filter_by_name(client, course_factory):
    courses = course_factory(_quantity=15)
    course_name = courses[3].name
    response = client.get(f'/api/v1/courses/?name={course_name}')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) and len(data) == 1
    assert data[0]['name'] == course_name

@pytest.mark.django_db
def test_create_course(client):
    response = client.post('/api/v1/courses/', data={'name': 'Java'}, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=2)
    update_data = {'name': 'math'}
    url = f'/api/v1/courses/{courses[0].id}/'
    response = client.patch(url, data=update_data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == update_data['name']

@pytest.mark.django_db
def test_delete_course(client):
    response = client.post('/api/v1/courses/', data={'name': 'Java'}, format='json')
    assert response.status_code == 201
    response = client.delete('/api/v1/courses/1/')
    assert response.status_code == 204