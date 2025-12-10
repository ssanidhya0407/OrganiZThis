import asyncio
import httpx
import sys
import time

BASE_URL = "http://localhost:8000"
TIMESTAMP = int(time.time())
ORG_NAME = f"TestOrg_{TIMESTAMP}"
NEW_ORG_NAME = f"NewTestOrg_{TIMESTAMP}"
EMAIL = f"admin_{TIMESTAMP}@testorg.com"
PASSWORD = "password123"

async def main():
    async with httpx.AsyncClient() as client:
        # 1. Create Organization
        print(f"1. Creating Organization {ORG_NAME}...")
        response = await client.post(f"{BASE_URL}/org/create", json={
            "organization_name": ORG_NAME,
            "email": EMAIL,
            "password": PASSWORD
        })
        print(f"Create Response: {response.status_code} - {response.text}")
        if response.status_code != 200:
            return

        # 2. Admin Login
        print("\n2. Admin Login...")
        response = await client.post(f"{BASE_URL}/admin/login", json={
            "email": EMAIL,
            "password": PASSWORD
        })
        print(f"Login Response: {response.status_code}")
        if response.status_code != 200:
            return
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Get Organization
        print(f"\n3. Get Organization {ORG_NAME}...")
        response = await client.get(f"{BASE_URL}/org/get", params={"organization_name": ORG_NAME})
        print(f"Get Response: {response.status_code} - {response.json()}")

        # 4. Update Organization (Rename)
        print(f"\n4. Updating Organization (Rename to {NEW_ORG_NAME})...")
        response = await client.put(f"{BASE_URL}/org/update", json={
            "organization_name": NEW_ORG_NAME
        }, headers=headers)
        print(f"Update Response: {response.status_code} - {response.text}")

        # 5. Get Updated Organization
        print(f"\n5. Get Updated Organization {NEW_ORG_NAME}...")
        response = await client.get(f"{BASE_URL}/org/get", params={"organization_name": NEW_ORG_NAME})
        print(f"Get Response: {response.status_code} - {response.json()}")

        # 6. Delete Organization
        print(f"\n6. Deleting Organization {NEW_ORG_NAME}...")
        response = await client.delete(f"{BASE_URL}/org/delete", params={"organization_name": NEW_ORG_NAME}, headers=headers)
        print(f"Delete Response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    asyncio.run(main())
