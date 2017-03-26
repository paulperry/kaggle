# This is a script which discloses spell corrections we used in our work
# Team: Turing test (Igor Buinyi, Kostia Omelianchuk, Chenglong Chen)

import numpy as np 
import pandas as pd 
import re

# Input data files are available in the "../input/" directory.
df_train = pd.read_csv('../input/train.csv', encoding="ISO-8859-1")[:3000] #update here
df_test = pd.read_csv('../input/test.csv', encoding="ISO-8859-1")[:1000] #update here
num_train = df_train.shape[0]
df_all = pd.concat((df_train, df_test), axis=0, ignore_index=True)

## This function perfroms spell correction. 
## It may take other automatically engineered dictionary as an additional input.
def spell_correction(s, automatic_spell_check_dict={}):
    s = s.replace("craftsm,an","craftsman")        
    s = re.sub(r'depot.com/search=', '', s)
    s = re.sub(r'pilers,needlenose', 'pliers, needle nose', s)    
    
    s=s.replace("ttt","tt")    
    s=s.replace("lll","ll") 
    s=s.replace("nnn","nn") 
    s=s.replace("rrr","rr") 
    s=s.replace("sss","ss") 
    s=s.replace("zzz","zz")
    s=s.replace("ccc","cc")
    s=s.replace("eee","ee")
    
    s=s.replace("acccessories","accessories")
    s=re.sub(r'\bscott\b', 'scotts', s) #brand
    s=re.sub(r'\borgainzer\b', 'organizer', s)
    s=re.sub(r'\bshark bite\b', 'sharkbite',s)
    
    s=s.replace("hinges with pishinges with pins","hinges with pins")    
    s=s.replace("virtue usa","virtu usa")
    s=re.sub('outdoor(?=[a-rt-z])', 'outdoor ', s)
    s=re.sub(r'\bdim able\b',"dimmable", s) 
    s=re.sub(r'\blink able\b',"linkable", s)
    s=re.sub(r'\bm aple\b',"maple", s)
    s=s.replace("aire acondicionado", "air conditioner")
    s=s.replace("borsh in dishwasher", "bosch dishwasher")
    s=re.sub(r'\bapt size\b','appartment size', s)
    s=re.sub(r'\barm[e|o]r max\b','armormax', s)
    s=re.sub(r' ss ',' stainless steel ', s)
    s=re.sub(r'\bmay tag\b','maytag', s)
    s=re.sub(r'\bback blash\b','backsplash', s)
    s=re.sub(r'\bbum boo\b','bamboo', s)
    s=re.sub(r'(?<=[0-9] )but\b','btu', s)
    s=re.sub(r'\bcharbroi l\b','charbroil', s)
    s=re.sub(r'\bair cond[it]*\b','air conditioner', s)
    s=re.sub(r'\bscrew conn\b','screw connector', s)
    s=re.sub(r'\bblack decker\b','black and decker', s)
    s=re.sub(r'\bchristmas din\b','christmas dinosaur', s)
    s=re.sub(r'\bdoug fir\b','douglas fir', s)
    s=re.sub(r'\belephant ear\b','elephant ears', s)
    s=re.sub(r'\bt emp gauge\b','temperature gauge', s)
    s=re.sub(r'\bsika felx\b','sikaflex', s)
    s=re.sub(r'\bsquare d\b', 'squared', s)
    s=re.sub(r'\bbehring\b', 'behr', s)
    s=re.sub(r'\bcam\b', 'camera', s)
    s=re.sub(r'\bjuke box\b', 'jukebox', s)
    s=re.sub(r'\brust o leum\b', 'rust oleum', s)
    s=re.sub(r'\bx mas\b', 'christmas', s)
    s=re.sub(r'\bmeld wen\b', 'jeld wen', s)
    s=re.sub(r'\bg e\b', 'ge', s)
    s=re.sub(r'\bmirr edge\b', 'mirredge', s)
    s=re.sub(r'\bx ontrol\b', 'control', s)
    s=re.sub(r'\boutler s\b', 'outlets', s)
    s=re.sub(r'\bpeep hole', 'peephole', s)
    s=re.sub(r'\bwater pik\b', 'waterpik', s)
    s=re.sub(r'\bwaterpi k\b', 'waterpik', s)
    s=re.sub(r'\bplex[iy] glass\b', 'plexiglass', s)
    s=re.sub(r'\bsheet rock\b', 'sheetrock',s)
    s=re.sub(r'\bgen purp\b', 'general purpose',s)
    s=re.sub(r'\bquicker crete\b', 'quikrete',s)
    s=re.sub(r'\bref ridge\b', 'refrigerator',s)
    s=re.sub(r'\bshark bite\b', 'sharkbite',s)
    s=re.sub(r'\buni door\b', 'unidoor',s)
    s=re.sub(r'\bair tit\b','airtight', s)
    s=re.sub(r'\bde walt\b','dewalt', s)
    s=re.sub(r'\bwaterpi k\b','waterpik', s)
    s=re.sub(r'\bsaw za(ll|w)\b','sawzall', s)
    s=re.sub(r'\blg elec\b', 'lg', s)
    s=re.sub(r'\bhumming bird\b', 'hummingbird', s)
    s=re.sub(r'\bde ice(?=r|\b)', 'deice',s)  
    s=re.sub(r'\bliquid nail\b', 'liquid nails', s)  
    s=re.sub(r'\bdeck over\b','deckover', s)
    s=re.sub(r'\bcounter sink(?=s|\b)','countersink', s)
    s=re.sub(r'\bpipes line(?=s|\b)','pipeline', s)
    s=re.sub(r'\bbook case(?=s|\b)','bookcase', s)
    s=re.sub(r'\bwalkie talkie\b','2 pair radio', s)
    s=re.sub(r'(?<=^)ks\b', 'kwikset',s)
    s=re.sub('(?<=[0-9])[\ ]*ft(?=[a-z])', 'ft ', s)
    s=re.sub('(?<=[0-9])[\ ]*mm(?=[a-z])', 'mm ', s)
    s=re.sub('(?<=[0-9])[\ ]*cm(?=[a-z])', 'cm ', s)
    s=re.sub('(?<=[0-9])[\ ]*inch(es)*(?=[a-z])', 'in ', s)
    
    s=re.sub(r'(?<=[1-9]) pac\b', 'pack', s)
 
    s=re.sub(r'\bcfl bulbs\b', 'cfl light bulbs', s)
    s=re.sub(r' cfl(?=$)', ' cfl light bulb', s)
    s=re.sub(r'candelabra cfl 4 pack', 'candelabra cfl light bulb 4 pack', s)
    s=re.sub(r'\bthhn(?=$|\ [0-9]|\ [a-rtuvx-z])', 'thhn wire', s)
    s=re.sub(r'\bplay ground\b', 'playground',s)
    s=re.sub(r'\bemt\b', 'emt electrical metallic tube',s)
    s=re.sub(r'\boutdoor dining se\b', 'outdoor dining set',s)
    
     
    if "a/c" in s:
        if ('unit' in s) or ('frost' in s) or ('duct' in s) or ('filt' in s) or ('vent' in s) or ('clean' in s) or ('vent' in s) or ('portab' in s):
            s=s.replace("a/c","air conditioner")
        else:
            s=s.replace("a/c","ac")

   
    external_data_dict={'airvents': 'air vents', 
    'antivibration': 'anti vibration', 
    'autofeeder': 'auto feeder', 
    'backbrace': 'back brace', 
    'behroil': 'behr oil', 
    'behrwooden': 'behr wooden', 
    'brownswitch': 'brown switch', 
    'byefold': 'bifold', 
    'canapu': 'canopy', 
    'cleanerakline': 'cleaner alkaline',
    'colared': 'colored', 
    'comercialcarpet': 'commercial carpet', 
    'dcon': 'd con', 
    'doorsmoocher': 'door smoocher', 
    'dreme': 'dremel', 
    'ecobulb': 'eco bulb', 
    'fantdoors': 'fan doors', 
    'gallondrywall': 'gallon drywall', 
    'geotextile': 'geo textile', 
    'hallodoor': 'hallo door', 
    'heatgasget': 'heat gasket', 
    'ilumination': 'illumination', 
    'insol': 'insulation', 
    'instock': 'in stock', 
    'joisthangers': 'joist hangers', 
    'kalkey': 'kelkay', 
    'kohlerdrop': 'kohler drop', 
    'kti': 'kit', 
    'laminet': 'laminate', 
    'mandoors': 'main doors', 
    'mountspacesaver': 'mount space saver', 
    'reffridge': 'refrigerator', 
    'refrig': 'refrigerator', 
    'reliabilt': 'reliability', 
    'replaclacemt': 'replacement', 
    'searchgalvanized': 'search galvanized', 
    'seedeater': 'seed eater', 
    'showerstorage': 'shower storage', 
    'straitline': 'straight line', 
    'subpumps': 'sub pumps', 
    'thromastate': 'thermostat', 
    'topsealer': 'top sealer', 
    'underlay': 'underlayment',
    'vdk': 'bdk', 
    'wallprimer': 'wall primer', 
    'weedbgon': 'weed b gon', 
    'weedeaters': 'weed eaters', 
    'weedwacker': 'weed wacker', 
    'wesleyspruce': 'wesley spruce', 
    'worklite': 'work light'}
     
    for word in external_data_dict.keys():
        s=re.sub(r'\b'+word+r'\b',external_data_dict[word], s)
        
    ############ replace words from dict
    for word in automatic_spell_check_dict.keys():
        s=re.sub(r'\b'+word+r'\b',automatic_spell_check_dict[word], s)
           
    return s

