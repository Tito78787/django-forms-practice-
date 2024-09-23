
# Forms Practice

Here are some practical scenarios to help you learn and practice Django forms and validation:

### 1. Simple Contact Form with Validation
**Scenario**: Create a contact form where users can submit their name, email, and message. The email field should only accept valid email formats, and the message must be at least 10 characters long.

**Skills Practiced**:
- Creating forms using Django’s `forms.Form` class.
- Adding custom validators for fields (e.g., `validate_email`).
- Using built-in validators like `MinLengthValidator`.
- Handling form submission and displaying error messages.

---

### 2. User Registration with Password Confirmation
**Scenario**: Build a registration form that requires users to enter their username, email, password, and confirm their password. Validate that the password confirmation matches the original password and that the email is unique in the system.

**Skills Practiced**:
- Using `forms.ModelForm` to work with the `User` model.
- Adding custom validation logic to check that both password fields match.
- Validating unique fields (like email) at the database level.
- Displaying form errors for invalid submissions.

---

### 3. Login Form with Authentication
**Scenario**: Develop a login form where users input their username and password. Add validation to ensure that both fields are required, and check that the credentials match an existing user in the database.

**Skills Practiced**:
- Using Django’s `AuthenticationForm` or creating a custom login form.
- Validating credentials using `authenticate` and `login` methods.
- Handling form errors like "invalid username or password."

---

### 4. Profile Update Form with Conditional Validation
**Scenario**: Allow users to update their profile information (e.g., first name, last name, email, phone number). If they change their email, ensure the new email is unique. If the phone number is provided, ensure it follows a specific format (e.g., US phone number).

**Skills Practiced**:
- Using `forms.ModelForm` to work with the `User` or custom profile model.
- Adding conditional validation (e.g., validate the phone number only if it's provided).
- Creating a custom validator to match the phone number format.

---

### 5. Multi-Step Form with Validation
**Scenario**: Create a multi-step form for a user to fill out their profile information in stages (e.g., basic info, contact details, preferences). Validate each step individually before allowing the user to proceed to the next step.

**Skills Practiced**:
- Using `FormWizard` or manually managing form steps.
- Validating each form at the end of each step.
- Storing form data between steps (e.g., using sessions).
- Handling navigation between steps based on validation success.

---

### 6. Dynamic Form Fields Based on User Input
**Scenario**: Build a form where the available options in certain fields are dependent on the user’s previous selection (e.g., if a user selects "Electronics" in a category field, the "Subcategory" field dynamically updates with options like "Phones," "Laptops," etc.). Validate that a valid subcategory is selected.

**Skills Practiced**:
- Using `ModelChoiceField` for dynamic field population.
- Adding custom logic in the form to dynamically adjust available choices.
- Handling client-side and server-side validation for dynamically populated fields.

---

### 7. File Upload Form with Size and Type Validation
**Scenario**: Create a form that allows users to upload a profile picture. The form should validate that the file is an image and that its size doesn’t exceed a specific limit (e.g., 2 MB).

**Skills Practiced**:
- Creating file upload forms using `forms.FileField`.
- Validating file types (e.g., only allow JPEG or PNG).
- Using custom validators to check file size.
- Storing and serving uploaded files securely.

---

### 8. Survey Form with Custom Validation
**Scenario**: Design a survey form where users answer multiple-choice questions. Ensure that certain questions are required based on previous answers (e.g., if a user answers "Yes" to "Do you have pets?", a question about pet types becomes required).

**Skills Practiced**:
- Building a form with multiple fields using `forms.Form`.
- Adding conditional validation logic based on user responses.
- Handling required fields based on other field values.
- Displaying context-sensitive error messages.

---

### 9. Product Order Form with Quantity Validation
**Scenario**: Create an order form where users can select a product and input the quantity. Ensure that the quantity is within available stock and not below 1. Provide validation feedback if stock levels are insufficient.

**Skills Practiced**:
- Using `forms.ModelForm` to connect the form with a `Product` model.
- Adding custom validation logic for checking stock levels.
- Displaying form errors for invalid quantities.

---

### 10. Reservation Form with Date Validation
**Scenario**: Develop a reservation form for a restaurant or hotel. Validate that the chosen reservation date is in the future and that the user hasn’t selected a time during non-operating hours.

**Skills Practiced**:
- Using `forms.DateField` and `forms.TimeField`.
- Adding custom validators to check the date and time range.
- Handling form errors for invalid dates or times.

---

### 11. Feedback Form with Anti-Spam Validation
**Scenario**: Create a feedback form where users can submit comments. Add anti-spam measures like CAPTCHA or a honeypot field, and validate that no automated bots are submitting the form.

**Skills Practiced**:
- Using Django’s CAPTCHA field (or third-party libraries like reCAPTCHA).
- Adding a honeypot field for invisible bot detection.
- Validating and handling form submissions to prevent spam.

---

### 12. Subscription Form with Email Uniqueness Validation
**Scenario**: Create a subscription form where users provide their email to subscribe to a newsletter. Validate that the email is unique and not already subscribed, and ensure the email format is valid.

**Skills Practiced**:
- Creating a form with `EmailField`.
- Using custom validation to check email uniqueness in the database.
- Handling form submission and sending confirmation emails.

---

By working through these scenarios, you’ll gain a comprehensive understanding of Django forms and validation techniques, from basic field validation to more advanced use cases.
