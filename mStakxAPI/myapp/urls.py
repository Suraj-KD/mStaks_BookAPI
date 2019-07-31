from django.conf.urls import url
from myapp import views

urlpatterns = [
    url(r'^books$', views.BookAPI.as_view(), name='books'),
    url(r'books/(?P<book_id>[\d]+)', views.BookDetails.as_view(), name='book_details'),
]