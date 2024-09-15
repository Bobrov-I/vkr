document.getElementById('reqestion').addEventListener('submit', function(event) {
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;
    var description = document.getElementById('description').value;
    var address = document.getElementById('address').value;
    var photos = document.getElementById('photos').files;
    var latitude = document.getElementById('latitude').value.trim();
    var longitude = document.getElementById('longitude').value.trim();
    var nameRegex = /^[А-Яа-я ]+$/;
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var phoneRegex = /^(\+7|8)[ ]?(\d{3})[ ]?(\d{3})[-]?(\d{2})[-]?(\d{2})$/;

    if (!name.match(nameRegex)) {
        document.getElementById('name-error').innerText = 'Имя должно состоять только из кириллических символов';
        event.preventDefault();
    } else {
        document.getElementById('name-error').innerText = '';
    }

    if (!email.match(emailRegex)) {
        document.getElementById('email-error').innerText = 'Некорректный формат email-адреса';
        event.preventDefault();
    } else {
        document.getElementById('email-error').innerText = '';
    }

    if (!phone.match(phoneRegex)) {
        document.getElementById('phone-error').innerText = 'Пожалуйста, введите корректный номер, в формате "+71234567890" или "81234567890"';
        event.preventDefault();
    } else {
        document.getElementById('phone-error').innerText = '';
    }
    if (description.trim() === '') {
    document.getElementById('description-error').innerText = 'Поле "Описание места" не должно быть пустым';
    event.preventDefault();
    } else {
        document.getElementById('description-error').innerText = '';
    }

    if (address.trim() === '') {
        document.getElementById('address-error').innerText = 'Поле "Адрес свалки" не должно быть пустым';
        event.preventDefault();
    } else {
        document.getElementById('address-error').innerText = '';
    }

    if (photos.length === 0) {
        document.getElementById('photos-error').innerText = 'Пожалуйста, прикрепите хотя бы одно фото';
        event.preventDefault();
    } else {
        document.getElementById('photos-error').innerText = '';
    }
    if (latitude.length === 0 || longitude.length === 0) {
        document.getElementById('address-error').innerText = 'Укажите более подробный адрес';
        event.preventDefault();
    } else {
        document.getElementById('address-error').innerText = '';
    }
});