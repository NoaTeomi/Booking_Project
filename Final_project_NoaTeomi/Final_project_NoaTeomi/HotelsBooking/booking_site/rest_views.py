from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Room, Reservation
from .serializers import HotelSerializer, RoomSerializer,ReservationSerializer
from datetime import datetime

class HotelListApiView(APIView):
    def get(self,request):
        hotels_list = Hotel.objects.all()
        serializer = HotelSerializer(hotels_list, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):

        data = {
            'name': request.data.get('name'), 
            'rank':request.data.get('rank'),
            'country' : request.data.get('country'), 
            'city': request.data.get('city') 
        }
        hotel = HotelSerializer(data=data)
        if hotel.is_valid():
            hotel.save()
            return Response(hotel.data, status=status.HTTP_201_CREATED)
        
        return Response(hotel.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RoomListApiView(APIView):
    def get(self,request):
        room_list = Room.objects.all()
        serializer = RoomSerializer(room_list, many=True)
        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):

        data = {
            'hotel':request.data.get('hotel'),
            'name': request.data.get('name'), 
            "serial_number": request.data.get("serial_number"),
            'max_guests': request.data.get('max_guests'),
            'price_for_night' : request.data.get('price_for_night'), 
            'size': request.data.get('size') 
        }
        room = RoomSerializer(data=data)
        if room.is_valid():
            room.save()
            return Response(room.data, status=status.HTTP_201_CREATED)
        
        return Response(room.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AvailableRoomsApiView(APIView):
    def get(self, request):
        check_in_date = request.query_params.get('check_in_date')
        check_out_date = request.query_params.get('check_out_date')

        if not check_in_date or not check_out_date:  # Validate date inputs
            return Response({"message": "Please provide both check_in_date and check_out_date."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"message": "Invalid date format. Please use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure check_out_date is after check_in_date
        if check_in_date >= check_out_date:
            return Response({"message": "check_out_date must be after check_in_date."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter rooms that are not reserved within the specified date range
        reserved_rooms = Reservation.objects.filter(
            check_out_date__gt=check_in_date,
            check_in_date__lt=check_out_date
        ).values_list('room_id', flat=True)
        
        available_rooms = Room.objects.exclude(id__in=reserved_rooms)
        
        if not available_rooms:
            return Response({"message": "No rooms found on these dates"}, status=status.HTTP_200_OK)
        
        # Serialize the available rooms
        serializer = RoomSerializer(available_rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request, *args, **kwargs):

        data = {
            'user':request.data.get('user'),
            'check_in_date': request.data.get('check_in_date'), 
            'check_out_date': request.data.get("check_out_date"),
            'hotel': request.data.get('hotel'),
            'room' : request.data.get('room'), 
            'total_price': request.data.get('total_price') 
        }
        reservation = ReservationSerializer(data=data)
        if reservation.is_valid():
            reservation.save()
            return Response(reservation.data, status=status.HTTP_201_CREATED)
        return Response(reservation.errors, status=status.HTTP_400_BAD_REQUEST)