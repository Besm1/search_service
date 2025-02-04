class DefaultRouter:
    """
    Маршрутизатор для основной базы данных (default).
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'search':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'search':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label == 'search' or
                obj2._meta.app_label == 'search'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'search':
            return db == 'default'
        return None


class ProfileRouter:
    """
    Маршрутизатор для базы данных профиля (prof).
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'prof':
            return 'prof'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'prof':
            return 'prof'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label == 'prof' or
                obj2._meta.app_label == 'prof'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'prof':
            return db == 'prof'
        return None