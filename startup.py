from db.db_setup import setup_db


# TODO: Let the user create portions now, in settings, they can create more, remind the user this after creating the portions.
def startup():
    setup_db()
    while True:
        print("Portions need creating")
        print("Create a new portion type:")
        uinput = input("Portion Name:")
