from smartphone import Smartphone

catalog = []

catalog.append(Smartphone("Samsung", "Galaxy S50", "+79261118954"))
catalog.append(Smartphone("Apple", "iPhone 17 Pro", "+79067848914"))
catalog.append(Smartphone("Xiaomi", "Redmi Note 10S", "+79258956835"))
catalog.append(Smartphone("Google", "Pixel 8 Pro", "+79257012041"))
catalog.append(Smartphone("Nokia", "XR2101", "+79268757880"))

for phone in catalog:
    print(f"{phone.brand}, {phone.model}, {phone.phone_number}")
