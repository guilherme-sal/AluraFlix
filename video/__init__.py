from video import crud
from urllib.parse import urlparse


class Video:

    def __init__(self, video_id=None, title=None, description=None, url=None):

        self.id = video_id
        self.title = title
        self.description = description
        self.url = url
        self.valid = self._validation()
        self.crud_action = self._crud_action()

    def __repr__(self):
        return self.title

    def get_data_dict(self):
        return {'Id': self.id, 'Title': self.title, 'Description': self.description, 'Url': self.url}

    def _validate_id(self):
        if type(self.id) == int and (self.id <= 10):
            return True
        else:
            return False

    def _validate_title(self):
        if len(self.title) <= 20:
            return True
        else:
            return False

    def _validate_description(self):
        if len(self.description) <= 200:
            return True
        else:
            return False

    def _validate_url(self):
        if len(self.url) <= 30:
            try:
                url_object = urlparse(self.url)
                self.url = url_object
                return True
            except:
                return False
        else:
            return False

    def get_validation_status(self):
        return self.valid

    def _validation(self):
        return False

    def _crud_action(self):
        return False


class NewVideo(Video):

    def _validation(self):
        if self.title and self.description and self.url:
            if super()._validate_title() and super()._validate_description() and super()._validate_url():
                return True
            else:
                return False
        else:
            return False

    def _crud_action(self):
        if self.valid:
            created_video = crud.create_video(self)
            if created_video:
                return True
            else:
                return False
        else:
            return False

    def set_video_id(self):
        try:
            _id = crud.read_video_id_from_title(self)
            self.id = _id
        except:
            pass


class EditVideo(Video):

    def _validation(self):
        if self.id and super()._validate_id():
            if crud.check_id(self.id):
                if self.title:
                    if super()._validate_title():
                        return True
                    else:
                        return False
                if self.description:
                    if super()._validate_description():
                        return True
                    else:
                        return False
                if self.url:
                    if super()._validate_url():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def _crud_action(self):
        if self.valid:
            new_data = [self.id, self. title, self.description, self.url]
            old_data = crud.read_video_data(self.id)
            mixed_data = []
            counter = 0
            for data in new_data:
                if data:
                    mixed_data.append(data)
                    counter += 1
                else:
                    mixed_data.append(old_data[counter])
                    counter += 1
            self.title = mixed_data[1]
            self.description = mixed_data[2]
            self.url = mixed_data[3]
            uptaded_video = crud.update_video(self)
            if uptaded_video:
                return True
            else:
                return False
        else:
            return False


class GetVideo(Video):

    def _validation(self):
        if self.id and super()._validate_id():
            if crud.check_id(self.id):
                return True
        else:
            return False

    def _crud_action(self):
        if self.valid:
            try:
                video_data = crud.read_video_data(self.id)
                self.title = video_data[1]
                self.description = video_data[2]
                self.url = video_data[3]
                return True
            except:
                return False
        else:
            return False


class DeleteVideo(GetVideo):
    def _crud_action(self):
        if self.valid:
            try:
                video_data = crud.read_video_data(self.id)
                self.title = video_data[1]
                self.description = video_data[2]
                self.url = video_data[3]
                crud.delete_video(self.id)
                return True
            except:
                return False
        else:
            return False


