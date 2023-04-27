import inspect
import os
from typing import Any, Optional

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

def getenvvar(key: str, default: Optional[Any] = None, empty_as_none: bool = False, parse_bool: bool = False) -> Any:
    value = None
    try:
        value = os.environ.get(key, default)
        if isinstance(value, str) and len(value) == 0:
            value = None
    except KeyError as err:
        pass
    if parse_bool:
        if value in [None, "0", "False", 0, "false", "n", "N"]:
            value = False
        else:
            value = True
    return value

def get_authenticator() -> LDAPAuthenticator:
    authenticator = LDAPAuthenticator()
    authenticator.server_address = getenvvar("LDAP_HOST", "localhost")
    authenticator.use_ssl = getenvvar("LDAP_SSL", True, parse_bool=True)
    authenticator.lookup_dn_search_user = getenvvar("LDAP_SEARCH_USER", None)
    authenticator.lookup_dn_search_password = getenvvar("LDAP_SEARCH_PASSWORD", None)
    authenticator.lookup_dn = True
    template = getenvvar("LDAP_BIND_DN_TEMPLATE", "cn={username},ou=people,dc=planetexpress,dc=com", True)
    authenticator.bind_dn_template = template if template else list()
    authenticator.user_search_base = getenvvar("LDAP_USER_SEARCH_BASE","ou=people,dc=planetexpress,dc=com")
    authenticator.user_attribute = getenvvar("LDAP_USER_ATTRIBUTE", "uid")
    authenticator.lookup_dn_user_dn_attribute = getenvvar("LDAP_LOOKUP_DB_USER_DN_ATTRIBUTES", "cn")
    authenticator.valid_username_regex = getenvvar("LDAP_VALID_USERNAME_REGEX", r"^[a-z][.a-z0-9_-]*$")
    authenticator.escape_userdn = getenvvar("LDAP_ESCAPE_USER_DN", True, parse_bool=True)
    authenticator.attributes = ["uid", "cn", "mail", "ou"]
    authenticator.use_lookup_dn_username = False
    authenticator.use_lookup_dn_user_for_group_lookup = getenvvar("LDAP_USE_LOOKUP_DN_USER_FOR_GROUP_LOOKUP", False, parse_bool=True)
    authenticator.allowed_groups = list(getenvvar("LDAP_ALLOWED_GROUPS",
        "cn=admin_staff,ou=people,dc=planetexpress,dc=com|cn=ship_crew,ou=people,dc=planetexpress,dc=com").split("|"))
    authenticator.auth_state_attributes =  list(getenvvar("LDAP_AUTH_STATE_ATTRIBUTES", "").split("|"))
    
    return authenticator

@pytest.fixture(scope="session")
def authenticator():
    return get_authenticator()
