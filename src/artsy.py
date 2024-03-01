import requests


def handle_api_error(response):
    """Handle API errors and print error details."""
    if response.status_code in [400, 404]:
        error_info = response.json()
        print(f"Error Type: {error_info.get('type', 'No error type')}")
        print(f"Message: {error_info.get('message', 'No error message')}")
        detail = error_info.get('detail', 'No additional detail')
        if isinstance(detail, dict):
            for key, value in detail.items():
                print(f"{key}: {value}")
        else:
            print(f"Detail: {detail}")
    else:
        print(f"Failed with status code: {response.status_code}, response: {response.text}")


def get_artworks_by_artist(access_token, artist_id):
    """
    Fetches and prints all artworks by a specified artist using the Artsy API.

    Parameters:
    - access_token (str): The access token for Artsy API authentication.
    - artist_id (str): The unique identifier for the artist.
    """
    url = 'https://api.artsy.net/api/artworks'
    headers = {'X-Xapp-Token': access_token}
    params = {'artist_id': artist_id,
              'published' : True}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        artworks_data = response.json()
        artworks = artworks_data['_embedded']['artworks']
        print(f"Found {len(artworks)} artworks by the artist with ID {artist_id}.")

        for artwork in artworks:
            title = artwork.get('title', 'No title provided')
            created_at = artwork.get('created_at', 'No creation date provided')
            medium = artwork.get('medium', 'No medium provided')
            dimensions_in = artwork.get('dimensions', {}).get('in', {}).get('text', 'No dimensions provided')
            print(f"Title: {title}, Created At: {created_at}, Medium: {medium}, Dimensions: {dimensions_in}")

    else:
        print(f"Failed to fetch artworks for artist ID {artist_id}. Status code: {response.status_code}")


def search_artist_id_by_name(access_token, artist_name):
    """
        Search for an artist by name using the Artsy API, print the JSON response,
        and return the ID of the first artist found.
        """
    url = "https://api.artsy.net/api/search"
    params = {
        'q': f"{artist_name}"
    }
    headers = {
        "X-XAPP-Token": access_token
    }

    print(f"Searching for artist: {artist_name}...")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:

        # Process the JSON to find artist IDs
        results = response.json()['_embedded']['results']
        artists_found = [result for result in results if result['type'] == 'artist']

        if not artists_found:
            print(f"No artists found matching the name: {artist_name}")
            return None

        # Assuming the first artist found is the desired one
        first_artist = artists_found[0]
        artist_id = first_artist['_links']['self']['href'].split('/')[-1]
        artist_name_found = first_artist['title']
        print(f"Found Artist ID: {artist_id} for '{artist_name_found}'")
        return artist_id
    else:
        error_message = f"Failed to search for artist due to an error. Status code: {response.status_code}"
        if response.status_code in [400, 404]:
            error_info = response.json()
            error_message += f" - {error_info.get('message', 'No additional error details.')}"
        print(error_message)
        return None


