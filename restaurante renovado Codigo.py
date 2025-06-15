import json
from collections import deque, namedtuple

MenuItemData = namedtuple("MenuItemData", ["name", "price", "type"])  


class MenuItem:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

class MainCourse(MenuItem):
    pass

class Beverage(MenuItem):
    pass

class Dessert(MenuItem):
    pass

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_total_price(self):
        total = 0
        has_main_course = any(isinstance(item, MainCourse) for item in self.items)
        for item in self.items:
            if isinstance(item, Beverage) and has_main_course:
                total += item.get_price() * 0.9
            else:
                total += item.get_price()
        return total

    def show_order(self):
        print("\nPedido actual:")
        for item in self.items:
            print(f"- {item.get_name()} : ${item.get_price():.2f}")
        print(f"Total hasta ahora: ${self.calculate_total_price():.2f}\n")

class Payment:
    def __init__(self, order, payment_method):
        self.order = order
        self.payment_method = payment_method

    def process_payment(self):
        total_price = self.order.calculate_total_price()
        print(f"\nPago de ${total_price:.2f} realizado con {self.payment_method}. ¡Gracias por tu compra!\n")

class MenuManager:
    def __init__(self, filename="menu.json"):
        self.filename = filename
        self.menu = self.load_menu()

    def load_menu(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_menu(self):
        with open(self.filename, "w") as f:
            json.dump(self.menu, f, indent=4)

    def create_item(self, name, price, item_type):
        self.menu[name] = {"price": price, "type": item_type}
        self.save_menu()

    def update_item(self, name, new_price=None, new_type=None):
        if name in self.menu:
            if new_price is not None:
                self.menu[name]["price"] = new_price
            if new_type is not None:
                self.menu[name]["type"] = new_type
            self.save_menu()

    def delete_item(self, name):
        if name in self.menu:
            del self.menu[name]
            self.save_menu()

    def list_menu(self):
        print("\n--- MENÚ ACTUAL ---")
        for i, (name, data) in enumerate(self.menu.items(), 1):
            print(f"{i}. {name} (${data['price']}) [{data['type']}]")

    def get_item_by_number(self, number):
        items = list(self.menu.items())
        if 0 < number <= len(items):
            name, data = items[number - 1]
            return MenuItemData(name, data["price"], data["type"])
        return None

if __name__ == "__main__":
    orders_queue = deque()
    menu_manager = MenuManager()

    print("Bienvenido al sistema de pedidos")

    while True:
        print("\n1. Ver menú\n2. Agregar ítem al menú\n3. Editar ítem\n4. Eliminar ítem")
        print("5. Crear nueva orden\n6. Atender próxima orden\n7. Salir")

        op = input("Elige una opción: ")

        if op == "1":
            menu_manager.list_menu()

        elif op == "2":
            name = input("Nombre del ítem: ")
            price = float(input("Precio: "))
            item_type = input("Tipo (MainCourse / Beverage / Dessert): ")
            menu_manager.create_item(name, price, item_type)

        elif op == "3":
            name = input("Nombre del ítem a editar: ")
            new_price = input("Nuevo precio (deja vacío si no cambia): ")
            new_type = input("Nuevo tipo (deja vacío si no cambia): ")
            menu_manager.update_item(
                name,
                float(new_price) if new_price else None,
                new_type if new_type else None,
            )

        elif op == "4":
            name = input("Nombre del ítem a eliminar: ")
            menu_manager.delete_item(name)

        elif op == "5":
            order = Order()
            while True:
                menu_manager.list_menu()
                choice = input("Número del ítem a agregar (0 para terminar): ")
                if choice == "0":
                    break
                item_data = menu_manager.get_item_by_number(int(choice))
                if item_data:
                    if item_data.type == "MainCourse":
                        order.add_item(MainCourse(item_data.name, item_data.price))
                    elif item_data.type == "Beverage":
                        order.add_item(Beverage(item_data.name, item_data.price))
                    elif item_data.type == "Dessert":
                        order.add_item(Dessert(item_data.name, item_data.price))
                else:
                    print("Opción inválida.")

            orders_queue.append(order)
            print("Orden agregada a la cola.\n")

        elif op == "6":
            if orders_queue:
                next_order = orders_queue.popleft()
                next_order.show_order()
                metodo = input("Método de pago (Tarjeta / Efectivo): ")
                Payment(next_order, metodo).process_payment()
            else:
                print("No hay órdenes pendientes.")

        elif op == "7":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida.")
