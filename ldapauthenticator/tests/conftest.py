import inspect
import os

import pytest
from dotenv import load_dotenv

from ..ldapauthenticator import LDAPAuthenticator

@pytest.fixture(autouse=True, scope='session')
def session_encapsule():
    setup_session()
    yield
    teardown_session()


def setup_session():
    # Setup output dir for test session
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)


def teardown_session():
    pass

def pytest_collection_modifyitems(items):
    """add asyncio marker to all async tests"""
    for item in items:
        if inspect.iscoroutinefunction(item.obj):
            item.add_marker("asyncio")
        if hasattr(inspect, "isasyncgenfunction"):
            # double-check that we aren't mixing yield and async def
            assert not inspect.isasyncgenfunction(item.obj)


def get_authenticator() -> LDAPAuthenticator:
    authenticator = LDAPAuthenticator()
    authenticator.server_address = os.environ.get("LDAP_HOST", "localhost")
    authenticator.lookup_dn = True
    authenticator.bind_dn_template = "cn={username},ou=people,dc=planetexpress,dc=com"
    authenticator.user_search_base = os.environ.get("LDAP_USER_SEARCH_BASE","ou=people,dc=planetexpress,dc=com")
    authenticator.user_attribute = os.environ.get("LDAP_USER_ATTRIBUTE", "uid")
    authenticator.lookup_dn_user_dn_attribute = os.environ.get("LDAP_LOOKUP_DB_USER_DN_ATTRIBUTES", "cn")
    authenticator.escape_userdn = bool(os.environ.get("LDAP_ESCAPE_USER_DN", True))
    authenticator.attributes = ["uid", "cn", "mail", "ou"]
    authenticator.use_lookup_dn_username = False

    authenticator.allowed_groups = list(os.environ.get("LDAP_ALLOWED_GROUPS",
        "cn=admin_staff,ou=people,dc=planetexpress,dc=com|cn=ship_crew,ou=people,dc=planetexpress,dc=com").split("|"))
    return authenticator

@pytest.fixture(scope="session")
def authenticator():
    return get_authenticator()
