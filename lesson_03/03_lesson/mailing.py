from address import Address
"""
    Класс Mailing описывает поля почтового отправления
    Имена полей:
        - to_address: адрес получателя (объект класса Address)
        - from_address: адрес отправителя (объект того же класса Address)
        - cost: стоимость или расходы на отправку (числовое значение)
        - track: трек-номер (строковое значение)
"""
class Mailing:
    def __init__(self, to_address, from_address, cost, track):
        self.to_address = to_address
        self.from_address = from_address
        self.cost = cost
        self.track = track