from flask import Flask
from flask_restful import Resource, Api, reqparse
import configparser
from video import NewVideo, EditVideo, GetVideo, DeleteVideo
from video.crud import read_all_ids

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, default=None)
parser.add_argument('title', type=str, default=None)
parser.add_argument('description', type=str, default=None)
parser.add_argument('url', type=str, default=None)


class AllVideos(Resource):

    def get(self):
        video_ids = read_all_ids()
        video_dict = {}
        for video_id in video_ids:
            get_video = GetVideo(video_id=video_id)
            if get_video.valid and get_video.crud_action:
                video_dict[get_video.id] = get_video.get_data_dict()
        if video_dict:
            return {'Code': 200, 'Alert': 'Success', 'Data': video_dict}
        else:
            return {'Code': 400, 'Alert': 'Database is empty.'}


class Videos(Resource):

    def get(self, video_id):
        get_video = GetVideo(video_id=video_id)
        if get_video.valid and get_video.crud_action:
            return {'Code': 200, 'Alert': 'Success', 'Data': get_video.get_data_dict()}
        else:
            return {'Code': 400, 'Alert': 'Please, verify video parameters'}

    def delete(self, video_id):
        delete_video = DeleteVideo(video_id=video_id)
        if delete_video.valid and delete_video.crud_action:
            return {'Code': 200, 'Alert': 'Success', 'Data': delete_video.get_data_dict()}
        else:
            return {'Code': 400, 'Alert': 'Please, verify video parameters'}


class PostVideo(Resource):

    def __init__(self):
        args = parser.parse_args()
        self.title = args.get('title')
        self.description = args.get('description')
        self.url = args.get('url')

    def post(self):
        new_video = NewVideo(video_id=None, title=self.title, description=self.description, url=self.url)
        new_video.set_video_id()
        if new_video.valid and new_video.crud_action:
            return {'Code': 200, 'Alert': 'Success', 'Data': new_video.get_data_dict()}
        else:
            return {'Code': 400, 'Alert': 'Please, verify video parameters'}


class PutVideo(Resource):

    def __init__(self):
        args = parser.parse_args()
        self.id = args.get('id')
        self.title = args.get('title', None)
        self.description = args.get('description', None)
        self.url = args.get('url', None)

    def put(self):
        edit_video = EditVideo(video_id=self.id, title=self.title, description=self.description, url=self.url)
        if edit_video.valid and edit_video.crud_action:
            return {'Code': 200, 'Alert': 'Success', 'Data': edit_video.get_data_dict()}

        else:
            return {'Code': 400, 'Alert': 'Please verify video parameters.'}


endpoints = configparser.ConfigParser()
endpoints.read('api_endpoints.txt')

api.add_resource(AllVideos, endpoints['ENDPOINTS']['all_videos'])
api.add_resource(Videos, endpoints['ENDPOINTS']['video'] + '/<int:video_id>')
api.add_resource(PostVideo, endpoints['ENDPOINTS']['post_video'])
api.add_resource(PutVideo, endpoints['ENDPOINTS']['put_video'])

if __name__ == '__main__':
    app.run(debug=True)
