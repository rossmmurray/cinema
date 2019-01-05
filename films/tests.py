from django.test import TestCase
from django.urls import reverse
from films.models import Film, Screening
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class IndexViewTests(TestCase):
	def test_good_response(self):
		"""Get a 200 back from the view"""
		response = self.client.get(reverse('screening_choice'))
		self.assertEqual(response.status_code, 302)


class FilmTests(TestCase):
	def setUp(self):
		"""Create a film object to be used in other tests"""
		image_path = '/Users/rossmurray/Uni/IntroPython/coursework/cinema/test_images/thelma.jpg'
		new_image = SimpleUploadedFile(name='thelma.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

		# N.B. object.create saves to database immediately
		new_film = Film.objects.create(
			title='Thelma and Louise',
			description="Somebody said get a life...so they did. In Ridley Scott's adventurous road picture.",
			image=new_image
		)

	def test_new_film(self):
		"""Test creating second film in database"""
		image_path = '/Users/rossmurray/Uni/IntroPython/coursework/cinema/test_images/thelma.jpg'
		new_image = SimpleUploadedFile(name='thelma.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
		new_film = Film(
			title='Batman and Robin',
			description="Batman tries to save Gotham.",
			image=new_image
		)
		self.assertEqual(new_film.clean(), None)
		new_film.save()

	def test_duplicate_film(self):
		"""Test film creation with the same title"""
		image_path = '/Users/rossmurray/Uni/IntroPython/coursework/cinema/test_images/thelma.jpg'
		new_image = SimpleUploadedFile(name='thelma.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
		new_film = Film(
			title='Thelma and Louise',
			description="Somebody said get a life...so they did. In Ridley Scott's adventurous road picture.",
			image=new_image
		)
		with self.assertRaises(IntegrityError):
			new_film.save()

	def test_screening_creation(self):
		"""Test screening creation"""
		new_film = Film.objects.get(title="Thelma and Louise")

		# future screening
		time = timezone.now() + timedelta(days=1)
		new_screening = Screening(film=new_film, date_time=time)
		self.assertEqual(new_screening.clean(), None)

		# overlapping screening
		new_screening.save()
		time += timedelta(minutes=20)
		new_screening = Screening(film=new_film, date_time=time)
		with self.assertRaises(ValidationError):
			new_screening.clean()

		# past screening
		time = timezone.now() - timedelta(days=1)
		new_screening = Screening(film=new_film, date_time=time)
		with self.assertRaises(ValidationError):
			new_screening.clean()




