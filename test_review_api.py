#!/usr/bin/env python3
"""
Test script for Movie Review API
"""
import requests
import json

def test_api():
    base_url = 'http://127.0.0.1:8000'
    
    print("🧪 Testing Movie Review API")
    print("=" * 50)
    
    # Test 1: GET reviews endpoint
    print("\n1. Testing GET /api/reviews/")
    try:
        response = requests.get(f'{base_url}/api/reviews/')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            print(f"   ✅ GET successful! Found {count} existing reviews")
        else:
            print(f"   ❌ GET failed: {response.text}")
    except Exception as e:
        print(f"   ❌ GET error: {e}")
    
    # Test 2: POST new review
    print("\n2. Testing POST /api/reviews/")
    try:
        # Create a session to handle cookies
        session = requests.Session()
        
        # Get CSRF token from the search page
        csrf_response = session.get(f'{base_url}/search/')
        csrf_token = session.cookies.get('csrftoken', '')
        
        # Prepare review data
        review_data = {
            'movie_title': 'Test Movie 2025',
            'review_content': 'This is a test review created via automated testing.',
            'rating': 4
        }
        
        # Set headers
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
            'Referer': f'{base_url}/search/'
        }
        
        # Make POST request
        post_response = session.post(
            f'{base_url}/api/reviews/',
            data=json.dumps(review_data),
            headers=headers
        )
        
        print(f"   Status: {post_response.status_code}")
        
        if post_response.status_code in [200, 201]:
            result = post_response.json()
            print(f"   ✅ POST successful! Created review ID: {result.get('id')}")
            print(f"   📝 Movie: {result.get('movie_title')}")
            print(f"   ⭐ Rating: {result.get('rating')}/5")
        else:
            print(f"   ❌ POST failed: {post_response.text}")
            
    except Exception as e:
        print(f"   ❌ POST error: {e}")
    
    # Test 3: Verify the review was created
    print("\n3. Verifying review was created")
    try:
        response = requests.get(f'{base_url}/api/reviews/')
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            print(f"   ✅ Now have {count} total reviews")
            
            # Look for our test review
            test_reviews = [r for r in data.get('results', []) if r.get('movie_title') == 'Test Movie 2025']
            if test_reviews:
                print(f"   ✅ Found our test review: {test_reviews[0]['movie_title']}")
            else:
                print(f"   ⚠️ Test review not found in results")
        
    except Exception as e:
        print(f"   ❌ Verification error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")

if __name__ == "__main__":
    test_api()
