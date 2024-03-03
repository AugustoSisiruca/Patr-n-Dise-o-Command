from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    """
    La interfaz Command declara un método para ejecutar un comando.
    """

    @abstractmethod
    def execute(self) -> None:
        pass


class SimpleCommand(Command):
    """
   Algunos comandos pueden implementar operaciones simples por sí solos.
    """

    def __init__(self, payload: str) -> None:
        self._payload = payload

    def execute(self) -> None:
        print(f"SimpleCommand: Mira, puedo hacer cosas simples como imprimir"
              f"({self._payload})")


class ComplexCommand(Command):
    """
    Sin embargo, algunos comandos pueden delegar operaciones más complejas a otros.
    objetos, llamados "receivers".
    """

    def __init__(self, receiver: Receiver, a: str, b: str) -> None:
        """
    Los comandos complejos pueden aceptar uno o varios objetos receptores junto con
    cualquier dato de contexto a través del constructor.
        """

        self._receiver = receiver
        self._a = a
        self._b = b

    def execute(self) -> None:
        """
        Los comandos pueden delegar a cualquier método de un receptor.
        """

        print("ComplexCommand: Las cosas complejas deben ser realizadas por un objeto receptor", end="")
        self._receiver.do_something(self._a)
        self._receiver.do_something_else(self._b)


class Receiver:
    """
    Las clases de Receiver contienen cierta lógica empresarial importante.
    Saben realizar todo tipo de operaciones asociadas a la realización de una solicitud.
    De hecho, cualquier clase puede actuar como Receiver.
    """

    def do_something(self, a: str) -> None:
        print(f"\nReceiver: Working on ({a}.)", end="")

    def do_something_else(self, b: str) -> None:
        print(f"\nReceiver: Also working on ({b}.)", end="")


class Invoker:
    """
    El Invoker está asociado a uno o varios comandos. 
    Este envía una solicitud al comando.
    """

    _on_start = None
    _on_finish = None

    """
    Inicializar comando.
    """

    def set_on_start(self, command: Command):
        self._on_start = command

    def set_on_finish(self, command: Command):
        self._on_finish = command

    def do_something_important(self) -> None:
        """
        El Invoker no depende de clases concretas de comando o receiver.
        El Invoker pasa una solicitud a un receiver indirectamente, ejecutando un
        comando.
        """

        print("Invoker: ¿Alguien quiere que se haga algo antes de comenzar?")
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        print("Invoker: ...haciendo algo realmente importante...")

        print("Invoker: ¿Alguien quiere que se haga algo después de que termine?")
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()


if __name__ == "__main__":
    """
    El código del cliente puede parametrizar un invocador con cualquier comando.
    """

    invoker = Invoker()
    invoker.set_on_start(SimpleCommand("Di hola!"))
    receiver = Receiver()
    invoker.set_on_finish(ComplexCommand(
        receiver, "Envia un email", "Guarda un reporte"))

    invoker.do_something_important()


"""
Output.txt: Resultado de la ejecución
Invoker: ¿Alguien quiere que se haga algo antes de comenzar?
SimpleCommand: Mira, puedo hacer cosas simples como imprimir (Di Hola!)
Invoker: ...haciendo algo realmente importante...
Invoker: ¿Alguien quiere que se haga algo después de que termine?
ComplexCommand: Las cosas complejas deben ser realizadas por un objeto receptor
Receiver: Working on (Envia un email.)
Receiver: Also working on (Guarda un reporte.)
"""