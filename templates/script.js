const ref_btn = document.getElementById('refresh-btn');
const vpn_btn = document.getElementById('VPN-btn')
const left_menu_button = document.querySelectorAll('.nav-btn')
const main_menu_block = document.querySelectorAll('.tab-content')
let vpn_btn_connected = false

left_menu_button.forEach(element => {
    element.addEventListener('click', () => {
        left_menu_button.forEach(btn => btn.classList.remove('active'))
        main_menu_block.forEach(btn => btn.classList.remove('active'))
        element.classList.add('active')
        document.getElementById('tab-' + element.dataset.tab).classList.add('active')
    }
)
});

ref_btn.addEventListener('click', () => {
    fetch('/update')
        .then(response => response.json())
        .then(data => {
            console.log('Ключи обновлены: ', data);
            if (data.status === 'no_valid_keys') {
                alert(data.message || 'Нет валидных ключей');
            }
        })
        .catch(error => {
            console.error("Ошибка обновления:", error);
        }
        )
})

vpn_btn.addEventListener('click', () => {
    vpn_btn_connected = !vpn_btn_connected;
    if(vpn_btn_connected) {
        vpn_btn.classList.remove('disconnected')
        vpn_btn.classList.add('connected')
        fetch('/start')
            .then(response => response.json())
            .then(data => {
                console.log('VPN запущен: ', data);
                vpn_btn_connected = true;
            })
            .catch(error => console.error('Ошибка:', error))
    }
    else
        vpn_btn.classList.remove('connected')
        vpn_btn.classList.add('disconnected')
        fetch('/stop')
            .then(response => response.json())
            .then(data => {
                console.log('VPN остановлен: ', data);
                vpn_btn_connected = false;
            })
            .catch(error => console.error('Ошибка:', error))
})