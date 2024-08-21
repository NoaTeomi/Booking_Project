from django.urls import path
from .views import HomePageView, HotelsPageView, HotelsDetailView, RoomDetailView, ReservationFormView
from .views import error_room_view, error_dates_view
from .views import order_confirmation_view, invalid_dates_view
from .rest_views import HotelListApiView, RoomListApiView, AvailableRoomsApiView

urlpatterns = [
    path("",HomePageView.as_view(),name="home"),
    path("hotels/",HotelsPageView.as_view(),name="hotels"),
    path("hotel/<int:pk>/",HotelsDetailView.as_view(),name="hotel_details"),
    path('room/<int:pk>/', RoomDetailView.as_view(), name='room_details'),
    path('reservation/<int:pk>/', ReservationFormView.as_view(), name='reservation_form'),
    path('order-confirmation/<int:reservation_id>/', order_confirmation_view, name='order_confirmation'),
    path('error_room/',error_room_view,name="error_room"),
    path('error_dates/', error_dates_view, name='error_dates'),
    path('invalid_dates/',invalid_dates_view, name='invalid_dates'),

    path("api/hotels/",HotelListApiView.as_view(http_method_names=['get'])),
    path("api/hotel/",HotelListApiView.as_view(http_method_names=['post'])),
    path("api/rooms/",RoomListApiView.as_view(http_method_names=['get'])),
    path("api/room/",RoomListApiView.as_view(http_method_names=['post'])),
    path('api/available_rooms/', AvailableRoomsApiView.as_view(http_method_names=['get'])),
]