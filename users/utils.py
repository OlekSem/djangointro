import uuid

def upload_avatar(size):
    def wrapper(instance, filename):
        return f"avatars/{size}/{uuid.uuid4()}.webp"
    return wrapper