from datetime import datetime
from typing import List
from fastapi import APIRouter, status, Response
from pydantic import BaseModel
import usecases
import database

meetingsRouter = APIRouter(
    tags=["meeting"]
)

@meetingsRouter.get("/meetings")
async def list_meetings():
    try:
        conn = database.create_server_connection()
        list_meetings_use_case = usecases.ListMeetingsUseCase(conn)

        meetings = list_meetings_use_case.execute()
        conn.close()
        return {"success": True, "meetings": meetings}
    except Exception as error:
        print(error)
        return {"success": False, "error": str(error)}

class CreateMeetingDTO(BaseModel):
    name: str
    category_id: int
    participants_username: List[str]
    duration_min: int
    date: datetime

# TODO: verify if the user is admin
@meetingsRouter.post("/meeting")
async def create_meeting(item: CreateMeetingDTO,  response: Response, ):
    try:
        conn = database.create_server_connection()

        create_meeting_use_case = usecases.CreateMeetingUseCase(conn)

        create_meeting_use_case.execute(
            input_params=item
        )
        conn.close()

        return {"success": True}
    except Exception as error:
        print(error)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"success": False, "error": str(error)}


@meetingsRouter.get("/meeting/{meeting_id}")
async def get_meeting(meeting_id: int, ):
    try:
        conn = database.create_server_connection()

        get_meeting_use_case = usecases.GetMeetingByIdUseCase(conn)

        result = get_meeting_use_case.execute(
            meeting_id=meeting_id
        )
        conn.close()

        return {"success": True, "meeting": result}
    except Exception as error:
        print(error)
        return {"success": False, "error": str(error)}
class EnrollMeetingDTO(BaseModel):
    username: str

# TODO: get user name from heades
@meetingsRouter.post("/meeting/{meeting_id}/enroll")
async def create_meeting(meeting_id: int, item: EnrollMeetingDTO,response: Response):
    try:
        conn = database.create_server_connection()

        enroll_meeting_use_case = usecases.EnrollMeetingUseCase(conn)

        enroll_meeting_use_case.execute(
            meeting_id=meeting_id,
            username=item.username
        )

        conn.close()
        return {"success": True}
    except Exception as error:
        print(error)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"success": False, "error": str(error)}