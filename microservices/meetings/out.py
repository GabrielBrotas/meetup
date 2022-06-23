from abc import abstractmethod


class MeetingOut:

    @abstractmethod
    def format(data):
        return {
            'id': data[0], 
            'name': data[1],
            'category_id': data[2], 
            'category_name': data[3], 
            'participants_username': data[4], 
            'duration_min': data[5], 
            'event_time': data[6]
        }
