import requests 
import image_lib
import os


poke_info_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():

    #info = get_poke_info(' PikaCHU   ')

    #get_pokemon_names()

    #download_poke_artwork('pikachu', r'C:\Users\joeln\Downloads')

    return


def get_poke_info(poke_name_or_num):
    """ Fetches information about pokemon from the PokeAPI

    Args:
        poke_name_or_num (str): name or number of any pokemon

    Returns:
        dictionary : all information about requested pokemon 
    """

    # Convert parameter to lower case and remove leading or trailing whitespace
    poke_name = poke_name_or_num.lower()
    final_poke_search = poke_name.strip()

    # Send a get request for pokemon information 
    print(f'Getting information for {final_poke_search.capitalize()} . . . ', end='')
    resp_msg = requests.get(f'{poke_info_URL}{final_poke_search}')

    # Check whether the request was successful 
    if resp_msg.ok:
        print('Success')
        info_dict = resp_msg.json()
        return info_dict

    else:
        print('Failure')
        print(f'Responce code: {resp_msg.status_code} ({resp_msg.reason})')
        print(f'Error: {resp_msg.text}')


def get_pokemon_names(offset=0, limit=100000):
    """Gets a list of all Pokemon names from the PokeAPI

    Args:
        offset (int, optional): Number of the pokemon you would like to start at. Defaults to 0.
        limit (int, optional): Number of results you want. Defaults to 100000.

    Returns:
        List : list of all pokemon names from the API
    """

    query_params = {
        "limit" : limit,
        "offset" : offset
    }


    # Send a get request for pokemon names
    print(f'Getting list of pokemon names. . . ', end='')
    resp_msg = requests.get(poke_info_URL, params=query_params)

    # Check whether the request was successful 
    if resp_msg.ok:
        print('Success')

        resp_dict = resp_msg.json()

        poke_names = [p['name'] for p in resp_dict['results']]



        return poke_names

    else:
        print('Failure')
        print(f'Responce code: {resp_msg.status_code} ({resp_msg.reason})')
        print(f'Error: {resp_msg.text}')


def download_poke_artwork(poke_name, folder_path):
    """retrieves a the artwork URL from the Poke API and downloads the image from the internet with the pokemons name as the filename

    Args:
        poke_name (int, str): Pokemon to retrieve artowrk for
        folder_path (str): directory the image will be downloaded 

    Returns:
        str : file path of the newly downloaded image
    """

    poke_info = get_poke_info(poke_name)
    if poke_info is None:
        return False

    poke_image_url = poke_info['sprites']['other']['official-artwork']['front_default']

    image_data = image_lib.download_image(poke_image_url)
    if image_data is None:
        return False

    image_ext = poke_image_url.split('.')[-1]
    file_name = f'{poke_info["name"]}.{image_ext}'
    file_path = os.path.join(folder_path, file_name)

    if image_lib.save_image_file(image_data, file_path):
        return file_path
    
    return False

    


if __name__ == "__main__":
    main()