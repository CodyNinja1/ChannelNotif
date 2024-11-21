from bs4 import BeautifulSoup 
import requests as Req 
import numpy
from typing import Literal
import re

Environment = Literal['Storm', 'Canyon', 'Valley', 'Stadium', 'Lagoon', 'United']

def RemoveTMFormatting(Str: str) -> str:
    return re.sub(r"\$(?:(\$)|[0-9a-fA-F]{2,3}|[lh]\[.*?\]|[lh]\[|.)", "", Str)

def GetServersA(OrderBy: str = "playerCount",
                TitleIDs: list[str] = [], 
                Environments: list[Environment] = [],
                ScriptName: str = "",
                Search: str = "",
                Zone: str = "",
                OnlyPublic: str = "0",
                OnlyPrivate: str = "0",
                OnlyLobby: str = "0",
                ExcludeLobby: str = "1",
                Offset: str = "0",
                Length: str = "10"):
    Query = {
        "orderBy":      OrderBy,
        "titleUids":    TitleIDs,
        "environments": Environments,
        "scriptName":   ScriptName,
        "search":       Search,
        "zone":         Zone,
        "onlyPublic":   OnlyPublic,
        "onlyPrivate":  OnlyPrivate,
        "onlyLobby":    OnlyLobby,
        "excludeLobby": ExcludeLobby,
        "offset":       Offset,
        "length":       Length
    }
    Web = Req.get(f"https://maniaplanet.com/webservices/servers/online/", params=Query)
    return Web.json()

def GetChannelsA():
    ServersFiltered = [(server if "channel_" in server["login"] else {}) for server in GetServersA(ExcludeLobby="0", Length="-1")]
    ServersFinal = []

    for Server in ServersFiltered:
        if Server != {}:
            ServersFinal.append(Server)
    
    return ServersFinal

def GetServerGameA(Server: dict[any, any]):
    if Server["environment"] == 'Storm':
        return True
    return False

def GetChannelsByGameA(Shootmania: bool = False):
    Channels = GetChannelsA()
    ChannelsFinal = []

    for Server in Channels:
        if GetServerGameA(Server) and Shootmania:
            ChannelsFinal.append(Server)
        
        if (not GetServerGameA(Server)) and (not Shootmania):
            ChannelsFinal.append(Server)

    return ChannelsFinal

def GetActiveChannelsPlayerCountA(Shootmania: bool = False):
    Channels = GetChannelsByGameA(Shootmania=Shootmania)
    CountsFinal = []

    for Channel in Channels: CountsFinal.append(Channel['player_count'])

    return CountsFinal

def GetChannelNameS(Shootmania: bool = False):
    Out = ""

    Web = Req.get('https://maniaplanet.com/') 
    S = BeautifulSoup(Web.text, 'lxml') 
    N = "1" if Shootmania else "2"
    Tags = S.select_one(f"div.col-md-6:nth-of-type({N})").select("span.mp-format")[0].children

    for Tag in Tags:
        Out += Tag.get_text()

    return Out

def GetChannelNameFromIdS(Id: int = 1):
    Temp = ""
    Web = Req.get(f'https://maniaplanet.com/channels/programs/{Id}')
    S = BeautifulSoup(Web.text, 'lxml') 
    Tag = S.select("div.card-footer")[0].select("a")[0].select("span")[0]
    Tog = Tag.children
    for Elem in Tog:
        Temp += Elem.get_text()
    return Temp

def GetChannelAuthorFromIdS(Id: int = 1):
    Temp = ""
    Web = Req.get(f'https://maniaplanet.com/channels/programs/{Id}')
    S = BeautifulSoup(Web.text, 'lxml') 
    Tag = S.select("div.d-flex.justify-content-between.align-items-center.small")[0].select("span")[0]
    Tog = Tag.children
    for Elem in Tog:
        Temp += Elem.get_text()
    return Temp.replace('\n', '')

def GetChannelGameFromIdS(Id: int = 1):
    Web = Req.get(f'https://maniaplanet.com/channels/programs/{Id}')
    S = BeautifulSoup(Web.text, 'lxml') 
    Tag = S.select("h1.d-inline-block.p-1.bg-faded.display-4")[0]
    return "Shootmania" in Tag.get_text()

def GetChannelImageURLS(Shootmania: bool = False):
    CleanImgs = []

    Web = Req.get('https://maniaplanet.com/') 
    S = BeautifulSoup(Web.text, 'lxml') 
    N = 0 if Shootmania else 1
    Imgs = S.select("img.w-100")

    for Img in Imgs:
        if ("programs" in Img.attrs["src"]):
            CleanImgs.append(Img)

    return CleanImgs[N].attrs["src"]

