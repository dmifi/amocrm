## Back-end сервиса по работе с API AmoCRM

### **Функционал:**
Реализован метод, который принимает GET запрос с обязательными параметрами:

- name **TEXT** - ФИО клиента;
- email **TEXT** - Email почта;
- phone **TEXT** - Номер телефона.

Используя эти данные, находится контакт в AmoCRM с данной почтой и(или)
телефоном. Если такого нет, создается новый, заполняя имя, телефон и почту
входными данными. Если найден, обновляется. После этого, создается сделка по
данному контакту в первом статусе воронки.
