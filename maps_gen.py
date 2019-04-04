import csv
import folium

def read_file():
    file = 'ping.csv'
    table = []
    with open(file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        for i in data:
            table.append(i)
    return table[1:]
    
   m = folium.Map(
    location=[51.719082, 94.433983],
    tiles='OpenStreetMap',
    zoom_start=2
)


for host in read_file():
    lat = float(host[3])
    lot = float(host[4])    
    point = (lat,lot)
    ttl = int(host[7])
    
    if ttl <=50:
        color = '#49e01f'
    elif ttl <=100: 
        color = '#e8ea6e'
    elif ttl <=150 :
        color = '#ffe100'
    elif ttl <=250: 
        color = '#e22b2b'
    else: 
        color = '#353aa0'
    
    folium.PolyLine(locations=[[51.719082, 94.433983], point], color=color, weight=0.1, opacity=0.5).add_to(m)
    
    folium.CircleMarker(
    location=point,
    radius=1,
    
    popup=(host[7]),
    color= color,  

    fill=True,
    fill_color='#3186cc'
).add_to(m)

m
m.save('tsi.html')
