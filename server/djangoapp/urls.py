from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [

    # Path for the about view
    path('about/', view=views.about, name='about'),

    # Path for the contact us view
    path('contact/', view=views.contact, name='contact'),

    # Path for registration
    path('registration/', view=views.registration_request, name='registration'),

    # Path for login
    path('login/', view=views.login_request, name='login'),

    # Path for logout
    path('logout/', view=views.logout_request, name='logout'),

    # Path for index
    path('', view=views.get_dealerships, name='index'),

    # Path for dealer reviews view
    path('dealer/<int:id>/', views.get_dealer_details, name='dealer_details'),

    # Path for add a review view
    path('dealer/review/<int:id>/', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
