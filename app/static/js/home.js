'use strict'

//Ставим прослушивание событий на кнопки на главной странице
document.querySelector('.btnSignIn').addEventListener('click', wrapOpenPopup('clickClient'))
document.querySelector('.content-btn__recording').addEventListener('click', wrapOpenPopup('NewRecord'))


//исправляем баг появления всплывающего окна
window.onload =  function() {
    document.querySelector('.popup').style.display = 'block'
}

//Прослушивание событий внутри всплывающего окна
if (document.querySelector('.popup').classList.contains('open'))
{
    if (document.querySelector('.popup_tabs')) {
        document.querySelector('.tab-client').addEventListener('click', resetPopup('clickClient'))
        document.querySelector('.tab-client').classList.remove('active')
        document.querySelector('.tab-manager').classList.add('active')
    }
    document.querySelector('.popup-close').addEventListener('click', closePopup)
    document.querySelector('.popup').addEventListener('click', function(e) {
        if (!e.target.closest('.popup_content') && !e.target.closest('.popup_tabs')) {
            closePopup()
        }
    })
}

//Перерисовка всплывающего окна
function resetPopup(str) {
    return function () {
        if (str === 'clickManager') //если кликнули на менеджера
        {
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
        if (str === 'clickClient') //если кликнули на клиента
        {
            let popup = document.querySelector('.popup_content')
            popup.innerHTML = ''
            popup.insertAdjacentHTML('beforeend', `
            <form action="login_client" method="POST">
                <p class="popup-close"></p>
                <div class="popup_tabs">
                    <p class="tab-client active">Клиент</p>
                    <p class="tab-manager">Менеджер</p>
                </div>
                <p class="popup_label">Введите номер телефона:</p>
                <input type="text" class="popup-input" id="phone" name="phone_number" placeholder="+7 (___) ___-__-__">
                <div class="btn-wrap">
                    <button class="popup-button" type="submit">Продолжить</button>
                </div>
            </form>
            `)
            jQuery(function($){
                $("#phone").mask("+7 (999) 999-99-99");
            });
            document.querySelector('.tab-manager').classList.remove('active')
            document.querySelector('.tab-client').classList.add('active')
            document.querySelector('.popup-close').addEventListener('click', closePopup)
            document.querySelector('.tab-manager').addEventListener('click', resetPopup('clickManager'))
        }
        if (str === 'NewRecord') //если кликнули записаться
        {
            let popup = document.querySelector('.popup_content')
            popup.innerHTML = ''
            popup.insertAdjacentHTML('beforeend', `   
                   <form action="new_record" method="POST">
                        <p class="popup-close"></p>
                        <p class="popup_label">Введите номер телефона:</p>
                        <input class="popup-input" name="phone_number" id="phone" type="tel"  placeholder="+7 (___) ___-__-__">
                        <p class="popup_label">Выберете марку авто:</p>
                        <select class="popup-list marks" name="Trademark">                                    
                        </select>
                        <p class="popup_label">Выберете тип услуги:</p>
                        <select class="popup-list services" name="About">
                        </select>
                        <div class="btn-wrap">
                            <button class="button popup-button" name="button" value="go to amount">Продолжить</button>
                        </div>
                   </form>`)
            jQuery(function($){
                $("#phone").mask("+7 (999) 999-99-99");
            });
            document.querySelector('.popup-close').addEventListener('click', closePopup)
            fetch('http://localhost:5000/new_record')
                .then(response => response.json())
                .then(result =>  {
                    result.trademark_list.forEach(mark => {
                        document.querySelector('.marks').insertAdjacentHTML('beforeend', `
                            <option value="${mark}">${mark}</option>
                        `)
                    })
                    result.about_list.forEach(service => {
                        document.querySelector('.services').insertAdjacentHTML('beforeend', `
                            <option value="${service}">${service}</option>
                        `)
                    })
                })
        }
    }
}

function wrapOpenPopup(str) {
    return function openPopup() {
        document.querySelector('.popup').classList.add('open')
        resetPopup(str)()
        document.querySelector('.popup').addEventListener('click', function(e) {
            if (!e.target.closest('.popup_content') && !e.target.closest('.popup_tabs')) {
                closePopup()
            }
        })
    }
}

function closePopup() {
    document.querySelector('.popup').classList.remove('open')
}