##### end of dunction 'spell_correction'
############################################


### another replacement dict used independently
another_replacement_dict={"undercabinet": "under cabinet", 
"snowerblower": "snower blower", 
"mountreading": "mount reading", 
"zeroturn": "zero turn", 
"stemcartridge": "stem cartridge", 
"greecianmarble": "greecian marble", 
"outdoorfurniture": "outdoor furniture", 
"outdoorlounge": "outdoor lounge", 
"heaterconditioner": "heater conditioner", 
"heater/conditioner": "heater conditioner", 
"conditioner/heater": "conditioner heater", 
"airconditioner": "air conditioner", 
"snowbl": "snow bl", 
"plexigla": "plexi gla", 
"whirlpoolga": "whirlpool ga", 
"whirlpoolstainless": "whirlpool stainless", 
"sedgehamm": "sledge hamm", 
"childproof": "child proof", 
"flatbraces": "flat braces", 
"zmax": "z max", 
"gal vanized": "galvanized", 
"battery powere weedeater": "battery power weed eater", 
"shark bite": "sharkbite", 
"rigid saw": "ridgid saw", 
"black decke": "black and decker", 
"exteriorpaint": "exterior paint", 
"fuelpellets": "fuel pellet", 
"cabinetwithouttops": "cabinet without tops", 
"castiron": "cast iron", 
"pfistersaxton": "pfister saxton ", 
"splitbolt": "split bolt", 
"soundfroofing": "sound froofing", 
"cornershower": "corner shower", 
"stronglus": "strong lus", 
"shopvac": "shop vac", 
"shoplight": "shop light", 
"airconditioner": "air conditioner", 
"whirlpoolga": "whirlpool ga", 
"whirlpoolstainless": "whirlpool stainless", 
"snowblower": "snow blower", 
"plexigla": "plexi gla", 
"trashcan": "trash can", 
"mountspacesaver": "mount space saver", 
"undercounter": "under counter", 
"stairtreads": "stair tread", 
"techni soil": "technisoil", 
"in sulated": "insulated", 
"closet maid": "closetmaid", 
"we mo": "wemo", 
"weather tech": "weathertech", 
"weather vane": "weathervane", 
"versa tube": "versatube", 
"versa bond": "versabond", 
"in termatic": "intermatic", 
"therma cell": "thermacell", 
"tuff screen": "tuffscreen", 
"sani flo": "saniflo", 
"timber lok": "timberlok", 
"thresh hold": "threshold", 
"yardguard": "yardgard", 
"incyh": "in.", 
"diswasher": "dishwasher", 
"closetmade": "closetmaid", 
"repir": "repair", 
"handycap": "handicap", 
"toliet": "toilet", 
"conditionar": "conditioner", 
"aircondition": "air conditioner", 
"aircondiioner": "air conditioner", 
"comercialcarpet": "commercial carpet", 
"commercail": "commercial", 
"inyl": "vinyl", 
"vinal": "vinyl", 
"vynal": "vinyl", 
"vynik": "vinyl", 
"skill": "skil", 
"whirpool": "whirlpool", 
"glaciar": "glacier", 
"glacie": "glacier", 
"rheum": "rheem", 
"one+": "1", 
"toll": "tool", 
"ceadar": "cedar", 
"shelv": "shelf", 
"toillet": "toilet", 
"toiet": "toilet", 
"toilest": "toilet", 
"toitet": "toilet", 
"ktoilet": "toilet", 
"tiolet": "toilet", 
"tolet": "toilet", 
"eater": "heater", 
"robi": "ryobi", 
"robyi": "ryobi", 
"roybi": "ryobi", 
"rayobi": "ryobi", 
"riobi": "ryobi", 
"screww": "screw", 
"stailess": "stainless", 
"dor": "door", 
"vaccuum": "vacuum", 
"vacum": "vacuum", 
"vaccum": "vacuum", 
"vinal": "vinyl", 
"vynal": "vinyl", 
"vinli": "vinyl", 
"viyl": "vinyl", 
"vynil": "vinyl", 
"vlave": "valve", 
"vlve": "valve", 
"walll": "wall", 
"steal": "steel", 
"stell": "steel", 
"pcv": "pvc", 
"blub": "bulb", 
"ligt": "light", 
"bateri": "battery", 
"kolher": "kohler", 
"fame": "frame", 
"have": "haven", 
"acccessori": "accessory", 
"accecori": "accessory", 
"accesnt": "accessory", 
"accesor": "accessory", 
"accesori": "accessory", 
"accesorio": "accessory", 
"accessori": "accessory", 
"repac": "replacement", 
"repalc": "replacement", 
"repar": "repair", 
"repir": "repair", 
"replacemet": "replacement", 
"replacemetn": "replacement", 
"replacemtn": "replacement", 
"replaclacemt": "replacement", 
"replament": "replacement", 
"toliet": "toilet", 
"skill": "skil", 
"whirpool": "whirlpool", 
"stailess": "stainless", 
"stainlss": "stainless", 
"stainstess": "stainless", 
"jigsaww": "jig saw", 
"woodwen": "wood", 
"pywood": "plywood", 
"woodebn": "wood", 
"repellant": "repellent", 
"concret": "concrete", 
"windos": "window", 
"wndows": "window", 
"wndow": "window", 
"winow": "window", 
"caamera": "camera", 
"sitch": "switch", 
"doort": "door", 
"coller": "cooler", 
"flasheing": "flashing", 
"wiga": "wigan", 
"bathroon": "bath room", 
"sinl": "sink", 
"melimine": "melamine", 
"inyrtior": "interior", 
"tilw": "tile", 
"wheelbarow": "wheelbarrow", 
"pedistal": "pedestal", 
"submerciable": "submercible", 
"weldn": "weld", 
"contaner": "container", 
"webmo": "wemo", 
"genis": "genesis", 
"waxhers": "washer", 
"softners": "softener", 
"sofn": "softener", 
"connecter": "connector", 
"heather": "heater", 
"heatere": "heater", 
"electic": "electric", 
"quarteround": "quarter round", 
"bprder": "border", 
"pannels": "panel", 
"framelessmirror": "frameless mirror", 
"paneling": "panel", 
"controle": "control", 
"flurescent": "fluorescent", 
"flourescent": "fluorescent", 
"molding": "moulding", 
"lattiace": "lattice", 
"barackets": "bracket", 
"vintemp": "vinotemp", 
"vetical": "vertical", 
"verticle": "vertical", 
"vesel": "vessel", 
"versatiube": "versatube", 
"versabon": "versabond", 
"dampr": "damper", 
"vegtable": "vegetable", 
"plannter": "planter", 
"fictures": "fixture", 
"mirros": "mirror", 
"topped": "top", 
"preventor": "breaker", 
"traiter": "trailer", 
"ureka": "eureka", 
"uplihght": "uplight", 
"upholstry": "upholstery", 
"untique": "antique", 
"unsulation": "insulation", 
"unfinushed": "unfinished", 
"verathane": "varathane", 
"ventenatural": "vent natural", 
"shoer": "shower", 
"floorong": "flooring", 
"tsnkless": "tankless", 
"tresers": "dresers", 
"treate": "treated", 
"transparant": "transparent", 
"transormations": "transformation", 
"mast5er": "master", 
"anity": "vanity", 
"tomostat": "thermostat", 
"thromastate": "thermostat", 
"kphler": "kohler", 
"tji": "tpi", 
"cuter": "cutter", 
"medalions": "medallion", 
"tourches": "torch", 
"tighrner": "tightener", 
"thewall": "the wall", 
"thru": "through", 
"wayy": "way", 
"temping": "tamping", 
"outsde": "outdoor", 
"bulbsu": "bulb", 
"ligh": "light", 
"swivrl": "swivel", 
"switchplate": "switch plate", 
"swiss+tech": "swiss tech", 
"sweenys": "sweeney", 
"susbenders": "suspender", 
"cucbi": "cu", 
"gaqs": "gas", 
"structered": "structured", 
"knops": "knob", 
"adopter": "adapter", 
"patr": "part", 
"storeage": "storage", 
"venner": "veneer", 
"veneerstone": "veneer stone", 
"stm": "stem", 
"steqamers": "steamer", 
"latter": "ladder", 
"steele": "steel", 
"builco": "bilco", 
"panals": "panel", 
"grasa": "grass", 
"unners": "runner", 
"maogani": "maogany", 
"sinl": "sink", 
"grat": "grate", 
"showerheards": "shower head", 
"spunge": "sponge", 
"conroller": "controller", 
"cleanerm": "cleaner", 
"preiumer": "primer", 
"fertillzer": "fertilzer", 
"spectrazide": "spectracide", 
"spaonges": "sponge", 
"stoage": "storage", 
"sower": "shower", 
"solor": "solar", 
"sodering": "solder", 
"powerd": "powered", 
"lmapy": "lamp", 
"naturlas": "natural", 
"sodpstone": "soapstone", 
"punp": "pump", 
"blowerr": "blower", 
"medicn": "medicine", 
"slidein": "slide", 
"sjhelf": "shelf", 
"oard": "board", 
"singel": "single", 
"paintr": "paint", 
"silocoln": "silicon", 
"poinsetia": "poinsettia", 
"sammples": "sample", 
"sidelits": "sidelight", 
"nitch": "niche", 
"pendent": "pendant", 
"shopac": "shop vac", 
"shoipping": "shopping", 
"shelfa": "shelf", 
"cabi": "cabinet", 
"nails18": "nail", 
"dewaqlt": "dewalt", 
"barreir": "barrier", 
"ilumination": "illumination", 
"mortice": "mortise", 
"lumes": "lumen", 
"blakck": "black", 
"exterieur": "exterior", 
"expsnsion": "expansion", 
"air condit$": "air conditioner", 
"double pole type chf breaker": "double pole type ch breaker", 
"mast 5 er": "master", 
"toilet rak": "toilet rack", 
"govenore": "governor", 
"in wide": "in white", 
"shepard hook": "shepherd hook", 
"frost fee": "frost free", 
"kitchen aide": "kitchen aid", 
"saww horse": "saw horse", 
"weather striping": "weatherstripper", 
"'girls": "girl", 
"girl's": "girl", 
"girls'": "girl", 
"girls": "girl", 
"girlz": "girl", 
"boy's": "boy", 
"boys'": "boy", 
"boys": "boy", 
"men's": "man", 
"mens'": "man", 
"mens": "mam", 
"men": "man", 
"women's": "woman", 
"womens'": "woman", 
"womens": "woman", 
"women": "woman", 
"kid's": "kid", 
"kids'": "kid", 
"kids": "kid", 
"children's": "kid", 
"childrens'": "kid", 
"childrens": "kid", 
"children": "kid", 
"child": "kid", 
"bras": "bra", 
"bicycles": "bike", 
"bicycle": "bike", 
"bikes": "bike", 
"refridgerators": "fridge", 
"refrigerator": "fridge", 
"refrigirator": "fridge", 
"freezer": "fridge", 
"memories": "memory", 
"fragance": "perfume", 
"fragrance": "perfume", 
"cologne": "perfume", 
"anime": "animal", 
"assassinss": "assassin", 
"assassin's": "assassin", 
"assassins": "assassin", 
"bedspreads": "bedspread", 
"shoppe": "shop", 
"extenal": "external", 
"knives": "knife", 
"kitty's": "kitty", 
"levi's": "levi", 
"squared": "square", 
"rachel": "rachael", 
"rechargable": "rechargeable", 
"batteries": "battery", 
"seiko's": "seiko", 
"ounce": "oz"
}
#### end of anoter_replacent_dict


