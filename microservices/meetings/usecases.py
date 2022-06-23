from dataclasses import dataclass
from typing import Any, List, Union

from dotenv import load_dotenv
import requests
import os
import out

load_dotenv()
@dataclass
class ListMeetingsUseCase:
    conn: Any

    def execute(self):
        cursor = self.conn.cursor()
        query = """SELECT * FROM meetings"""
        cursor.execute(query)
        rows = cursor.fetchall()
        return [out.MeetingOut.format(data) for data in rows]


@dataclass
class CreateMeetingUseCase:
    conn: Any

    def execute(self, input_params: 'Input') -> None:
        category_api_url = os.getenv("CATAGEORY_API_URL")

        category_response = requests.get(category_api_url + "/category/{}".format(input_params.category_id)).json()
        
        if(category_response["success"] == False):
            raise Exception(category_response["error"])
        print(input_params)

        cursor = self.conn.cursor()
        query = """INSERT INTO meetings(name, category_id, category_name, participants_username, duration_min, event_time)
        VALUES(%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            input_params.name, 
            input_params.category_id, 
            category_response["category"]["name"], 
            input_params.participants_username, 
            input_params.duration_min,
            input_params.date)
        )
        self.conn.commit()

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        category_id: int
        participants_username: List[str]
        duration_min: int
        date: int

@dataclass
class GetMeetingByIdUseCase:
    conn: Any

    def execute(self, meeting_id: str):
        cursor = self.conn.cursor()
        query = """SELECT * FROM meetings WHERE id = %s LIMIT 1"""
        cursor.execute(query, (str(meeting_id)))
        row = cursor.fetchone()

        if row == None:
            raise Exception("Meeting with id: {} not found".format(meeting_id))
        
        return out.MeetingOut.format(row)

@dataclass
class EnrollMeetingUseCase:
    conn: Any

    def execute(self, meeting_id: str, username: str):
        cursor = self.conn.cursor()
        query = """SELECT * FROM meetings WHERE id = %s LIMIT 1"""
        cursor.execute(query, (str(meeting_id)))
        row = cursor.fetchone()

        if row == None:
            raise Exception("Meeting with id: {} not found".format(meeting_id))
        
        meeting = out.MeetingOut.format(row)
        if username in meeting["participants_username"]:
            raise Exception("User already registered on this meeting")
        
        meeting["participants_username"].append(username)

        query_update = """UPDATE meetings SET participants_username = %s WHERE id = %s"""
        cursor.execute(query_update, (meeting["participants_username"], meeting_id))
        self.conn.commit()
        return meeting