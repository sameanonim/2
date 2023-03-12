import os
import json
import pytest
from second import Channel, Video, PLVideo

class TestChannel:

    def setup_class(cls):
        cls.channel = Channel('UC_x5XG1OV2P6uZZ5FSM9Ttw')

    def test_channel_id(self):
        assert self.channel.channel_id == 'UC_x5XG1OV2P6uZZ5FSM9Ttw'

    def test_title(self):
        assert self.channel.title == 'Google Developers'

    def test_description(self):
        assert self.channel.description is not None

    def test_url(self):
        assert self.channel.url == 'https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw'

    def test_subscriber_count(self):
        assert isinstance(self.channel.subscriber_count, int)

    def test_video_count(self):
        assert isinstance(self.channel.video_count, int)

    def test_view_count(self):
        assert isinstance(self.channel.view_count, int)

    def test_to_json(self, tmpdir):
        file_name = tmpdir.join('test_channel.json')
        self.channel.to_json(str(file_name))
        with open(str(file_name), 'r') as f:
            data = json.load(f)
            assert data['channel_id'] == 'UC_x5XG1OV2P6uZZ5FSM9Ttw'
            assert data['title'] == 'Google Developers'
            assert data['description'] is not None
            assert data['url'] == 'https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw'
            assert isinstance(data['subscriber_count'], int)
            assert isinstance(data['video_count'], int)
            assert isinstance(data['view_count'], int)
        os.remove(str(file_name))

class TestVideo:
    def test_init(self):
        video = Video('BBotskuyw_M')
        assert video.video_id == 'BBotskuyw_M'
        assert video.title is not None
        assert video.view_count is not None
        assert video.like_count is not None

    def test_str(self):
        video = Video('BBotskuyw_M')
        assert str(video) == video.title

    def test_invalid_video_id(self):
        try:
            video = Video('BBotskuyw_M')
            assert False
        except:
            assert True

class TestPLVideo:
    def test_init(self):
        pl_video = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
        assert pl_video.video_id == 'BBotskuyw_M'
        assert pl_video.playlist_id == 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD'
        assert pl_video.title is not None
        assert pl_video.view_count is not None
        assert pl_video.like_count is not None
        assert pl_video.playlist_title is not None

    def test_str(self):
        pl_video = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
        assert str(pl_video) == f'{pl_video.title} ({pl_video.playlist_title})'

    def test_invalid_video_id(self):
        try:
            pl_video = PLVideo('1234abcd', 'xyz789')
            assert False
        except:
            assert True

    def test_invalid_playlist_id(self):
        try:
            pl_video = PLVideo('abcd1234', '789xyz')
            assert False
        except:
            assert True