from typing import Union, Annotated

from fastapi import FastAPI, Query, Path
import json
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/city/{city_name}")
def read_city(city_name: Annotated[str, Path(regex="yangon", title="We still only accept yangon")]):
    city = ['Thaketa', 'Insein', 'Bahan', 'Botahtaung', 'Dagon Myothit East', 'Dagon Myothit North', 'Kyauktada', 'Dawbon', 'Kamaryut', 'Kyeemyindaing', 'Lanmadaw', 'Latha', 'Mayangone', 'Mingaladon', 'Mingalar Taung Nyunt', 'North Okkalapa', 'Pabedan', 'Pazundaung',
            'Shwepyithar', 'Seikgyikanaungto', 'Sanchaung', 'Dagon Myothit Seikkan', 'Dagon Myothit South', 'Dagon', 'Dala', 'Hlaing Thar Yar', 'Hlaing', 'Thingangyun', 'Thongwa', 'Yankin', 'Kawhmu', 'Kayan', 'Kungyangon', 'Kyauktan', 'South Okkalapa', 'Tarmwe', 'Thanlyin', 'Twantay']
    return {"yangon": city}
@app.get("/city/{city_name}/township/{township_name}")
def read_city_township(city_name: Annotated[str, Path(regex="yangon", title="We still only accept yangon")], township_name: Union[str, None] = None):    

    if (township_name == None):
        json_file_path = "json/township.json"
    elif(township_name == 'Bahan'):
        json_file_path = "json/bahan.json"
    elif(township_name == 'Botahtaung'):
        json_file_path = "json/botahtaung.json"
    elif(township_name == 'Bahan'):
        json_file_path = "json/bahan.json"
    elif(township_name == 'Dagon Myothit East'):
        json_file_path = "json/dagon_myothit_east.json"
    elif(township_name == 'Dagon Myothit North'):
        json_file_path = "json/dagon_myothit_north.json"
    elif(township_name == 'Dagon Myothit Seikkan'):
        json_file_path = "json/dagon_myothit_seikkan.json"
    elif(township_name == 'Dagon Myothit South'):
        json_file_path = "json/dagon_myothit_south.json"
    elif(township_name == 'Dagon'):
        json_file_path = "json/Dagon.json"
    elif(township_name == 'dala'):
        json_file_path = "json/dala.json"
    elif(township_name == 'Dawbon'):
        json_file_path = "json/dawbon.json"
    elif(township_name == 'Hlaing'):
        json_file_path = "json/hlaing.json"
    elif(township_name == 'Hlaing Thar Yar'):
        json_file_path = "json/hlaingtharyar.json"
    elif(township_name == 'Insein'):
        json_file_path = "json/insein.json"
    elif(township_name == 'Kamaryut'):
        json_file_path = "json/kamaryut.json"
    elif(township_name == 'Kawhmu'):
        json_file_path = "json/kawhmu.json"
    elif(township_name == 'Kayan'):
        json_file_path = "json/kayan.json"
    elif(township_name == 'Kungyangon'):
        json_file_path = "json/kungyangon.json"
    elif(township_name == 'Kyauktada'):
        json_file_path = "json/kyauktada.json"
    elif(township_name == 'Kyauktan'):
        json_file_path = "json/kyauktan.json"
    elif(township_name == 'Kyeemyindaing'):
        json_file_path = "json/kyeemyindaing.json"
    elif(township_name == 'Lanmadaw'):
        json_file_path = "json/lamadaw.json"
    elif(township_name == 'Latha'):
        json_file_path = "json/latha.json"
    elif(township_name == 'Mayangone'):
        json_file_path = "json/mayagone.json"
    elif(township_name == 'Mingalar Taung Nyunt'):
        json_file_path = "json/mingalartaungnyunt.json"
    elif(township_name == 'Mingaladon'):
        json_file_path = "json/mingladon.json"
    elif(township_name == 'North Okkalapa'):
        json_file_path = "json/northoakalapa.json"
    elif(township_name == 'Pabedan'):
        json_file_path = "json/pabedan.json"
    elif(township_name == 'Pazundaung'):
        json_file_path = "json/pazundaung.json"
    elif(township_name == 'Sanchaung'):
        json_file_path = "json/sanchaung.json"
    elif(township_name == 'Seikgyikanaungto'):
        json_file_path = "json/seigyikanaungto.json"
    elif(township_name == 'Shwepyithar'):
        json_file_path = "json/shwepyithar.json"
    elif(township_name == 'South Okkalapa'):
        json_file_path = "json/southoakalapa.json"
    elif(township_name == 'Tarmwe'):
        json_file_path = "json/tarmwe.json"
    elif(township_name == 'Thaketa'):
        json_file_path = "json/thaketa.json"
    elif(township_name == 'Thanlyin'):
        json_file_path = "json/thanlyin.json"
    elif(township_name == 'Thingangyun'):
        json_file_path = "json/thingangyun.json"
    elif(township_name == 'Thongwa'):
        json_file_path = "json/thongwa.json"
    elif(township_name == 'Twantay'):
        json_file_path = "json/twantay.json"
    elif(township_name == 'yankin'):
        json_file_path = "json/yankin.json"
    
    try:
        with open(json_file_path, "r") as file:
            # Load the JSON data from the file
            data = json.load(file)
        return data  # Return the JSON data as the API response
    except FileNotFoundError:
        # Handle the case when the file is not found
        return {"error": "File not found"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
