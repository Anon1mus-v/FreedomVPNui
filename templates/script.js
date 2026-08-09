const ref_btn = document.getElementById('refresh-btn');
const vpn_btn = document.getElementById('VPN-btn')
let vpn_btn_connected = false

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
    if(vpn_btn_connected) {
        fetch('/stop')
            .then(response => response.json())
            .then(data => {
                console.log('VPN остановлен: ', data);
                vpn_btn_connected = false;
                vpn_btn.querySelector('.text-btn').textContent = 'Start';
            })
            .catch(error => console.error('Ошибка:', error))
    }
    else
        fetch('/start')
            .then(response => response.json())
            .then(data => {
                console.log('VPN запущен: ', data);
                vpn_btn_connected = true;
                vpn_btn.querySelector('.text-btn').textContent = 'Stop';
            })
            .catch(error => console.error('Ошибка:', error))
})