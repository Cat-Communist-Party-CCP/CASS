"""
Quick test for PostgresRunner
Run: python -m backend.src.cass.integrations.database.test_postgres
"""

import asyncio
import os
from postgres import PostgresRunner


async def main():
    # Connection string for local PostgreSQL
    conn_str = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:1693@localhost:5432/cassdb"
    )

    # Using context manager (recommended)
    async with PostgresRunner(conn_str) as db:
        # Test 1: Simple query
        print("=== Test 1: Query customers ===")
        customers = await db.execute(
            "SELECT id, first_name, last_name, city FROM customers LIMIT 5"
        )
        for c in customers:
            print(f"  {c['id']}: {c['first_name']} {c['last_name']} ({c['city']})")

        # Test 2: Get schema
        print("\n=== Test 2: Get schema ===")
        schema = await db.get_schema()
        print(schema[:500] + "...")  # Print first 500 chars

        # Test 3: Count query
        print("\n=== Test 3: Count records ===")
        counts = await db.execute("""
            SELECT
                (SELECT COUNT(*) FROM customers) as customers,
                (SELECT COUNT(*) FROM products) as products,
                (SELECT COUNT(*) FROM orders) as orders
        """)
        print(f"  Customers: {counts[0]['customers']}")
        print(f"  Products: {counts[0]['products']}")
        print(f"  Orders: {counts[0]['orders']}")

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
