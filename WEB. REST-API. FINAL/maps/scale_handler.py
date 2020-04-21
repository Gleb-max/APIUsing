def get_scale(json):
    envelope = json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]
    up = list(map(float, envelope["upperCorner"].split()))
    down = list(map(float, envelope["lowerCorner"].split()))
    dx = up[0] - down[0]
    dy = up[1] - down[1]
    return f"{dx},{dy}"
