"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "blues", "mood": "melancholic", "energy": 0.5}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 70)
    print("TOP 5 MUSIC RECOMMENDATIONS".center(70))
    print("=" * 70 + "\n")
    
    for idx, rec in enumerate(recommendations, 1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{idx}. {song['title']}")
        print(f"   Score: {score:.2f}/4.0")
        print(f"   Reasons: {explanation}")
        print()


if __name__ == "__main__":
    main()
