from django.db import IntegrityError
from django.db.models import Q
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from models import Book
import requests


# Create your views here.
class ExternalBookApi(APIView):

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.context_dict = {}
        self.url = 'https://www.anapioficeandfire.com/api/books'
        return super(ExternalBookApi, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        self.get_books()
        return Response(self.context_dict, content_type='json')

    def get_books(self):
        try:
            final_data = []
            import pdb;pdb.set_trace()
            name = self.request.GET.get('name')
            self.url = self.url + '?name=' + name
            res = requests.get(self.url)
            if res.status_code == 200:
                data = res.json()

            if data:
                data = data[0]
                # Convert string format date to date format
                dt = datetime.strptime(data['released'], '%Y-%m-%dT%H:%M:%S').date()
                # Preparing data for output
                final_data.append({'name': data['name'], 'isbn': data['isbn'],
                                   'number_of_pages': data['numberOfPages'], 'authors': data['authors'],
                                   'publisher': data['publisher'], 'country': data['country'],
                                   'released_date': datetime.strftime(dt, '%Y-%m-%d')})

            self.context_dict['status_code'] = 200
            self.context_dict['status'] = "success"
            self.context_dict['data'] = final_data

        except Exception as e:
            self.context_dict['status_code'] = 500
            self.context_dict['status'] = "Something went wrong: {}".format(e)


class BookAPI(APIView):

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.context_dict = {}
        return super(BookAPI, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        self.get_object()
        return Response(self.context_dict, content_type='json')

    def post(self, *args, **kwargs):
        self.create_object()
        return Response(self.context_dict, content_type='json')

    def get_object(self):
        data = []
        name = self.request.POST.get('name')
        publisher = self.request.POST.get('publisher')
        country = self.request.POST.get('country')
        released_year = self.request.POST.get('released')
        try:
            # qs to search data if any parameter is paased to search
            if name or publisher or country or released_year:
                if released_year:
                    qs = Q(released__year=released_year)
                else:
                    qs = Q(released=released_year)

                qs = qs | Q(name=name) | Q(country=country) | Q(publisher=publisher)
                bookslist = list(Book.objects.filter(qs))

            else:
                bookslist = list(Book.objects.all())

            for book in bookslist:
                data.append({'id': book.pk, 'name': book.name, 'isbn': book.isbn, 'authors': book.author,
                             'number_of_pages': book.nopages, 'publisher': book.publisher,
                             'country': book.country, 'release_date': book.released})
            self.context_dict['status'] = "success"
            self.context_dict['status_code'] = 200
            self.context_dict['data'] = data
        except Exception as e:
            self.context_dict['status_code'] = 500
            self.context_dict['status'] = "Failed!"
            self.context_dict['statusDescription'] = "Something went wrong: {}".format(e)

    def create_object(self):
        name = self.request.POST.get('name')
        isbn = self.request.POST.get('isbn')
        author = self.request.POST.get('author')
        nopages = self.request.POST.get('nopages')
        publisher = self.request.POST.get('publisher')
        country = self.request.POST.get('country')
        released = self.request.POST.get('released')

        try:
            Book.objects.create(name=name, isbn=isbn, author=author, nopages=nopages,
                                publisher=publisher, country=country, released=released)
            self.context_dict['status_code'] = 201
            self.context_dict['status'] = "success"
            self.context_dict['data'] = [{'name': name, 'isbn': isbn, 'author': [author],
                                          'number_of_pages': nopages, 'publisher': publisher,
                                          'country': country,
                                          'released': datetime.strftime(
                                              datetime.strptime(released, '%Y-%m-%d').date(),
                                              '%d-%m-%Y')}]
        except IntegrityError:
            self.context_dict['status_code'] = 500
            self.context_dict['status'] = "Failed"
            self.context_dict['statusDescription'] = "Duplicate entry!"
        except ValueError:
            self.context_dict['status_code'] = 500
            self.context_dict['status'] = "Failed"
            self.context_dict['statusDescription'] = "Wrong value entered!"
        except Exception as e:
            self.context_dict['status_code'] = 500
            self.context_dict['status'] = "Failed"
            self.context_dict['statusDescription'] = "Something went wrong: {}".format(e)


class BookDetails(APIView):

    def dispatch(self, request, *args, **kwargs):
        self.book_id = self.kwargs['book_id']
        self.request = request
        self.context_dict = {}
        return super(BookDetails, self).dispatch(request,*args, **kwargs)

    def get(self, *args, **kwargs):
        self.get_object()
        return Response(self.context_dict, content_type='json')

    def patch(self, *args, **kwargs):
        self.update_object()
        return Response(self.context_dict, content_type='json')

    def delete(self, *args, **kwargs):
        self.delete_object()
        return Response(self.context_dict, content_type='json')

    def get_object(self):
        try:
            book = Book.objects.get(pk=self.book_id)
            self.context_dict['status_code'] = 200
            self.context_dict['status'] = "success"
            self.context_dict['data'] = [{'id': book.pk, 'name': book.name, 'isbn': book.isbn,
                                          'authors': book.author, 'number_of_pages': book.nopages,
                                          'publisher': book.publisher, 'country': book.country,
                                          'release_date': book.released}]
        except Book.DoesNotExist:
            self.context_dict['status_code'] = 400
            self.context_dict['status'] = "Not found!"
            self.context_dict['statusDescription'] = "No Book with id: {}" \
                                                     " is present.".format(self.book_id)

    def update_object(self):
        name = self.request.POST.get('name')
        isbn = self.request.POST.get('isbn')
        author = self.request.POST.get('author')
        nopages = self.request.POST.get('nopages')
        publisher = self.request.POST.get('publisher')
        country = self.request.POST.get('country')
        released_date = self.request.POST.get('released')
        try:
            book = Book.objects.get(pk=self.book_id)

            if name:
                book.name = name
            if isbn:
                book.isbn = isbn
            if author:
                book.author = author
            if nopages:
                book.nopages = nopages
            if publisher:
                book.publisher = publisher
            if country:
                book.country = country
            if released_date:
                book.released = datetime.strptime(released_date, '%Y-%m-%d').date()

            book.save()
            self.context_dict['status_code'] = 200
            self.context_dict['status'] = "success"
            self.context_dict['data'] = [{'id': book.pk, 'name': book.name, 'isbn': book.isbn,
                                          'authors': book.author, 'number_of_pages': book.nopages,
                                          'publisher': book.publisher, 'country': book.country,
                                          'release_date': book.released}]
        except Book.DoesNotExist:
            self.context_dict['status_code'] = 400
            self.context_dict['status'] = "Not found!"
            self.context_dict['statusDescription'] = "No Book with id: {}" \
                                                     " is present.".format(self.book_id)

    def delete_object(self):
        try:
            book = Book.objects.get(pk=self.book_id)
            book.delete()
            self.context_dict['status_code'] = 200
            self.context_dict['status'] = "success"
            self.context_dict['message'] = "The book {} was deleted successfully.".format(book.name)
            self.context_dict['data'] = list(Book.objects.filter(pk=self.book_id))
        except Book.DoesNotExist:
            self.context_dict['status_code'] = 400
            self.context_dict['status'] = "Not Found!"
            self.context_dict['statusDescription'] = "No Book with id: {}" \
                                                     " is present.".format(self.book_id)
