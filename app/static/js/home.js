'use strict'

jQuery(function($){
    $("#phone").mask("+7 (999) 999-99-99");
});

document.querySelector('.btnSignIn').addEventListener('click', openPopup)
document.querySelector('.tab-manager').addEventListener('click', resetPopup('clickManager'))
document.querySelector('.tab-client').addEventListener('click', resetPopup('clickClient'))
document.querySelector('.popup-close').addEventListener('click', closePopup)

window.onload =  function() {
    document.querySelector('.popup').style.display = 'block'
}

function resetPopup(str) {
    return function () {
        if (str === 'clickManager') {
            document.querySelector('.tab-client').classList.remove('active')
            document.querySelector('.tab-manager').classList.add('active')
        }
        if (str === 'clickClient')
        {
            document.querySelector('.tab-manager').classList.remove('active')
            document.querySelector('.tab-client').classList.add('active')
        }
    }
}

function openPopup() {
    document.querySelector('.popup').classList.add('open')
    document.querySelector('.popup').addEventListener('click', function(e) {
        if (!e.target.closest('.popup_content')) {
            closePopup()
        }
    })
}

function closePopup() {
    document.querySelector('.popup').classList.remove('open')
}