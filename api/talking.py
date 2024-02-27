# This is api implementation of the session and talking history.
from fastapi import APIRouter
from db.model import ChatSession, Session, TalkingHistory
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import datetime

router = APIRouter()


class ChatSessionToCreate(BaseModel):
    name: str


class TalkingHistoryToCreate(BaseModel):
    role: str
    message: str


# API for get /users/{user_id}/sessions
# This API will return all the chat sessions for the user.
@router.get("/users/{user_id}/sessions")
async def list_sessions(user_id: int):
    with Session() as session:
        chat_sessions = session.query(ChatSession).filter_by(user_id=user_id).all()
        return [
            {
                "id": chat_session.id,
                "user_id": chat_session.user_id,
                "name": chat_session.name,
            }
            for chat_session in chat_sessions
        ]


# API for create a session for a user
@router.post("/users/{user_id}/sessions")
async def create_session(user_id: int, chat_session: ChatSessionToCreate):
    with Session() as session:
        new_session = ChatSession(
            user_id=user_id, name=chat_session.name
        )
        session.add(new_session)
        session.commit()
        return {
            "id": new_session.id,
            "user_id": new_session.user_id,
            "name": new_session.name,
        }


# API for get talking history for a chat session of a user
# This API will return all the talking history for a chat session.
@router.get("/users/{user_id}/sessions/{session_id}/talking_histories")
async def list_talking_histories(user_id: int, session_id: int):
    histories = db_list_talking_histories(user_id, session_id)
    return [
        {
            "id": talking_history.id,
            "user_id": talking_history.user_id,
            "chat_session_id": talking_history.chat_session_id,
            "timestamp": talking_history.timestamp,
            "role": talking_history.role,
            "message": talking_history.message,
        }
        for talking_history in histories
    ]

def db_list_talking_histories(user_id: int, session_id: int):
    with Session() as session:
        talking_histories = (
            session.query(TalkingHistory)
            .filter_by(user_id=user_id, chat_session_id=session_id)
            .order_by(TalkingHistory.timestamp)
            .all()
        )
        return talking_histories


# API for create a talking history for a chat session of a user
@router.post("/users/{user_id}/sessions/{session_id}/talking_histories")
async def say(
    user_id: int, session_id: int, talking_history: TalkingHistoryToCreate
):

    histories = db_list_talking_histories(user_id, session_id)
    say_content = TalkingHistory(
            user_id=user_id, 
            chat_session_id=session_id, 
            timestamp=datetime.datetime.now(),
            role=talking_history.role,
            message=talking_history.message
        )
    histories.append(say_content)
    answer_content = talk(user_id, session_id, talk_histories=histories)
    histories.append(answer_content)

    with Session() as session:
        session.add(say_content)
        session.add(answer_content)
        session.commit()
    histories = db_list_talking_histories(user_id, session_id)
    return [
        {
            "id": talking_history.id,
            "user_id": talking_history.user_id,
            "chat_session_id": talking_history.chat_session_id,
            "timestamp": talking_history.timestamp,
            "role": talking_history.role,
            "message": talking_history.message,
        }
        for talking_history in histories
    ]

def talk(user_id, session_id, talk_histories: List[TalkingHistory]):
    # do a chat completion using openai api, and receive the response
    # Add it to the talk_history and append it to db.
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": talk_history.role,
                "content": talk_history.message
            } for talk_history in talk_histories
        ])
    return TalkingHistory(
            user_id=user_id, 
            chat_session_id=session_id, 
            timestamp=datetime.datetime.fromtimestamp(response.created),
            role="assistant",
            message=response.choices[0].message.content
        )
