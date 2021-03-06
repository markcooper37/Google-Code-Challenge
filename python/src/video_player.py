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
        self._flagged = {}

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
                    if self._flagged.get(video.video_id) != None:
                        print(f"{video.title} ({video.video_id}) [{' '.join(video.tags)}] - FLAGGED (reason: {self._flagged[video.video_id]})")
                    else:
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
        elif self._flagged.get(video_id) != None:
            print(
                f"Cannot play video: Video is currently flagged (reason: {self._flagged[video_id]})")
        elif self._current_video != None:
            print(f"Stopping video: {self._current_video.title}")
            print(f"Playing video: {video.title}")
            self._current_video = video
            self._paused = False
        else:
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

        for key in self._video_library._videos:
            if self._flagged.get(key) == None:
                self.play_video(key)
                return
        print("No videos available")

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
        elif self._flagged.get(video_id) != None:
            print(
                f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {self._flagged[video_id]})")
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
                    if self._flagged.get(video.video_id) != None:
                        print(f"{video.title} ({video.video_id}) [{' '.join(video.tags)}] - FLAGGED (reason: {self._flagged[video.video_id]})")
                    else:
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

        video_list = self._video_library.get_all_videos()
        correct_videos = []
        for video in video_list:
            if search_term.lower() in video.title.lower() and self._flagged.get(video.video_id) == None:
                correct_videos.append(video)
        if len(correct_videos) == 0:
            print(f"No search results for {search_term}")
            return
        sorted(correct_videos, key=lambda x: x.title)
        print(f"Here are the results for {search_term}:")
        for index, video in enumerate(correct_videos):
            print(
                f"  {index+1}) {video.title} ({video.video_id}) [{' '.join(video.tags)}]")
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        try:
            user_input = int(input(""))
        except ValueError:
            return
        else:
            if user_input >= 1 and user_input <= len(correct_videos):
                self.play_video(correct_videos[user_input-1].video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        video_list = self._video_library.get_all_videos()
        correct_videos = []
        for video in video_list:
            if self._flagged.get(video.video_id) != None:
                continue
            for tag in video.tags:
                if video_tag.lower() == tag.lower():
                    correct_videos.append(video)
                    break
        if len(correct_videos) == 0:
            print(f"No search results for {video_tag}")
            return
        sorted(correct_videos, key=lambda x: x.title)
        print(f"Here are the results for {video_tag}:")
        for index, video in enumerate(correct_videos):
            print(
                f"  {index+1}) {video.title} ({video.video_id}) [{' '.join(video.tags)}]")
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        try:
            user_input = int(input(""))
        except ValueError:
            return
        else:
            if user_input >= 1 and user_input <= len(correct_videos):
                self.play_video(correct_videos[user_input-1].video_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        if video_id in self._flagged:
            print("Cannot flag video: Video is already flagged")
        elif self._video_library.get_video(video_id) == None:
            print("Cannot flag video: Video does not exist")
        else:
            if self._current_video == self._video_library.get_video(video_id):
                self.stop_video()
            if flag_reason == "":
                flag_reason = "Not supplied"
            self._flagged[video_id] = flag_reason
            print(
                f"Successfully flagged video: {self._video_library.get_video(video_id).title} (reason: {flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

        if self._video_library.get_video(video_id) == None:
            print("Cannot remove flag from video: Video does not exist")
        elif video_id not in self._flagged:
            print("Cannot remove flag from video: Video is not flagged")
        else:
            self._flagged.pop(video_id)
            print(
                f"Successfully removed flag from video: {self._video_library.get_video(video_id).title}")
