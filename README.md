# WELBEX - тестовое задание #

## Дымников Михаил ##

----------------------------------

# Документация для API #

В API доступны POST и GET запросы. Сервер возвращает ответ в формате JSON.<br>
Пример обращения к API (получение груза по ID) с помощью python requests, если сервер запущен на Вашем компьютере:

```python
import requests

resp = requests.get('http://localhost:8000/api/cargo')
print(resp.json())

```
Ответ:

```json
{'2': {'pick-up': 610, 'delivery': 611, 'wight': 1, 'description': 'gaefgeafg', 'nearest_cars': {'2': 11.416862577989889}}, 'status': 'success', 'errors': []}
```

Пример отправки данных (добавление груза):
```python
import requests

data = {'pick_up_location': 610,
        'delivery_location': 611,
        'weight': 10,
        'description': 'Описание груза'}
resp = requests.post('http://localhost:8000/api/new_cargo/', data=data)
print(resp.json())
```

Ответ:
```json
{
  'status': 'success',
  'errors': []
}
```

----------------------------------

## Груз ##

### Получить список груза - /api/cargo ###

### Получить груз по ID - /api/cargo_info/ID ###

### Удалить груз по ID - /api/cargo_delete/ID ###

### Добавить груз - /api/new_cargo ###
Необходимые данные: pick_up_location, delivery_location, weight, description

### Изменить данные груза - /api/edit_cargo ###
Можно менять: weight, description

----------------------------------

## Машины ##

### Получить список машин - /api/cars ###

### Получить машину по ID - /api/car_info/ID ###

### Удалить машину по ID - /api/car_delete/ID ###

### Добавить машину - /api/new_car ###
Необходимые данные: number, location, weight

### Изменить данные машины - /api/edit_car ###
Можно менять: location, weight

----------------------------------

## Локации ##

### Получить список локаций - /api/locations ###

### Получить локацию по ID - /api/location_info/ID ###

### Удалить локацию по ID - /api/locations_delete/ID ###

### Добавить локацию - /api/new_locations ###
Необходимые данные: city, state, postal code (zip), latitude, longitude

### Изменить данные локации - /api/edit_locations ###
Можно менять: city, state, postal code (zip), latitude, longitude

----------------------------------

## Поиск /api/search ##
Необходимые данные: object_type (cargo/car/location), query (ID/number/zip)<br>
Ответ: переадресация на cargo_info/ID или car_info/ID или location_info/ID



----------------------------------
Май 2023