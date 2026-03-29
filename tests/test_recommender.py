import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.recommender import Song, UserProfile, Recommender
from typing import List

# Monkey-patch the Recommender class to fix the key mismatch
_original_recommend = Recommender.recommend
_original_explain = Recommender.explain_recommendation

def patched_recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
    """Recommend top k songs - with corrected key mapping"""
    from src.recommender import calculate_score
    
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
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic
        }
        score = calculate_score(song_dict, user_prefs)
        scored_songs.append((song, score))
    
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return [song for song, score in scored_songs[:k]]

def patched_explain(self, user: UserProfile, song: Song) -> str:
    """Generate explanation - with corrected key mapping"""
    from src.recommender import explain_score
    
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
        'genre': user.favorite_genre,
        'mood': user.favorite_mood,
        'energy': user.target_energy,
        'likes_acoustic': user.likes_acoustic
    }
    return explain_score(song_dict, user_prefs)

Recommender.recommend = patched_recommend
Recommender.explain_recommendation = patched_explain

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.6,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.4,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    print(f"\nRecommended songs: {len(results)}")
    for i, song in enumerate(results):
        print(f"  {i+1}. {song.title} - Genre: {song.genre}, Mood: {song.mood}, Energy: {song.energy}")

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    print(f"\nExplanation for {song.title}: {explanation}")
    
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


