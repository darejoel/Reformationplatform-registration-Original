import requests










import requests

def get_country_details(country_code):
    response = requests.get(
      f'https://api.countrystatecity.in/v1/countries/{country_code}',
      headers={'X-CSCAPI-KEY': 'a3RQYjRqUmhmT1hkZDdjVHA4enFMcWZ0QVlNaDU1NUN1QnZ2MjNWTQ=='}
    )
    
    if response.ok:
        return response.json()
    else:
        print('Country not found')
        return None

country = get_country_details('IN')
country= country['name']
print(country)
