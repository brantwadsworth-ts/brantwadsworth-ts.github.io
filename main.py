
form_values = {
    "email": "",
    "like-level": ""
}

display(f"Form values are: {form_values}", target="form-values")


# Create all the event handlers

def submit_handler(event = None):
    if event:
        event.preventDefault()
        display(f"Form values are: {form_values}", target="form-values")

def reset_handler(event = None):
    if event:
        form_values = {
            "email": "",
            "like-level": ""
        }

        display(f"Form values are: {form_values}", target="form-values")

def email_input_handler(event = None):
    if event:
        form_values["email"] = event.target.value

def change_handler(event = None):
    if event:
        form_values["like-level"] = event.target.value

# Now map the event handlers to the elements

Element("email").element.oninput = email_input_handler
Element("like-level").element.onchange = change_handler
Element("form").element.onsubmit = submit_handler
Element("form").element.onreset = reset_handler
