document.addEventListener('DOMContentLoaded', () => {
    const bell = document.getElementById('notif-bell');
    const modal = document.getElementById('notificationModal');
    const closeBtn = document.getElementById('closeModal');
    const badge = document.querySelector('.badge');
    const notificationsList = document.getElementById('notificationsList');
    const profileLink = document.getElementById('profileLink');
    const dropdown = document.getElementById('profileDropdown');
    const bookEvent = document.getElementById('bookEvent');

    if (bookEvent) {
        // Функция для обработки статуса и создания модалки
        function showMessageStatus(message, status) {
            const notification = document.getElementById('status-message');
            notification.innerText = message;

            if (status === 'success' || status === 'already_booked') {
                notification.style.backgroundColor = 'green';
            } else if (status === 'error') {
                notification.style.backgroundColor = '#c92626';
            } else {
                notification.style.backgroundColor = '#444';
            }

            notification.style.display = 'block';

            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }

    // fetch запрос на бронирование мероприятия
        bookEvent.addEventListener('click', function(e) {
            e.preventDefault(); // отменим-ка базовую отправку формы, чтобы сисрф токен смогли передать
            eventId = this.dataset.eventId
            fetch(`/events/booking/${eventId}/`, {
                "method": "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            })

            .then(response => response.json())
            .then(data => {
                showMessageStatus(data.message, data.status)
//                console.log(data);
            })
        });
    }

    if (bell) {
        // Открытие модального по клику
        bell.addEventListener('click', () => {
            console.log("TRue")
            modal.style.display = 'flex';
        });

        // Функция добавления уведомлений в модальное окно
        function addNotification(message) {
            const div = document.createElement('div');
            div.className = 'modal__item'
            div.style.padding = '10px';
            div.style.borderBottom = '1px solid #ccc';
            let messageDate = `<span>${String(new Date(message.created_at).toLocaleDateString())}</span>`
            div.innerHTML = message.message + messageDate;

            if (notificationsList) {
                notificationsList.appendChild(div)
            }

            if (message.is_read == true) {
                badge.style.display = "none";
            }
        }

        // fetch запрос на сервер для получения уведомлений
        bell.addEventListener("click", () => {
            fetch("/users/get_messages/")
                .then(response => response.json())
                .then(data => {
                    data.messages.forEach(message => {
                        addNotification(message);
                    })
                })
        })

        // Закрытие модального
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                notificationsList.innerHTML = ''
                modal.style.display = 'none';
            });
        }

        // Закрытие по клику вне модального контента
        window.addEventListener('click', (e) => {
          if (e.target === modal) {
            notificationsList.innerHTML = ''
            modal.style.display = 'none';
          }
        });
    }

    //
    profileLink.addEventListener('click', function(e) {
        e.preventDefault();
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });

    //
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.profile-menu-wrapper')) {
            dropdown.style.display = 'none';
        }
    });
});
