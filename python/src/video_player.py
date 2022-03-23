"""A video player class."""

from numpy import true_divide
from .video_library import VideoLibrary
import random
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video = None
        self._paused = False
        self._playlists = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        video_list = self._video_library.get_all_videos()
        video_titles = []
        for video in video_list:
            video_titles.append(video.title)
        sorted_titles = sorted(video_titles)
        print("Here's a list of all available videos:")
        for sorted_title in sorted_titles:
            for video in video_list:
                if sorted_title == video.title:
                    print(
                        f"{video.title} ({video.video_id}) [{' '.join(video.tags)}]")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        video = self._video_library.get_video(video_id)

        if not video:
            print("Cannot play video: Video does not exist")
            return

        if self._current_video != None:
            print(f"Stopping video: {self._current_video.title}")
            print(f"Playing video: {video.title}")
            self._current_video = video
            self._paused = False
            return

        print(f"Playing video: {video.title}")
        self._current_video = video

    def stop_video(self):
        """Stops the current video."""

        if self._current_video == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self._current_video.title}")
            self._current_video = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        if len(self._video_library.get_all_videos()) == 0:
            print("No videos available")
            return

        self.play_video(random.choice(
            self._video_library.get_all_videos()).video_id)

    def pause_video(self):
        """Pauses the current video."""

        if self._current_video == None:
            print("Cannot pause video: No video is currently playing")
        elif self._paused == False:
            self._paused = True
            print(f"Pausing video: {self._current_video.title}")
        else:
            print(f"Video already paused: {self._current_video.title}")

    def continue_video(self):
        """Resumes playing the current video."""

        if self._current_video == None:
            print("Cannot continue video: No video is currently playing")
        elif self._paused == True:
            self._paused = False
            print(f"Continuing video: {self._current_video.title}")
        else:
            print(f"Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""

        if self._current_video == None:
            print("No video is currently playing")
        elif self._paused == False:
            print(
                f"Currently playing: {self._current_video.title} ({self._current_video.video_id}) [{' '.join(self._current_video.tags)}]")
        else:
            print(
                f"Currently playing: {self._current_video.title} ({self._current_video.video_id}) [{' '.join(self._current_video.tags)}] - PAUSED")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlists.get(playlist_name.lower()) != None:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlists[playlist_name.lower()] = Playlist(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        if self._playlists.get(playlist_name.lower()) == None:
            print(
                f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        elif self._playlists.get(playlist_name.lower())._videos.get(video_id) != None:
            print(f"Cannot add video to {playlist_name}: Video already added")
        else:
            self._playlists.get(playlist_name.lower())._videos[video_id] = True
            print(
                f"Added video to {playlist_name}: {self._video_library.get_video(video_id).title}")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for key in sorted(self._playlists):
                print(f"  {self._playlists[key]._name}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlists.get(playlist_name.lower()) == None:
            print(
                f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            print(f"Showing playlist: {playlist_name}")
            if len(self._playlists[playlist_name.lower()]._videos.keys()) == 0:
                print("No videos here yet")
            else:
                for key in self._playlists[playlist_name.lower()]._videos.keys():
                    video = self._video_library.get_video(key)
                    print(
                        f"  {video.title} ({video.video_id}) [{' '.join(video.tags)}]")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        if self._playlists.get(playlist_name.lower()) == None:
            print(
                f"Cannot remove video from {playlist_name}: Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print(
                f"Cannot remove video from {playlist_name}: Video does not exist")
        elif self._playlists.get(playlist_name.lower())._videos.get(video_id) == None:
            print(
                f"Cannot remove video from {playlist_name}: Video is not in playlist")
        else:
            self._playlists.get(playlist_name.lower())._videos.pop(video_id)
            print(
                f"Removed video from {playlist_name}: {self._video_library.get_video(video_id).title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlists.get(playlist_name.lower()) == None:
            print(
                f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            for key in self._playlists[playlist_name.lower()]._videos.keys():
                self._playlists.get(playlist_name.lower())._videos.pop(key)
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlists.get(playlist_name.lower()) == None:
            print(
                f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            self._playlists.pop(playlist_name.lower())
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
