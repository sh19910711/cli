from makestack import api
from makestack.helpers import get_env_or_ask


def change_password(args):
    current_password      = get_env_or_ask("MAKESTACK_CURRENT_PASSWORD",
                                           "Current Password: ", password=True)
    new_password          = get_env_or_ask("MAKESTACK_NEW_PASSWORD",
                                           "New Password: ", password=True)
    password_confirmation = get_env_or_ask("MAKESTACK_PASSWORD_CONFIRMATION",
                                           "New Password (confirmation): ",
                                           password=True)

    if new_password != password_confirmation:
        error("New passwords din't match.")

    r = api.invoke('PUT', '/auth/password', params={
                     'current_password': current_password,
                     'password': new_password,
                     'password_confirmation': password_confirmation
                   }, prepend_user_path=False)
