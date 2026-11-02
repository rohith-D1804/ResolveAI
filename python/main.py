from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from db import get_connection
from pydantic import BaseModel, Field, field_validator
from typing import Literal

app = FastAPI()


class TicketCreate(BaseModel):
    customer: str = Field(min_length=1)
    issue: str = Field(min_length=1)

    @field_validator("customer", "issue")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field cannot be blank")
        return value.strip()


class TicketStatusUpdate(BaseModel):
    status: Literal["open", "in_progress", "resolved"]


@app.get("/")
def home():
    return {"message": "Welcome to ResolveAI!"}


@app.get("/tickets")
def get_tickets():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tickets ORDER BY id")

            tickets = cursor.fetchall()

    return tickets

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, customer, issue, status FROM tickets WHERE id = %s",
                (ticket_id,)
            )
            ticket = cursor.fetchone()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@app.post("/tickets")
def create_ticket(ticket: TicketCreate):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tickets (customer, issue)
                VALUES (%s, %s)
                RETURNING id, customer, issue, status
                """,
                (ticket.customer, ticket.issue)
            )

            new_ticket = cursor.fetchone()

    return new_ticket

@app.patch("/tickets/{ticket_id}")
def update_ticket_status(ticket_id: int, update: TicketStatusUpdate):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tickets
                SET status = %s
                WHERE id = %s
                RETURNING id, customer, issue, status
                """,
                (update.status, ticket_id)
            )
            ticket = cursor.fetchone()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM tickets
                WHERE id = %s
                RETURNING id
                """,
                (ticket_id,)
            )
            deleted_ticket = cursor.fetchone()

    if deleted_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"message": "Ticket deleted successfully", "id": deleted_ticket["id"]}