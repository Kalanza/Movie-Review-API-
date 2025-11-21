#!/usr/bin/env python3
"""
Test script to verify that reviews can be created and retrieved later
"""
import requests
import json
import time

def test_review_persistence():
    base_url = 'http://127.0.0.1:8000'

    print("🧪 Testing Review Persistence")
    print("=" * 50)

    # Test 1: Create a review
    print("\n1. Creating a new review...")
    try:
        review_data = {
            'movie_title': 'Test Movie for Persistence',
            'review_content': 'This review should be retrievable later. Created at ' + str(time.time()),
            'rating': 5
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{base_url}/api/reviews/', data=json.dumps(review_data), headers=headers)

        print(f"   Status: {response.status_code}")

        if response.status_code in [200, 201]:
            created_review = response.json()
            review_id = created_review.get('id')
            print(f"   ✅ Review created successfully! ID: {review_id}")
            print(f"   📝 Movie: {created_review.get('movie_title')}")
            print(f"   ⭐ Rating: {created_review.get('rating')}/5")
        else:
            print(f"   ❌ Failed to create review: {response.text}")
            return

    except Exception as e:
        print(f"   ❌ Error creating review: {e}")
        return

    # Wait a moment
    time.sleep(1)

    # Test 2: Retrieve the specific review
    print(f"\n2. Retrieving review with ID {review_id}...")
    try:
        response = requests.get(f'{base_url}/api/reviews/{review_id}/')
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            retrieved_review = response.json()
            print("   ✅ Review retrieved successfully!")
            print(f"   📝 Movie: {retrieved_review.get('movie_title')}")
            print(f"   ⭐ Rating: {retrieved_review.get('rating')}/5")
            print(f"   📄 Content: {retrieved_review.get('review_content')[:50]}...")

            # Verify it's the same review
            if retrieved_review.get('id') == review_id:
                print("   ✅ Review ID matches!")
            else:
                print("   ❌ Review ID mismatch!")

            if retrieved_review.get('movie_title') == review_data['movie_title']:
                print("   ✅ Movie title matches!")
            else:
                print("   ❌ Movie title mismatch!")

        else:
            print(f"   ❌ Failed to retrieve review: {response.text}")

    except Exception as e:
        print(f"   ❌ Error retrieving review: {e}")

    # Test 3: Verify in list of all reviews
    print("\n3. Verifying review appears in list of all reviews...")
    try:
        response = requests.get(f'{base_url}/api/reviews/')
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            matching_reviews = [r for r in results if r.get('id') == review_id]

            if matching_reviews:
                print("   ✅ Review found in list of all reviews!")
            else:
                print("   ❌ Review not found in list of all reviews!")
        else:
            print(f"   ❌ Failed to get reviews list: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Error checking reviews list: {e}")

    print("\n" + "=" * 50)
    print("🎯 Persistence test completed!")

if __name__ == "__main__":
    test_review_persistence()