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

document.getElementById('save-sub-btn').addEventListener('click', async () => {
    const urlInput = document.getElementById('sub-url-input');
    const statusDiv = document.getElementById('sub-status');
    const subUrl = urlInput.value.trim();

    if (!subUrl) {
        statusDiv.className = 'status-message error';
        statusDiv.textContent = 'Пожалуйста, введите ссылку на подписку.';
        return;
    }

    statusDiv.className = 'status-message';
    statusDiv.textContent = 'Сохранение ссылки...';

    try {
        const response = await fetch('/api/update-subscription', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: subUrl })
        });
        const data = await response.json();

        if (data.status === 'success') {
            renderServers(data.servers)
            statusDiv.className = 'status-message success';
            statusDiv.textContent = 'Ссылка успешно сохранена.';
            console.log('Ссылка на подписку успешно обновлена:', data.servers);
        }
        else {
            statusDiv.className = 'status-message error';
            statusDiv.textContent = data.message || 'Произошла ошибка при сохранении ссылки.';
            console.error('Ошибка при обновлении ссылки на подписку:', data.message);
        }
    }
    catch (error) {
            statusDiv.className = 'status-message error';
            statusDiv.textContent = 'Произошла ошибка при сохранении ссылки.';
            console.error('Ошибка при обновлении ссылки на подписку:', error)}
        })

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/get-config');
        const data = await response.json();

        if(data.status === 'success' && data.config) {
            const subInput = document.getElementById('sub-url-input');
            if(subInput && data.config.sub_url) {
                subInput.value = data.config.sub_url;
            }
            if(data.config.servers && data.config.servers.length > 0) {
                renderServers(data.config.servers);
            }
        }}
    catch (error) {
            console.error('Ошибка при получении конфигурации:', error);
        }});


let availableServers = [];

function renderServers(servers) {
    availableServers = servers;
    const listContainer = document.getElementById('proxies-list');
    const countBadge = document.getElementById('proxies-count');

    if (!servers || servers.length === 0) {
        listContainer.innerHTML = '<p class="empty-message">Список серверов пуст.</p>';
        countBadge.textContent = '0';
        return;
    }

    countBadge.textContent = servers.length;
    listContainer.innerHTML = '';

    servers.forEach((server, index) => {
        const card = document.createElement('div'); card.className = 'proxy-card';
        card.innerHTML = `
        <div class="proxy-info">
            <span class="proxy-name">${server.name}</span>
            <span class="proxy-type">${server.type}</span>
        </div>
        `;
        card.addEventListener('click', () => {
            document.querySelectorAll('.proxy-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            console.log('Выбран сервер: ', server);
        })
        listContainer.appendChild(card);
    })

}