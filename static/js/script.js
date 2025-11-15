document.addEventListener('DOMContentLoaded', () => {
    const bell = document.getElementById('notif-bell');
    const modal = document.getElementById('notificationModal');
    const closeBtn = document.getElementById('closeModal');
    const badge = document.querySelector('.badge');
    const notificationsList = document.getElementById('notificationsList');

    // Закрытие модального
    closeBtn.addEventListener('click', () => {
      notificationsList.innerHTML = ''
      modal.style.display = 'none';
    });

    // Закрытие по клику вне модального контента
    window.addEventListener('click', (e) => {
      if (e.target === modal) {
        notificationsList.innerHTML = ''
        modal.style.display = 'none';
      }
    });

    if (bell) {
        // Открытие модального по клику
        bell.addEventListener('click', () => {
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
            console.log(message.message)

            if (notificationsList) {
                notificationsList.appendChild(div)
            }

            if (message.is_read == true) {
                console.log(message.is_read)
                badge.style.display = "none";
            }
        }

        // fetch запрос на сервер
        bell.addEventListener("click", () => {
            fetch("/users/get_messages/")
                .then(response => response.json())
                .then(data => {
                    data.messages.forEach(message => {
                        addNotification(message);
                    })
                })
        })
    }
  });

//                  {% for message in request.user.user_messages.all %}
//                    {{message.message|safe}}
//                    {{message.created_at|date:"d.m.y"}}
//                {% endfor %}