valuable_words_list=['tv','downrod', 'sillcock', 'shelving', 'luminaire', 'paracord', 'ducting', \
    'recyclamat', 'rebar', 'spackling', 'hoodie', 'placemat', 'innoculant', 'protectant', \
    'colorant', 'penetrant', 'attractant', 'bibb', 'nosing', 'subflooring', 'torchiere', 'thhn',\
    'lantern','epoxy','cloth','trim','adhesive','light','lights','saw','pad','polish','nose','stove',\
    'elbow','elbows','lamp','door','doors','pipe','bulb','wood','woods','wire','sink','hose','tile','bath','table','duct',\
    'windows','mesh','rug','rugs','shower','showers','wheels','fan','lock','rod','mirror','cabinet','shelves','paint',\
    'plier','pliers','set','screw','lever','bathtub','vacuum','nut', 'nipple','straw','saddle','pouch','underlayment',\
    'shade','top', 'bulb', 'bulbs', 'paint', 'oven', 'ranges', 'sharpie', 'shed', 'faucet',\
    'finish','microwave', 'can', 'nozzle', 'grabber', 'tub', 'angles','showerhead', 'dehumidifier', \
    'shelving', 'urinal', 'mdf']

not_so_valuable_words_list= ['aaa','off','impact','square','shelves','finish','ring','flood','dual','ball','cutter',\
'max','off','mat','allure','diamond','drive', 'edge','anchor','walls','universal','cat', 'dawn','ion','daylight',\
'roman', 'weed eater', 'restore', 'design', 'caddy', 'pole caddy', 'jet', 'classic', 'element', 'aqua',\
'terra', 'decora', 'ez', 'briggs', 'wedge', 'sunbrella',  'adorne', 'santa', 'bella', 'duck', 'hotpoint',\
'duck', 'tech', 'titan', 'powerwasher', 'cooper lighting', 'heritage', 'imperial', 'monster', 'peak', 
'bell', 'drive', 'trademark', 'toto', 'champion', 'shop vac', 'lava', 'jet', 'flood', \
'roman', 'duck', 'magic', 'allen', 'bunn', 'element', 'international', 'larson', 'tiki', 'titan', \
 'space saver', 'cutter', 'scotch', 'adorne', 'ball', 'sunbeam', 'fatmax', 'poulan', 'ring', 'sparkle', 'bissell', \
 'universal', 'paw', 'wedge', 'restore', 'daylight', 'edge', 'americana', 'wacker', 'cat', 'allure', 'bonnie plants', \
 'troy', 'impact', 'buffalo', 'adams', 'jasco', 'rapid dry', 'aaa', 'pole caddy', 'pac', 'seymour', 'mobil', \
 'mastercool', 'coca cola', 'timberline', 'classic', 'caddy', 'sentry', 'terrain', 'nautilus', 'precision', \
 'artisan', 'mural', 'game', 'royal', 'use', 'dawn', 'task', 'american line', 'sawtrax', 'solo', 'elements', \
 'summit', 'anchor', 'off', 'spruce', 'medina', 'shoulder dolly', 'brentwood', 'alex', 'wilkins', 'natural magic', \
 'kodiak', 'metro', 'shelter', 'centipede', 'imperial', 'cooper lighting', 'exide', 'bella', 'ez', 'decora', \
 'terra', 'design', 'diamond', 'mat', 'finish', 'tilex', 'rhino', 'crock pot', 'legend', 'leatherman', 'remove', \
 'architect series', 'greased lightning', 'castle', 'spirit', 'corian', 'peak', 'monster', 'heritage', 'powerwasher',\
 'reese', 'tech', 'santa', 'briggs', 'aqua', 'weed eater', 'ion', 'walls', 'max', 'dual', 'shelves', 'square',\
 'hickory', "vikrell", "e3", "pro series", "keeper", "coastal shower doors", 'cadet','church','gerber','glidden',\
 'cooper wiring devices', 'border blocks', 'commercial electric', 'pri','exteria','extreme', 'veranda',\
 'gorilla glue','gorilla','shark','wen']