def GetImageURLFromChannelIdS(Id: int):
    Web = Req.get(f'https://maniaplanet.com/channels/programs/{Id}')
    S = BeautifulSoup(Web.text, 'lxml') 
    Tag = S.select("img.w-100")[0]

    return Tag.attrs["src"]

# def GetCacheNames():
#     with open("cache_names.json") as CacheNamesFile:
#         return json.load(CacheNamesFile)

# def GetCacheURLs():
#     with open("cache_urls.json") as CacheURLsFile:
#         return json.load(CacheURLsFile)

def GetScheduleS(Shootmania: bool = False):
    CacheNames = {}
    CacheURLs = {}
    Out = []
    OutReal = []
    Urls = []
    OutRealButActuallyThisTime: dict[str, list[dict[str, dict[str, str]]]] = {}

    Web = Req.get('https://maniaplanet.com/channels/trackmania' if not Shootmania else 'https://maniaplanet.com/channels/shootmania')
    S = BeautifulSoup(Web.text, 'lxml') 
    Tags = S.select("table")[0].select("a")

    for Elem in Tags:
        Out.append(int(Elem.attrs["href"][-3:].replace("/", "")))

    for Num in Out:
        Temp = ""

        CacheURLs[str(Num)] = GetImageURLFromChannelIdS(Num)
        Urls.append(CacheURLs[str(Num)])

        Web = Req.get(f'https://maniaplanet.com/channels/programs/{Num}')
        S = BeautifulSoup(Web.text, 'lxml') 
        Tag = S.select("div.card-footer")[0].select("a")[0].select("span")[0]
        Tog = Tag.children
        for Elem in Tog:
            Temp += Elem.get_text()
        CacheNames[str(Num)] = Temp
        OutReal.append(Temp)
    
    OutReal = numpy.reshape(OutReal, (24, 7))
    Urls = numpy.reshape(Urls, (24, 7))

    for I in range(24):
        for J in range(7):
            try:
                OutRealButActuallyThisTime[J].append({str(I): {OutReal[I][J]: Urls[I][J]}})
            except:
                OutRealButActuallyThisTime[J] = [{str(I): {OutReal[I][J]: Urls[I][J]}}]
        
            OutRealButActuallyThisTime[J].sort(key=lambda Y: int(list(Y)[0]))

    return OutRealButActuallyThisTime

def GetScheduleA(Shootmania: bool = False):
    # curl -H 'User-Agent: ManiaPlanet 4.1' -H 'Content-Type: application/json' -H 'Accept: application/json' -H '' -g 'https://prod.live.maniaplanet.com/ingame/public/channels?uid[]=trackmania&uid[]=shootmania'
    Headers = {
        'User-Agent': 'ManiaPlanet 4.1',
        'From': 'jailmanguy1@gmail.com',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    Query = {
        "uid[]": "shootmania" if Shootmania else "trackmania"
    }
    Web = Req.get('https://prod.live.maniaplanet.com/ingame/public/channels/schedule2', headers=Headers, params=Query)
    Json = Web.json()
    SortedArrSched = numpy.reshape(Json, (7, 24))
    return SortedArrSched.tolist()

def GetChannelA(Shootmania: bool = False):
    from datetime import datetime
    import pytz
    from tzlocal.win32 import get_localzone_name
    from math import floor

    get_localzone_name()
    tz = pytz.timezone(get_localzone_name())
    Offset = (floor(tz.utcoffset(datetime.now()).total_seconds()) // 3600) - 1
    Day = datetime.now(tz=tz).weekday()
    Hour = datetime.now(tz=tz).hour

    def Shift(i: int, al: list):
        temp = al.copy()
        for _ in range(i):
            x = temp[0]; temp.remove(x); temp.append(x)
        return temp

    def RShift(i: int, al: list):
        temp = al.copy()
        for _ in range(i):
            temp = temp[::-1]; x = temp[0]; temp.remove(x); temp.append(x); temp = temp[::-1]
        return temp

    def ShiftA(i: int, al: list):
        if i < 0:
            return RShift(abs(i), al)
        return Shift(i, al)
    
    return ShiftA(-Offset, GetScheduleA(Shootmania=Shootmania)[Day])[Hour]

def GetTitleDownloadLinkA(TitleID: str):
    Web = Req.get(f"https://maniaplanet.com/webservices/titles/{TitleID}")
    return Web.json()["download_url"]

def IdExists(Id: int = 1):
    Web = Req.get(f'https://maniaplanet.com/channels/programs/{Id}')
    if Web.status_code == 200:
        return True
    return False