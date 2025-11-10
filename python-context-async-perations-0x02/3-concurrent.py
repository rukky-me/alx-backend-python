#!/usr/bin/python3
"""
Run multiple database queries concurrently using asyncio.gather
and aiosqlite for asynchronous database interaction.
"""

import asyncio
import aiosqlite

DB_FILE = "users.db"


# --- Asynchronous query functions ---
async def async_fetch_users():
    """Fetch all users from the database asynchronously."""
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("[LOG] All users fetched.")
            return users


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("[LOG] Users older than 40 fetched.")
            return older_users


# --- Function to run both queries concurrently ---
async def fetch_concurrently():
    """Run both database queries concurrently using asyncio.gather."""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    all_users, older_users = results

    print("\n--- All Users ---")
    for user in all_users:
        print(user)

    print("\n--- Users Older Than 40 ---")
    for user in older_users:
        print(user)


# --- Entry point ---
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
