import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import Contact, User

from repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
    get_upcoming_birthdays,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.body = Contact(
            user_id=self.user.id,
            first_name="Name",
            last_name="Lastname",
            email="xyz@example.com",
            phone_number="123 456 789",
            birth_date=(date.today() + timedelta(days=366 * 20)).strftime("%Y-%m-%d"),
            extra_data="Extra data"
        )

    async def test_crate_contact(self):
        body = self.body
        result = await create_contact(body=body, user=self.user, db=self.session)

        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birth_date, body.birth_date)
        self.assertEqual(result.extra_data, body.extra_data)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)

        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)

        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)

        self.assertIsNone(result)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)

        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)

        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = self.body
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)

        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = self.body
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)

        self.assertIsNone(result)

    async def test_get_upcoming_birthdays(self):
        future_birthday = self.body
        self.session.query().filter().all.return_value = [future_birthday]
        result = await get_upcoming_birthdays(user=self.user, db=self.session)

        self.assertEqual(result[0].id, future_birthday.id)
        self.assertEqual(result[0].first_name, future_birthday.first_name)
        self.assertEqual(result[0].last_name, future_birthday.last_name)
        self.assertEqual(result[0].email, future_birthday.email)
        self.assertEqual(result[0].phone_number, future_birthday.phone_number)
        self.assertEqual(result[0].birth_date, future_birthday.birth_date)
        self.assertEqual(result[0].extra_data, future_birthday.extra_data)


if __name__ == '__main__':
    unittest.main()