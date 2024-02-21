# This is api implementation of the session and talking history.
from fastapi import APIRouter
from db.model import ChatSession, Session, TalkingHistory
from pydantic import BaseModel

router = APIRouter()


class ChatSessionToCreate(BaseModel):
    name: str
    prompt: str


class TalkingHistoryToCreate(BaseModel):
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
                "prompt": chat_session.prompt,
            }
            for chat_session in chat_sessions
        ]


# API for create a session for a user
@router.post("/users/{user_id}/sessions")
async def create_session(user_id: int, chat_session: ChatSessionToCreate):
    with Session() as session:
        new_session = ChatSession(
            user_id=user_id, name=chat_session.name, prompt=chat_session.prompt
        )
        session.add(new_session)
        session.commit()
        return {
            "id": new_session.id,
            "user_id": new_session.user_id,
            "name": new_session.name,
            "prompt": new_session.prompt,
        }


# API for get talking history for a chat session of a user
# This API will return all the talking history for a chat session.
@router.get("/users/{user_id}/sessions/{session_id}/talking_histories")
async def list_talking_histories(user_id: int, session_id: int):
    with Session() as session:
        talking_histories = (
            session.query(TalkingHistory)
            .filter_by(user_id=user_id, chat_session_id=session_id)
            .order_by(TalkingHistory.timestamp)
            .all()
        )

        return [
            {
                "id": talking_history.id,
                "user_id": talking_history.user_id,
                "chat_session_id": talking_history.chat_session_id,
                "timestame": talking_history.timestame,
                "role": talking_history.role,
                "message": talking_history.message,
            }
            for talking_history in talking_histories
        ]


# API for create a talking history for a chat session of a user
@router.post("/users/{user_id}/sessions/{session_id}/talking_histories")
def say(
    user_id: int, session_id: int, talking_history: TalkingHistoryToCreate
):
    with Session() as session:
        new_talking_history = TalkingHistory(
            user_id=user_id, 
            chat_session_id=session_id, 
            role="user",
            message=talking_history.message
        )
        session.add(new_talking_history)
        session.commit()
        return {
            "id": new_talking_history.id,
            "user_id": new_talking_history.user_id,
            "chat_session_id": new_talking_history.chat_session_id,
            "timestame": new_talking_history.timestame,
            "role": new_talking_history.role,
            "message": new_talking_history.message,
        }
