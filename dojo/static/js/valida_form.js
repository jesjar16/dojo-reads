document.addEventListener("DOMContentLoaded", function() {
    // if register_form is presente, then add event listener
    if (document.getElementById("register_form"))
        document.getElementById("register_form").addEventListener('submit', validarRegistro); 

    // if login_form is presente, then add event listener
    if (document.getElementById("login_form"))
        document.getElementById("login_form").addEventListener('submit', validarLogin); 
  });

// function to validate register form fields
function validarRegistro(evento) {
    evento.preventDefault();

    let first_name = document.getElementById('first_name').value;
    if (first_name.length == 0) {
        alert('First name can not be empty');
        document.getElementById('first_name').focus();
        return;
    }
    else if (first_name.length > 0 && first_name.length < 2) {
        alert('First name should be less at least 2 characters long');
        document.getElementById('first_name').focus();
        return;
    }

    let last_name = document.getElementById('last_name').value;
    if (last_name.length == 0) {
        alert('Last name can not be empty');
        document.getElementById('last_name').focus();
        return;
    }
    else if (last_name.length > 0 && last_name.length < 2) {
        alert('Last name should be less at least 2 characters long');
        document.getElementById('last_name').focus();
        return;
    }

    let email = document.getElementById('email').value;
    let mailformat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    
    if (email.length == 0) {
        alert('Email address can not be empty');
        document.getElementById('email').focus();
        return;
    }

    valid_email = mailformat.test(email);

    if (!valid_email) {
        alert("Email address is invalid");
        document.getElementById('email').focus();
        return;
    }

    let birthday_field = document.getElementById('birthday').value;
    if (!birthday_field) {
        alert("Birthday can not be empty");
        document.getElementById('birthday').focus();
        return;
    }
        
    let birthday= new Date(document.getElementById('birthday').value);

    // calculatin birthday difference in days and yearts
    difference_in_days = (Date.now() - birthday) / (1000 * 3600 * 24);
    difference_in_years = (Date.now() - birthday) / 1000;
    difference_in_years = difference_in_years / (60 * 60 * 24);
    difference_in_years = difference_in_years / (365.25);

    if (difference_in_days < 1) {
        alert("Birthday must be less than today's date")
        document.getElementById('birthday').focus()
        return;
    }
    else if (difference_in_days >= 1 && difference_in_years < 13) {
        alert("Age should be at least 13 years old")
        document.getElementById('birthday').focus()
        return;
    }

    let password = document.getElementById('password').value;
    if (password.length == 0) {
        alert('Password can not be empty');
        document.getElementById('password').focus();
        return;
    }
    else if (password.length > 0 && password.length < 8) {
        alert('Password should be less at least 8 characters long');
        document.getElementById('password').focus();
        return;
    }

    let password2 = document.getElementById('password2').value;
    if (password2.length == 0) {
        alert('Password confirmation can not be empty');
        document.getElementById('password2').focus();
        return;
    }
    else if (password2.length > 0 && password2.length < 8) {
        alert('Password confirmation should be less at least 8 characters long');
        document.getElementById('password2').focus();
        return;
    }

    if (password.length > 7 && password2.length > 7 && (password != password2)) {
        alert('Passwords do not match, please try again');
        document.getElementById('password').focus();
        return;
    }

    // if everything's correct, submit the form
    this.submit();
}

// function to validate login form fields
function validarLogin(evento) {
    evento.preventDefault();

    let email_login = document.getElementById('email_login').value;
   
    if (email_login.length == 0) {
        alert('Email address can not be empty');
        document.getElementById('email_login').focus();
        return;
    }

    let mailformat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    valid_email = mailformat.test(email_login);

    if (!valid_email) {
        alert("Email address is invalid");
        document.getElementById('email_login').focus();
        return;
    }

    let password_login = document.getElementById('password_login').value;
    if (password_login.length == 0) {
        alert('Password can not be empty');
        document.getElementById('password_login').focus();
        return;
    }
    else if (password_login.length > 0 && password_login.length < 8) {
        alert('Password should be less at least 8 characters long');
        document.getElementById('password_login').focus();
        return;
    }

    // if everything's correct, submit the form
    this.submit();
}