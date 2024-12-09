from dependency_injector import containers


class Container(containers.DeclarativeContainer):
    pass


__container = Container()


def get_di_container() -> Container:
    return __container
