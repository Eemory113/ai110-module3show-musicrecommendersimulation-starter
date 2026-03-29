from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Recommend top k songs for a user based on scoring recipe."""
        scored_songs = []
        for song in self.songs:
            song_dict = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'mood': song.mood,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm,
                'valence': song.valence,
                'danceability': song.danceability,
                'acousticness': song.acousticness
            }
            user_prefs = {
                'favorite_genre': user.favorite_genre,
                'favorite_mood': user.favorite_mood,
                'target_energy': user.target_energy,
                'likes_acoustic': user.likes_acoustic
            }
            score = calculate_score(song_dict, user_prefs)
            scored_songs.append((song, score))
        
        # Sort by score descending, take top k
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate explanation for why a song was recommended."""
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness
        }
        user_prefs = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic
        }
        return explain_score(song_dict, user_prefs)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            songs.append(row)
    return songs

def calculate_score(song: Dict, user_prefs: Dict) -> float:
    """
    Scoring Recipe (Option A):
    +2.0 points for genre match
    +1.0 point for mood match
    +0 to 1.0 points based on energy similarity
    
    Returns: score between 0.0 and 4.0
    """
    score = 0.0
    
    # +2.0 for genre match
    if song['genre'] == user_prefs['genre']:
        score += 2.0
    
    # +1.0 for mood match
    if song['mood'] == user_prefs['mood']:
        score += 1.0
    
    # Energy similarity: 0 to 1.0 points (closer = higher)
    energy_distance = abs(float(song['energy']) - user_prefs['energy'])
    energy_points = max(0, 1.0 - energy_distance)
    score += energy_points
    
    return score


def explain_score(song: Dict, user_prefs: Dict) -> str:
    """
    Generate human-readable explanation for a song's score.
    """
    reasons = []
    
    # Genre match
    if song['genre'] == user_prefs['genre']:
        reasons.append(f"Matches your {user_prefs['genre']} preference (+2.0)")
    
    # Mood match
    if song['mood'] == user_prefs['mood']:
        reasons.append(f"Has the {user_prefs['mood']} mood (+1.0)")
    
    # Energy proximity
    energy_distance = abs(float(song['energy']) - user_prefs['energy'])
    energy_points = max(0, 1.0 - energy_distance)
    if energy_points > 0:
        reasons.append(f"Energy {float(song['energy']):.2f} is close to your target {user_prefs['energy']:.2f} (+{energy_points:.2f})")
    
    return " | ".join(reasons) if reasons else "Decent match"


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    
    Returns top k songs ranked by score with explanations.
    Expected return format: (song_dict, score, explanation)
    """
    scored_songs = []
    
    for song in songs:
        score = calculate_score(song, user_prefs)
        explanation = explain_score(song, user_prefs)
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending, return top k
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
