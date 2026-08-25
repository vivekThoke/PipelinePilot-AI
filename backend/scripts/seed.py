import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models import Account, Lead


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        existing_account = await session.scalar(
            select(Account).where(
                Account.name == "Acme Logistics"
            )
        )

        if existing_account:
            print("Seed data already exists.")
            return

        account = Account(
            name="Acme Logistics",
            industry="Logistics",
            company_size=5000,
        )

        session.add(account)

        await session.flush()

        leads = [
            Lead(
                account_id=account.id,
                name="John Smith",
                email="john.smith@example.com",
                job_title="VP of Operations",
                status="new",
                source="enterprise_demo",
                notes=(
                    "Interested in reducing manual sales operations."
                ),
            ),
            Lead(
                account_id=account.id,
                name="Sarah Johnson",
                email="sarah.johnson@example.com",
                job_title="Sales Operations Manager",
                status="new",
                source="website",
                notes="Downloaded the revenue operations guide.",
            ),
            Lead(
                account_id=account.id,
                name="Mike Brown",
                email="mike.brown@example.com",
                job_title="Procurement Manager",
                status="contacted",
                source="conference",
                notes="Requested pricing information.",
            ),
        ]

        session.add_all(leads)

        await session.commit()

        print("Seed data created successfully.")


if __name__ == "__main__":
    asyncio.run(
        seed(),
        loop_factory=asyncio.SelectorEventLoop,
    )