import questionary

questionary.text("What's your first name").ask()
passwd = questionary.password("What's your secret?").ask()
print("The password is", passwd)
responseConfirm = questionary.confirm("Are you amazed?").ask()
print("The confirmation is", responseConfirm)
questionary.select(
    "What do you want to do?",
    choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
).ask()

questionary.rawselect(
    "What do you want to do?",
    choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
).ask()

opcionesSelected = questionary.checkbox(
    "Select toppings", choices=["foo", "bar", "bazz"]
).ask()

questionary.path("Path to the projects version file").ask()