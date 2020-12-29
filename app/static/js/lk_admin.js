//берём данные
let marks = document.querySelectorAll('.mark')
let counts = document.querySelectorAll('.count')
let columnContent = document.querySelectorAll('.column-content')

//Находим график, задаём контекст
let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');

//Отрисовываем оси
ctx.fillStyle = "black"; // Задаём чёрный цвет для линий
ctx.lineWidth = 2.0; // Ширина линии
ctx.beginPath(); // Запускает путь
ctx.moveTo(30, 10); // Указываем начальный путь
ctx.lineTo(30, 460); // Перемешаем указатель
ctx.lineTo(500, 460); // Ещё раз перемешаем указатель
ctx.stroke(); // Делаем контур


let maxValue = 0;
counts.forEach(item => {
    maxValue = (+item.innerHTML > maxValue)  ? item.innerHTML : maxValue
})

let dy= (Math.ceil(maxValue*0.1)*10)/5
//Выводим метки
// Цвет для рисования
ctx.font = '14px serif'
ctx.fillStyle = "black";
// Цикл для отображения значений по Y
for(let i = 0; i < 6; i++) {

    ctx.fillText((5 - i) * dy + "", 4, i * 80 + 60);
    ctx.beginPath();
    ctx.moveTo(25, i * 80 + 60);
    ctx.lineTo(30, i * 80 + 60);
    ctx.stroke();
}


// Массив с метками машин
let labels = []
marks.forEach((item, index) => labels[index] = item.innerHTML)


// Выводим меток
for(var i=0; i<labels.length; i++) {
    ctx.fillText(labels[i], 50+ i*100, 475);
}

//рисуем результат
// Объявляем массив данных графика
let data = [ ];
counts.forEach((item, index) => data[index] = item.innerHTML)


// Назначаем зелёный цвет для графика
let colors = ['blue', 'yellow', 'green', 'red']
// Цикл для от рисовки графиков
for(var i=0; i< data.length; i++) {
    ctx.fillStyle = colors[i]
    var dp = data[i]*dy;
    ctx.fillRect(40 + i*100, 460-dp*5 , 50, dp*5);
}

document.querySelector('.btnSignOut').addEventListener('click', function () {
    document.location.href = 'http://localhost:5000'
})

columnContent.forEach(item => item.addEventListener('click', updatePage(item.getAttribute('id'))))

function updatePage (id) {
    return function () {
        if (id === '1') {
            document.location.href = 'http://localhost:5000/admin_lk/'
        }
        if (id === '2') {
            document.querySelector('.container').innerHTML = ''
            document.querySelector('.container').insertAdjacentHTML('beforeend', `
            <div class="header">
                        <h1>Заработок</h1>
                        <button class="btnSignOut">Выход</button>
            </div>     
            `)
        }
        if (id === '3') {
            document.querySelector('.container').innerHTML = ''
            document.querySelector('.container').insertAdjacentHTML('beforeend', `
            <div class="header">
                        <h1>Все заявки</h1>
                        <button class="btnSignOut">Выход</button>
            </div>     
            `)
        }
    }
}