def get_artist(access_token, artist_id):
    """Fetch artist details using the Artsy API."""
    url = f'https://api.artsy.net/api/artists/{artist_id}'
    headers = {'X-XAPP-Token': access_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        handle_api_error(response)
        return None


def display_artist_details(artist):
    """Display selected details of an artist."""
    print("Artist Details:")
    print(f"Name: {artist.get('name')}")
    print(f"Biography: {artist.get('biography', 'No biography available')}")
    print(f"Birthday: {artist.get('birthday', 'No birthday available')}")
    print(f"Nationality: {artist.get('nationality', 'No nationality available')}")


def get_artist_shows(access_token, artist_id):
    """Fetch and display all shows and their descriptions for a specified artist."""
    url = f'https://api.artsy.net/api/shows'
    params = {'artist_id': artist_id}
    headers = {'X-XAPP-Token': access_token}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        shows_data = response.json()
        if '_embedded' in shows_data and 'shows' in shows_data['_embedded']:
            shows = shows_data['_embedded']['shows']
            if shows:
                print(f"\nShows for artist ID {artist_id}:")
                for show in shows:
                    title = show.get('name', 'No title available')
                    description = show.get('description', 'No description available')
                    print(f"\nTitle: {title}")
                    print(f"Description: {description}")
            else:
                print(f"No shows found for artist ID {artist_id}.")
        else:
            print("Unexpected JSON structure. No 'shows' key found.")
    else:
        handle_api_error(response)



def get_artwork_details(access_token, artwork_id):
    """Fetch details of a specific artwork using the Artsy API."""
    url = f'https://api.artsy.net/api/artworks/{artwork_id}'
    headers = {'X-XAPP-Token': access_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        handle_api_error(response)
        return None


def display_artworks(artworks):
    """Display details of artworks."""
    if artworks:
        print("\nArtworks by the artist:")
        for artwork in artworks:
            print(f"Title: {artwork.get('title', 'No title available')}")
            # Add more fields as needed
    else:
        print("No artworks found for the specified artist.")


def search_artwork_by_name(access_token, artwork_name):
    """
    Search for an artwork by name using the Artsy API, print the JSON response,
    and return the ID of the first artwork found.
    """
    url = "https://api.artsy.net/api/search"
    params = {
        'q': artwork_name,
        'type': 'artwork'  # This parameter can help narrow down the search results to artworks only
    }
    headers = {"X-XAPP-Token": access_token}

    print(f"\nSearching for artwork: {artwork_name}...")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        search_results = response.json()
        artworks_found = [
            result for result in search_results['_embedded']['results']
            if result['type'] == 'artwork'
        ]

        if artworks_found:
            print("Artwork search results:")
            for artwork in artworks_found:
                artwork_id = artwork['_links']['self']['href'].split('/')[-1]
                title = artwork['title']
                print(f"Artwork ID: {artwork_id}, Title: {title}")
                # Optionally, return the first artwork ID found or keep printing IDs
                # return artwork_id
        else:
            print(f"No artworks found matching the name: {artwork_name}")
            return None
    else:
        print(f"Error retrieving artwork by name {artwork_name}: {response.status_code}")
        return None



def get_artists_by_criteria(access_token, criteria):
    """
    Fetch a list of artists based on given criteria.
    `criteria` is a dictionary of parameter names and values.
    """
    url = 'https://api.artsy.net/api/artists'
    headers = {'X-XAPP-Token': access_token}
    response = requests.get(url, headers=headers, params=criteria)
    if response.status_code == 200:
        data = response.json()
        artists = data['_embedded']['artists']
        return [artist['id'] for artist in artists]  # Extract and return artist IDs
    else:
        print(f"Error fetching artists: {response.status_code}")
        return []


def get_similar_artwork_ids(access_token, artwork_id):
    """Fetch IDs of artworks similar to the specified artwork using the Artsy API."""
    # Construct the URL for fetching similar artworks by the artwork's ID
    url = f'https://api.artsy.net/api/artworks?similar_to_artwork_id={artwork_id}'
    headers = {'X-XAPP-Token': access_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        artworks_data = response.json()
        # Assuming '_embedded' and 'artworks' keys exist based on the provided documentation
        if '_embedded' in artworks_data and 'artworks' in artworks_data['_embedded']:
            similar_artworks = artworks_data['_embedded']['artworks']
            print("\nIDs of Similar Artworks:")
            for artwork in similar_artworks:
                print(artwork['id'])
            return [artwork['id'] for artwork in similar_artworks]
        else:
            print("No similar artworks found or the structure is different.")
            return []  # Return an empty list if no similar artworks found
    else:
        handle_api_error(response)
        return []

def display_artwork_details(artwork):
    """Display selected details of an artwork."""
    print("\nArtwork Details:")
    print(f"Title: {artwork.get('title', 'No title available')}")
    print(f"Medium: {artwork.get('medium', 'No medium info available')}")
    print(f"Date: {artwork.get('date', 'No date available')}")
    dimensions = artwork.get('dimensions', {})
    dimensions_in = dimensions.get('in', {})
    dimensions_cm = dimensions.get('cm', {})
    print(f"Dimensions (in): {dimensions_in.get('text', 'No dimensions available')}")
    print(f"Dimensions (cm): {dimensions_cm.get('text', 'No dimensions available')}")
    print(f"Collecting Institution: {artwork.get('collecting_institution', 'No collecting institution available')}")


if __name__ == '__main__':
    access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJyb2xlcyI6IiIsInN1YmplY3RfYXBwbGljYXRpb24iOiI3YjNlODkwYS02MzQzLTRkZW' \
                   'QtOTEzYi03YjczMGMwYzEzNmEiLCJleHAiOjE3MDk2MDI4MTAsImlhdCI6MTcwODk5ODAxMCwiYXVkIjoiN2IzZTg5M' \
                   'GEtNjM0My00ZGVkLTkxM2ItN2I3MzBjMGMxMzZhIiwiaXNzIjoiR3Jhdml0eSIsImp0aSI6IjY1ZGQzZDdhZDM3NmEz' \
                   'MDAwZWVlZTlkZCJ9.o2j8I5ygp4IiF4ZSTYIVkcd95hh2opGw25N5YwbHSYY'
    artist_name = input("Please enter the artist's name you are searching for: ")
    artwork_id = "516dfb9ab31e2b2270000c45"

    artist_id = search_artist_id_by_name(access_token, artist_name)
    get_artworks_by_artist(access_token, artist_id)

    artist = get_artist(access_token, artist_id)
    if artist:
        display_artist_details(artist)
    else:
        print("Could not retrieve artist details.")

    get_artist_shows(access_token, artist_id)

    similar_artists_ids = get_artists_by_criteria(access_token, {'similar_to_artist_id': artist_id})
    print(f"Similar Artist IDs: {similar_artists_ids}")

    artwork = get_artwork_details(access_token, artwork_id)

    if artwork:
        display_artwork_details(artwork)
    else:
        print("Could not retrieve artwork details.")

    similar_artwork_ids = get_similar_artwork_ids(access_token, artwork_id)

    art_name = input("Please enter the name of an art piece you are looking for: ")
    search_artwork_by_name(access_token, art_name)
