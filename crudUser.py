from email_validator import validate_email, EmailNotValidError

def validate_login(pswd, email):
    # validate password
    validate_result = [False, False, None]
    if len(pswd) > 6:
        for char in pswd:
            if char.isupper():
                validate_result[0] = True

    try:
        # Check that the email address is valid. Turn on check_deliverability
        # for first-time validations like on account creation pages (but not
        # login pages).
        emailinfo = validate_email(email, check_deliverability=False)
        validate_result[1] = True
        # After this point, use only the normalized form of the email address,
        # especially before going to a database query.
        email = emailinfo.normalized
    except EmailNotValidError as e:
        validate_result[2] = e
        # The exception message is human-readable explanation of why it's
        # not a valid (or deliverable) email address.

    return validate_result