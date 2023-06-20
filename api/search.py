import tempfile
import aiohttp
from api import request


async def fetch_audio_stream(url):
        # Invoke the search method to get the necessary parameters
        search_url, headers, params = await request.search(url)

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers, params=params) as response:
                data = await response.json()
                # Process the search results and extract the necessary information and assuming the first result is the desired track
                track = data['data'][0]

                # Get the preview URL of the track
                preview_url = track['preview']

                # Fetch the audio stream using the preview URL
                async with session.get(preview_url) as audio_response:
                    # Read the audio stream as bytes
                    audio_bytes = await audio_response.read()

                    # Return the audio stream as a file-like object (BytesIO)
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(audio_bytes)

                # Return the path to the temporary file and filename
                return tmp_file.name, track['title']