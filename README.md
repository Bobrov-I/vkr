## <div align="center">Краткое описание📑</div>
<p>
  Django проект, который представляет из себя сервис для отправки заявок о несанкционированных свалках с использованием обученных моделей ИИ.
  В сценарии использования сервиса модели выполняют роли детектора, сегментатора и классификатора как куч мусора, так и отдельной фракции, тем самым упрощая работу Администрации сайта с       обработкой заявок от пользователей.
</p>
<p>
Для детекции и сегментации куч мусора использовались две модели YOLOv8n.
Для классификации опасной и не опасной фракции использовалась модель DenseNet121.
</p>
<p>
Помимо этого в сервисе присутствуют библиотеки предоставляющие и представляющие геоинформационные данные, они используются для автозаполнения адреса и для отображения маркеров свалок на карте. 
</p>
