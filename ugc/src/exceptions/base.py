class NotFoundError(Exception):
    entity_name: str

    def __init__(self, object_id):
        super().__init__(f'{self.entity_name} not found, object: {object_id}')


class NotModifiedError(Exception):
    entity_name: str

    def __init__(self, object_id):
        super().__init__(f'{self.entity_name} not modified, object: {object_id}')


class AlreadyExistsError(Exception):
    entity_name: str

    def __init__(self, object_id):
        super().__init__(f'{self.entity_name} already exists, object: {object_id}')
