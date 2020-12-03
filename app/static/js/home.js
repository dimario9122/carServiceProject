'use strict'

jQuery(function($){
    $("#phone").mask("+7 (999) 999-99-99");
});

document.querySelector('.btnSignIn').addEventListener('click', openPopup)

window.onload =  function() {
    document.querySelector('.popup').style.display = 'block'
}

if (document.querySelector('.popup').classList.contains('open'))
{
    if (document.querySelector('.popup_tabs')) {
        document.querySelector('.tab-client').classList.remove('active')
        document.querySelector('.tab-manager').classList.add('active')
    }
    document.querySelector('.popup-close').addEventListener('click', closePopup)
    document.querySelector('.tab-client').addEventListener('click', resetPopup('clickClient'))
    document.querySelector('.popup').addEventListener('click', function(e) {
        if (!e.target.closest('.popup_content') && !e.target.closest('.popup_tabs')) {
            closePopup()
        }
    })
}

function resetPopup(str) {
    return function () {
        if (str === 'clickManager') {
            let popup = document.querySelector('.popup_content')
            popup.innerHTML = ''
            popup.insertAdjacentHTML('beforeend', `   
            <form action="login" method="POST">
                <p class="popup-close"></p>
                <div class="popup_tabs">
                    <p class="tab-client active">Клиент</p>
                    <p class="tab-manager">Менеджер</p>
                </div>
                <p class="popup_label">Введите логин:</p>
                <input type="text" class="popup-input" name="username">
                <p class="popup_label">Введите пароль:</p>
                <input type="password" class="popup-input" name="password">
                <div class="btn-wrap">
                    <button class="popup-button" type="submit">Продолжить</button>
                </div>
            </form>
            `)
            document.querySelector('.tab-client').classList.remove('active')
            document.querySelector('.tab-manager').classList.add('active')
            document.querySelector('.popup-close').addEventListener('click', closePopup)
            document.querySelector('.tab-client').addEventListener('click', resetPopup('clickClient'))
        }
        if (str === 'clickClient')
        {
            let popup = document.querySelector('.popup_content')
            popup.innerHTML = ''
            popup.insertAdjacentHTML('beforeend', `
             <p class="popup-close"></p>
            <div class="popup_tabs">
                <p class="tab-client active">Клиент</p>
                <p class="tab-manager">Менеджер</p>
            </div>
            <p class="popup_label">Введите номер телефона:</p>
            <input type="text" class="popup-input" id="phone" placeholder="+7 (___) ___-__-__">
            <div class="btn-wrap">
                <button class="popup-button">Продолжить</button>
            </div>
            `)
            document.querySelector('.tab-manager').classList.remove('active')
            document.querySelector('.tab-client').classList.add('active')
            document.querySelector('.popup-close').addEventListener('click', closePopup)
            document.querySelector('.tab-manager').addEventListener('click', resetPopup('clickManager'))
        }
    }
}

function openPopup() {
    document.querySelector('.popup').classList.add('open')
    resetPopup('clickClient')()
    document.querySelector('.popup').addEventListener('click', function(e) {
        if (!e.target.closest('.popup_content') && !e.target.closest('.popup_tabs')) {
            closePopup()
        }
    })
}

function closePopup() {
    document.querySelector('.popup').classList.remove('open')
}