not_so_valuable_words_list+=['free','height', 'width', 'depth', 'model','pcs', 'thick','pack','adhesive','steel','cordless', 'aaa' 'b', 'nm', 'hc', 'insulated','gll', 'nutmeg',\
    'pnl', 'sotc','withe','stainless','chrome','beige','max','acrylic', 'cognac', 'cherry', 'ivory','electric','fluorescent', 'recessed', 'matte',\
    'propane','sku','brushless','quartz','gfci','shut','sds','value','brown','white','black','red','green','yellow','blue','silver','pink',\
    'gray','gold','thw','medium','type','flush',"metaliks", 'metallic', 'amp','btu','gpf','pvc','mil','gcfi','plastic', 'vinyl','aaa',\
    'aluminum','brass','antique', 'brass','copper','nickel','satin','rubber','porcelain','hickory','marble','polyacrylic','golden','fiberglass',\
    'nylon','lmapy','maple','polyurethane','mahogany','enamel', 'enameled', 'linen','redwood', 'sku','oak','quart','abs','travertine', 'resin',\
    'birch','birchwood','zinc','pointe','polycarbonate', 'ash', 'wool', 'rockwool', 'teak','alder','frp','cellulose','abz', 'male', 'female', 'used',\
    'hepa','acc','keyless','aqg','arabesque','polyurethane', 'polyurethanes','ardex','armorguard','asb', 'motion','adorne','fatpack',\
    'fatmax','feet','ffgf','fgryblkg', 'douglas', 'fir', 'fleece','abba', 'nutri', 'thermal','thermoclear', 'heat', 'water', 'systemic',\
    'heatgasget', 'cool', 'fusion', 'awg', 'par', 'parabolic', 'tpi', 'pint', 'draining', 'rain', 'cost', 'costs', 'costa','ecostorage',
    'mtd', 'pass', 'emt', 'jeld', 'npt', 'sch', 'pvc', 'dusk', 'dawn', 'lathe','lows','pressure', 'round', 'series','impact', 'resistant','outdoor',\
    'off', 'sawall', 'elephant', 'ear', 'abb', 'baby', 'feedback', 'fastback','jumbo', 'flexlock', 'instant', 'natol', 'naples','florcant',\
    'canna','hammock', 'jrc', 'honeysuckle', 'honey', 'serrano','sequoia', 'amass', 'ashford', 'gal','gas', 'gasoline', 'compane','occupancy',\
    'home','bakeware', 'lite', 'lithium', 'golith','gxwh',  'wht', 'heirloom', 'marine', 'marietta', 'cambria', 'campane','birmingham',\
    'bellingham','chamois', 'chamomile', 'chaosaw', 'chanpayne', 'thats', 'urethane', 'champion', 'chann', 'mocha', 'bay', 'rough',\
    'undermount', 'price', 'prices', 'way', 'air', 'bazaar', 'broadway', 'driveway', 'sprayway', 'subway', 'flood', 'slate', 'wet',\
    'clean', 'tweed', 'weed', 'cub', 'barb', 'salem', 'sale', 'sales', 'slip', 'slim', 'gang', 'office', 'allure', 'bronze', 'banbury',\
    'tuscan','tuscany', 'refinishing', 'fleam','schedule', 'doeskin','destiny', 'mean', 'hide', 'bobbex', 'pdi', 'dpdt', 'tri', 'order',\
    'kamado','seahawks','weymouth', 'summit','tel','riddex', 'alick','alvin', 'ano', 'assy', 'grade', 'barranco', 'batte','banbury',\
    'mcmaster', 'carr', 'ccl', 'china', 'choc', 'colle', 'cothom', 'cucbi', 'cuv', 'cwg', 'cylander', 'cylinoid', 'dcf', 'number', 'ultra',\
    'diat','discon', 'disconnect', 'plantation', 'dpt', 'duomo', 'dupioni', 'eglimgton', 'egnighter','ert','euroloft', 'everready',\
    'felxfx', 'financing', 'fitt', 'fosle', 'footage', 'gpf','fro', 'genis', 'giga', 'glu', 'gpxtpnrf', 'size', 'hacr', 'hardw',\
    'hexagon', 'hire', 'hoo','number','cosm', 'kelston', 'kind', 'all', 'semi', 'gloss', 'lmi', 'luana', 'gdak', 'natol', 'oatu',\
    'oval', 'olinol', 'pdi','penticlea', 'portalino', 'racc', 'rads', 'renat', 'roc', 'lon', 'sendero', 'adora', 'sleave', 'swu',
    'tilde', 'cordoba', 'tuvpl','yel', 'acacia','mig','parties','alkaline','plexiglass', 'iii', 'watt']


## example of usage
df_all['search_term_replaced'] = df_all['search_term'].map(lambda x:spell_correction(x))
print(df_all[['search_term','search_term_replaced']][2705:2707])

df_all['search_term_replaced'] = df_all['search_term_replaced'].map(lambda x: " ".join(\
        [another_replacement_dict[w] if w in another_replacement_dict.keys() else w \
         for w in x.split()]))
print(df_all[['search_term','search_term_replaced']][1923:1925])


print(df_all['search_term'][200:203].map(lambda x: max([int(w in valuable_words_list) for w in x.split()]) ))

print(df_all['search_term'][1216:1219].map(lambda x: max([int(w in not_so_valuable_words_list) for w in x.split()]) ))