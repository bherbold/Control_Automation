from Booking_System import bookingManager as BM


def update_bookings ():
    schedule = BM.loads_matrix()
    mode_array = []

    for hour in schedule:
        if hour['mode'] == 'Regular':
            mode_array.append('Regular')
        elif hour['mode'] == 'Economic':
            mode_array.append('Eco')
        else:
            mode_array.append('No Booking')
        
    #print(mode_array)