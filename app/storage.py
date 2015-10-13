class StorageException(Exception):
    pass

class Storage(object):
    def __init__(self):
        self._init_django()

    def get_all_recordings(self):
        from home.models import get_recordings

        return list(get_recordings())

    def get_all_photos(self):
        from home.models import get_photos

        return list(get_photos())

    def get_all_movements(self):
        from home.models import get_movements

        return list(get_movements())

    def delete_recording(self, name):
        from webcam import settings

        try:
            self._delete(settings.STATICFILES_DIRS[0], name)
        except StorageException:
            pass
        else:
            self._remove_recording_from_database(name)

    def delete_photo(self, name, thumbnail):
        from webcam import settings

        try:
            self._delete(settings.STATICFILES_DIRS[1], name)
            self._delete(settings.STATICFILES_DIRS[1], thumbnail)
        except StorageException:
            pass
        else:
            self._remove_photo_from_database(name)

    def delete_movement(self, movement):
        self._remove_movement_from_database(movement)

    def save_photo(self, photo):
        import photo as photo_

        try:
            self._save_photo(photo)
        except photo_.PhotoException as error:
            raise StorageException(str(error))

        self._add_photo_to_database(photo)

    def save_recording(self, recording, photo):
        import recording as recording_

        try:
            self._save_recording(recording)
        except recording_.RecordingException as error:
            raise StorageException(str(error))

        self._add_recording_to_database(recording, photo)

    def save_motion(self, recording, photo):
        self._add_motion_to_database(recording, photo)

    def _delete(self, root, name):
        import os

        path = os.path.join(root, name)
        if os.path.isfile(path):
            try:
                os.unlink(path)
            except OSError as error:
                print "Cannot delete: " + path + " Error: " + str(error)
                raise StorageException(error)

    def _remove_recording_from_database(self, name):
        from home.models import remove_recording

        remove_recording(name)

    def _remove_photo_from_database(self, name):
        from home.models import remove_photo

        remove_photo(name)

    def _remove_movement_from_database(self, name):
        from home.models import remove_movement

        remove_movement(name)

    def _save_recording(self, recording):
        from webcam import settings

        recording.save(settings.STATICFILES_DIRS[0])

    def _save_photo(self, photo):
        from webcam import settings

        photo.save(settings.STATICFILES_DIRS[1])

    def _add_recording_to_database(self, recording, photo):
        from home.models import add_recording

        add_recording(recording.name, recording.time, recording.lenght, photo.name)

    def _add_photo_to_database(self, photo):
        from home.models import add_photo

        add_photo(photo.name, photo.thumbnail, photo.time)

    def _add_motion_to_database(self, recording, photo):
        from home.models import add_movement

        add_movement(photo.time, recording.name, photo.name)

    def _init_django(self):
        from os import environ
        from os.path import join, dirname, abspath
        import sys
        import django

        environ['DJANGO_SETTINGS_MODULE'] = 'webcam.settings'
        sys.path.append(join(dirname(dirname(abspath(__file__))), "web"))
        django.setup()