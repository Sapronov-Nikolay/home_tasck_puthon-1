from address import Address
from mailing import Mailing

# Создаём адреса
address_from = Address(
    "111672",
    "Москва",
    "Сергея Радонежского",
    "2",
    "17"
)
address_to = Address(
    "190542",
    "Уфа",
    "Бабушкин проезд",
    "7",
    "10"
)

# Создаём Отправление, передавая адреса как объекты
maling = Mailing(
    from_address=address_from,
    to_address=address_to,
    cost=350.50,
    track="TRK11121985780"
)
# Воспроизводим результат заданию:
# Отправление <track> из <индекс>, <город>, <улица>, <дом> - <квартира>
# в <индекс>, <город>, <улица>, <дом> -<квартира>.
# Стоимость <стоимость> рублей.
print(f"Отправление {maling.track} из {maling.from_address.index}, г.{maling.from_address.city}, ул.{maling.from_address.street}, д.{maling.from_address.house}, кв.{maling.from_address.apartment} "
      f"в {maling.to_address.index} г.{maling.to_address.city} ул.{maling.to_address.street} д.{maling.to_address.house} кв.{maling.to_address.apartment}."
      f" Стоимость {maling.cost} рублей")