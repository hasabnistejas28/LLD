import random
from abc import ABC, abstractmethod
from typing import List

# ---------------------------
# Song Entity
# ---------------------------

class Song:
    def __init__(self, title: str, artist: str, duration: int):
        self.title = title
        self.artist = artist
        self.duration = duration  # in seconds

    def __repr__(self):
        return f"{self.title} by {self.artist}"


# ---------------------------
# Playlist Entity
# ---------------------------

class Playlist:
    def __init__(self, name: str):
        self.name = name
        self.songs: List[Song] = []

    def add_song(self, song: Song):
        self.songs.append(song)

    def remove_song(self, song: Song):
        self.songs.remove(song)

    def get_songs(self) -> List[Song]:
        return self.songs

    def __repr__(self):
        return f"Playlist({self.name}, {len(self.songs)} songs)"


# ---------------------------
# Strategy Pattern: Playback Modes
# ---------------------------

class PlaybackStrategy(ABC):
    @abstractmethod
    def get_next_song(self, playlist: Playlist, current_index: int) -> int:
        """Return index of the next song"""
        pass


class NormalPlay(PlaybackStrategy):
    def get_next_song(self, playlist: Playlist, current_index: int) -> int:
        if current_index + 1 < len(playlist.songs):
            return current_index + 1
        return -1  # End of playlist


class LoopPlay(PlaybackStrategy):
    def get_next_song(self, playlist: Playlist, current_index: int) -> int:
        return (current_index + 1) % len(playlist.songs)


class ShufflePlay(PlaybackStrategy):
    def get_next_song(self, playlist: Playlist, current_index: int) -> int:
        return random.randint(0, len(playlist.songs) - 1)


class RepeatOnePlay(PlaybackStrategy):
    def get_next_song(self, playlist: Playlist, current_index: int) -> int:
        return current_index  # Always repeat the same song


# ---------------------------
# Player
# ---------------------------

class MusicPlayer:
    def __init__(self, playlist: Playlist, strategy: PlaybackStrategy):
        self.playlist = playlist
        self.strategy = strategy
        self.current_index = 0 if playlist.songs else -1

    def play_current(self):
        if self.current_index == -1:
            print("No songs in playlist.")
        else:
            print(f"Playing: {self.playlist.songs[self.current_index]}")

    def next_song(self):
        if not self.playlist.songs:
            print("Playlist is empty.")
            return

        self.current_index = self.strategy.get_next_song(self.playlist, self.current_index)
        if self.current_index == -1:
            print("Reached end of playlist.")
        else:
            self.play_current()

    def set_strategy(self, strategy: PlaybackStrategy):
        self.strategy = strategy
        print(f"Playback mode changed to: {strategy.__class__.__name__}")


# ---------------------------
# Demo
# ---------------------------

if __name__ == "__main__":
    # Create songs
    s1 = Song("Song A", "Artist 1", 210)
    s2 = Song("Song B", "Artist 2", 180)
    s3 = Song("Song C", "Artist 3", 200)

    # Create playlist
    playlist = Playlist("My Playlist")
    playlist.add_song(s1)
    playlist.add_song(s2)
    playlist.add_song(s3)

    print(playlist)

    # Normal play
    player = MusicPlayer(playlist, NormalPlay())
    player.play_current()
    player.next_song()
    player.next_song()
    player.next_song()  # end

    # Loop play
    player.set_strategy(LoopPlay())
    for _ in range(5):
        player.next_song()

    # Shuffle play
    player.set_strategy(ShufflePlay())
    for _ in range(5):
        player.next_song()

    # Repeat one play
    player.set_strategy(RepeatOnePlay())
    for _ in range(3):
        player.next_song()
