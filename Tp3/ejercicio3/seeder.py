from continente import Continente
from pais import Pais
from provincia import Provincia


def inicializar_datos():
    america = Continente("america")
    europa = Continente("europa")

    # ── SUDAMÉRICA ───────────────────────────────────────────────────────────
    argentina = Pais("Argentina", "Buenos Aires", 2780400)
    for p in ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Tucumán",
              "Salta", "Misiones", "Chaco", "Entre Ríos", "Corrientes",
              "Santiago del Estero", "San Juan", "Jujuy", "Río Negro",
              "Neuquén", "Formosa", "Chubut", "San Luis", "Catamarca",
              "La Rioja", "La Pampa", "Santa Cruz", "Tierra del Fuego",
              "Ciudad Autónoma de Buenos Aires"]:
        argentina.agregar_provincia(Provincia(p))

    brasil = Pais("Brasil", "Brasilia", 8515767)
    for p in ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia", "Paraná",
              "Rio Grande do Sul", "Santa Catarina", "Pernambuco", "Ceará",
              "Goiás", "Pará", "Maranhão", "Amazonas", "Mato Grosso",
              "Mato Grosso do Sul", "Espírito Santo", "Alagoas", "Piauí",
              "Rio Grande do Norte", "Paraíba", "Sergipe", "Rondônia",
              "Tocantins", "Amapá", "Roraima", "Acre", "Distrito Federal"]:
        brasil.agregar_provincia(Provincia(p))

    chile = Pais("Chile", "Santiago", 756102)
    for p in ["Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama",
              "Coquimbo", "Valparaíso", "Metropolitana de Santiago", "O'Higgins",
              "Maule", "Ñuble", "Biobío", "La Araucanía", "Los Ríos",
              "Los Lagos", "Aysén", "Magallanes"]:
        chile.agregar_provincia(Provincia(p))

    uruguay = Pais("Uruguay", "Montevideo", 176215)
    for p in ["Montevideo", "Canelones", "Maldonado", "Rocha", "Treinta y Tres",
              "Cerro Largo", "Rivera", "Artigas", "Salto", "Paysandú",
              "Río Negro", "Soriano", "Colonia", "San José", "Flores",
              "Florida", "Lavalleja", "Durazno", "Tacuarembó"]:
        uruguay.agregar_provincia(Provincia(p))

    paraguay = Pais("Paraguay", "Asunción", 406752)
    for p in ["Asunción", "Alto Paraguay", "Alto Paraná", "Amambay", "Boquerón",
              "Caaguazú", "Caazapá", "Canindeyú", "Central", "Concepción",
              "Cordillera", "Guairá", "Itapúa", "Misiones", "Ñeembucú",
              "Paraguarí", "Presidente Hayes", "San Pedro"]:
        paraguay.agregar_provincia(Provincia(p))

    bolivia = Pais("Bolivia", "Sucre", 1098581)
    for p in ["La Paz", "Cochabamba", "Santa Cruz", "Oruro", "Potosí",
              "Chuquisaca", "Tarija", "Beni", "Pando"]:
        bolivia.agregar_provincia(Provincia(p))

    peru = Pais("Perú", "Lima", 1285216)
    for p in ["Lima", "Arequipa", "La Libertad", "Piura", "Cajamarca",
              "Puno", "Junín", "Cusco", "Áncash", "Loreto",
              "Lambayeque", "Tacna", "Ica", "San Martín", "Ucayali",
              "Ayacucho", "Huánuco", "Huancavelica", "Apurímac",
              "Madre de Dios", "Amazonas", "Tumbes", "Pasco", "Moquegua"]:
        peru.agregar_provincia(Provincia(p))

    colombia = Pais("Colombia", "Bogotá", 1141748)
    for p in ["Bogotá D.C.", "Antioquia", "Valle del Cauca", "Cundinamarca",
              "Atlántico", "Bolívar", "Magdalena", "Nariño", "Córdoba",
              "Santander", "Norte de Santander", "Cauca", "Boyacá",
              "Huila", "Tolima", "Meta", "Risaralda", "Caldas",
              "Quindío", "Sucre", "César", "La Guajira", "Caquetá",
              "Arauca", "Casanare", "Putumayo", "Chocó", "Amazonas"]:
        colombia.agregar_provincia(Provincia(p))

    venezuela = Pais("Venezuela", "Caracas", 916445)
    for p in ["Amazonas", "Anzoátegui", "Apure", "Aragua", "Barinas",
              "Bolívar", "Carabobo", "Cojedes", "Delta Amacuro", "Falcón",
              "Guárico", "Lara", "Mérida", "Miranda", "Monagas",
              "Nueva Esparta", "Portuguesa", "Sucre", "Táchira",
              "Trujillo", "Vargas", "Yaracuy", "Zulia", "Distrito Capital"]:
        venezuela.agregar_provincia(Provincia(p))

    ecuador = Pais("Ecuador", "Quito", 283561)
    for p in ["Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo",
              "Cotopaxi", "El Oro", "Esmeraldas", "Galápagos", "Guayas",
              "Imbabura", "Loja", "Los Ríos", "Manabí", "Morona Santiago",
              "Napo", "Orellana", "Pastaza", "Pichincha", "Santa Elena",
              "Santo Domingo", "Sucumbíos", "Tungurahua", "Zamora Chinchipe"]:
        ecuador.agregar_provincia(Provincia(p))

    guyana = Pais("Guyana", "Georgetown", 214969)
    for p in ["Barima-Waini", "Cuyuni-Mazaruni", "Demerara-Mahaica",
              "East Berbice-Corentyne", "Essequibo Islands", "Mahaica-Berbice",
              "Pomeroon-Supenaam", "Potaro-Siparuni", "Upper Demerara",
              "Upper Takutu"]:
        guyana.agregar_provincia(Provincia(p))

    suriname = Pais("Surinam", "Paramaribo", 163820)
    for p in ["Brokopondo", "Commewijne", "Coronie", "Marowijne",
              "Nickerie", "Para", "Paramaribo", "Saramacca",
              "Sipaliwini", "Wanica"]:
        suriname.agregar_provincia(Provincia(p))

    # ── NORTEAMÉRICA ─────────────────────────────────────────────────────────
    usa = Pais("Estados Unidos", "Washington D.C.", 9833517)
    for p in ["Alabama", "Alaska", "Arizona", "Arkansas", "California",
              "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
              "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
              "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
              "Massachusetts", "Michigan", "Minnesota", "Mississippi",
              "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
              "New Jersey", "New Mexico", "New York", "North Carolina",
              "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
              "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
              "Texas", "Utah", "Vermont", "Virginia", "Washington",
              "West Virginia", "Wisconsin", "Wyoming"]:
        usa.agregar_provincia(Provincia(p))

    canada = Pais("Canadá", "Ottawa", 9984670)
    for p in ["Alberta", "Columbia Británica", "Manitoba", "Nuevo Brunswick",
              "Terranova y Labrador", "Territorios del Noroeste",
              "Nueva Escocia", "Nunavut", "Ontario",
              "Isla del Príncipe Eduardo", "Quebec", "Saskatchewan", "Yukón"]:
        canada.agregar_provincia(Provincia(p))

    mexico = Pais("México", "Ciudad de México", 1964375)
    for p in ["Aguascalientes", "Baja California", "Baja California Sur",
              "Campeche", "Chiapas", "Chihuahua", "Ciudad de México",
              "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero",
              "Hidalgo", "Jalisco", "Estado de México", "Michoacán",
              "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
              "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa",
              "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz",
              "Yucatán", "Zacatecas"]:
        mexico.agregar_provincia(Provincia(p))

    # ── CENTROAMÉRICA ────────────────────────────────────────────────────────
    guatemala = Pais("Guatemala", "Ciudad de Guatemala", 108889)
    for p in ["Alta Verapaz", "Baja Verapaz", "Chimaltenango", "Chiquimula",
              "El Progreso", "Escuintla", "Guatemala", "Huehuetenango",
              "Izabal", "Jalapa", "Jutiapa", "Petén", "Quetzaltenango",
              "Quiché", "Retalhuleu", "Sacatepéquez", "San Marcos",
              "Santa Rosa", "Sololá", "Suchitepéquez", "Totonicapán", "Zacapa"]:
        guatemala.agregar_provincia(Provincia(p))

    belize = Pais("Belice", "Belmopán", 22966)
    for p in ["Belice", "Cayo", "Corozal", "Orange Walk", "Stann Creek", "Toledo"]:
        belize.agregar_provincia(Provincia(p))

    honduras = Pais("Honduras", "Tegucigalpa", 112492)
    for p in ["Atlántida", "Choluteca", "Colón", "Comayagua", "Copán",
              "Cortés", "El Paraíso", "Francisco Morazán", "Gracias a Dios",
              "Intibucá", "Islas de la Bahía", "La Paz", "Lempira",
              "Ocotepeque", "Olancho", "Santa Bárbara", "Valle", "Yoro"]:
        honduras.agregar_provincia(Provincia(p))

    el_salvador = Pais("El Salvador", "San Salvador", 21041)
    for p in ["Ahuachapán", "Cabañas", "Chalatenango", "Cuscatlán",
              "La Libertad", "La Paz", "La Unión", "Morazán",
              "San Miguel", "San Salvador", "San Vicente",
              "Santa Ana", "Sonsonate", "Usulután"]:
        el_salvador.agregar_provincia(Provincia(p))

    nicaragua = Pais("Nicaragua", "Managua", 130373)
    for p in ["Boaco", "Carazo", "Chinandega", "Chontales", "Estelí",
              "Granada", "Jinotega", "León", "Madriz", "Managua",
              "Masaya", "Matagalpa", "Nueva Segovia", "Río San Juan",
              "Rivas", "Costa Caribe Norte", "Costa Caribe Sur"]:
        nicaragua.agregar_provincia(Provincia(p))

    costa_rica = Pais("Costa Rica", "San José", 51100)
    for p in ["Alajuela", "Cartago", "Guanacaste", "Heredia",
              "Limón", "Puntarenas", "San José"]:
        costa_rica.agregar_provincia(Provincia(p))

    panama = Pais("Panamá", "Ciudad de Panamá", 75417)
    for p in ["Bocas del Toro", "Chiriquí", "Coclé", "Colón",
              "Darién", "Herrera", "Los Santos", "Panamá",
              "Veraguas", "Panamá Oeste", "Guna Yala"]:
        panama.agregar_provincia(Provincia(p))

    # ── CARIBE ───────────────────────────────────────────────────────────────
    cuba = Pais("Cuba", "La Habana", 109884)
    for p in ["Pinar del Río", "Artemisa", "La Habana", "Mayabeque",
              "Matanzas", "Cienfuegos", "Villa Clara", "Sancti Spíritus",
              "Ciego de Ávila", "Camagüey", "Las Tunas", "Holguín",
              "Granma", "Santiago de Cuba", "Guantánamo", "Isla de la Juventud"]:
        cuba.agregar_provincia(Provincia(p))

    republica_dominicana = Pais("República Dominicana", "Santo Domingo", 48671)
    for p in ["Azua", "Baoruco", "Barahona", "Dajabón", "Distrito Nacional",
              "Duarte", "El Seibo", "Espaillat", "Hato Mayor", "Independencia",
              "La Altagracia", "La Romana", "La Vega", "Monte Cristi",
              "Pedernales", "Peravia", "Puerto Plata", "Samaná",
              "San Cristóbal", "San Juan", "San Pedro de Macorís",
              "Santiago", "Santo Domingo", "Valverde"]:
        republica_dominicana.agregar_provincia(Provincia(p))

    haiti = Pais("Haití", "Puerto Príncipe", 27750)
    for p in ["Artibonite", "Centre", "Grand'Anse", "Nippes", "Nord",
              "Nord-Est", "Nord-Ouest", "Ouest", "Sud", "Sud-Est"]:
        haiti.agregar_provincia(Provincia(p))

    jamaica = Pais("Jamaica", "Kingston", 10991)
    for p in ["Clarendon", "Hanover", "Kingston", "Manchester", "Portland",
              "Saint Andrew", "Saint Ann", "Saint Catherine",
              "Saint Elizabeth", "Saint James", "Saint Mary",
              "Saint Thomas", "Trelawny", "Westmoreland"]:
        jamaica.agregar_provincia(Provincia(p))

    # ── EUROPA OCCIDENTAL ────────────────────────────────────────────────────
    alemania = Pais("Alemania", "Berlín", 357114)
    for p in ["Baden-Württemberg", "Baviera", "Berlín", "Brandeburgo",
              "Bremen", "Hamburgo", "Hesse", "Baja Sajonia",
              "Mecklemburgo-Pomerania Occidental", "Renania del Norte-Westfalia",
              "Renania-Palatinado", "Sarre", "Sajonia",
              "Sajonia-Anhalt", "Schleswig-Holstein", "Turingia"]:
        alemania.agregar_provincia(Provincia(p))

    francia = Pais("Francia", "París", 643801)
    for p in ["Auvernia-Ródano-Alpes", "Borgoña-Franco Condado", "Bretaña",
              "Centro-Valle del Loira", "Córcega", "Gran Este",
              "Altos de Francia", "Isla de Francia", "Normandía",
              "Nueva Aquitania", "Occitania", "Países del Loira",
              "Provenza-Alpes-Costa Azul"]:
        francia.agregar_provincia(Provincia(p))

    espana = Pais("España", "Madrid", 505990)
    for p in ["Andalucía", "Aragón", "Asturias", "Islas Baleares",
              "País Vasco", "Islas Canarias", "Cantabria",
              "Castilla-La Mancha", "Castilla y León", "Cataluña",
              "Extremadura", "Galicia", "La Rioja", "Comunidad de Madrid",
              "Región de Murcia", "Navarra", "Comunidad Valenciana"]:
        espana.agregar_provincia(Provincia(p))

    italia = Pais("Italia", "Roma", 301340)
    for p in ["Abruzos", "Basilicata", "Calabria", "Campania",
              "Emilia-Romaña", "Friuli-Venecia Julia", "Lacio", "Liguria",
              "Lombardía", "Marcas", "Molise", "Piamonte",
              "Pulla", "Cerdeña", "Sicilia", "Trentino-Alto Adigio",
              "Toscana", "Umbría", "Valle de Aosta", "Véneto"]:
        italia.agregar_provincia(Provincia(p))

    reino_unido = Pais("Reino Unido", "Londres", 243610)
    for p in ["Inglaterra", "Escocia", "Gales", "Irlanda del Norte"]:
        reino_unido.agregar_provincia(Provincia(p))

    portugal = Pais("Portugal", "Lisboa", 92212)
    for p in ["Aveiro", "Beja", "Braga", "Braganza", "Castelo Branco",
              "Coimbra", "Évora", "Faro", "Guarda", "Leiria",
              "Lisboa", "Portalegre", "Oporto", "Santarém",
              "Setúbal", "Viana do Castelo", "Vila Real", "Viseu",
              "Azores", "Madeira"]:
        portugal.agregar_provincia(Provincia(p))

    paises_bajos = Pais("Países Bajos", "Ámsterdam", 41543)
    for p in ["Drenthe", "Flevoland", "Frisia", "Güeldres", "Groninga",
              "Limburgo", "Brabante Septentrional", "Holanda Septentrional",
              "Overijssel", "Utrecht", "Zelanda", "Holanda Meridional"]:
        paises_bajos.agregar_provincia(Provincia(p))

    belgica = Pais("Bélgica", "Bruselas", 30528)
    for p in ["Flandes", "Valonia", "Región de Bruselas-Capital"]:
        belgica.agregar_provincia(Provincia(p))

    suiza = Pais("Suiza", "Berna", 41285)
    for p in ["Zúrich", "Berna", "Lucerna", "Uri", "Schwyz",
              "Glaris", "Zug", "Friburgo", "Soleura", "Basilea-Ciudad",
              "Basilea-Campiña", "Schaffhausen", "San Galo", "Grisones",
              "Argovia", "Turgovia", "Tesino", "Vaud", "Valais",
              "Neuchâtel", "Ginebra", "Jura"]:
        suiza.agregar_provincia(Provincia(p))

    austria = Pais("Austria", "Viena", 83871)
    for p in ["Burgenland", "Carintia", "Baja Austria", "Alta Austria",
              "Salzburgo", "Estiria", "Tirol", "Vorarlberg", "Viena"]:
        austria.agregar_provincia(Provincia(p))

    irlanda = Pais("Irlanda", "Dublín", 70273)
    for p in ["Connacht", "Leinster", "Munster", "Ulster"]:
        irlanda.agregar_provincia(Provincia(p))

    islandia = Pais("Islandia", "Reikiavik", 103000)
    for p in ["Capital", "Penínsulas del Sur", "Fiordos Occidentales",
              "Noroeste", "Noreste", "Este", "Sur", "Reikjanes"]:
        islandia.agregar_provincia(Provincia(p))

    luxemburgo = Pais("Luxemburgo", "Luxemburgo", 2586)
    for p in ["Este", "Norte", "Sur"]:
        luxemburgo.agregar_provincia(Provincia(p))

    # ── EUROPA CENTRAL Y DEL ESTE ────────────────────────────────────────────
    polonia = Pais("Polonia", "Varsovia", 312696)
    for p in ["Baja Silesia", "Cuyavia-Pomerania", "Łódź", "Lublin",
              "Lubusz", "Pequeña Polonia", "Mazovia", "Opole",
              "Subcarpacia", "Podlaquia", "Pomerania", "Silesia",
              "Santa Cruz", "Varmia-Mazuria", "Gran Polonia",
              "Pomerania Occidental"]:
        polonia.agregar_provincia(Provincia(p))

    republica_checa = Pais("República Checa", "Praga", 78866)
    for p in ["Praga", "Bohemia Central", "Bohemia Meridional", "Plzeň",
              "Karlovy Vary", "Ústí nad Labem", "Liberec", "Hradec Králové",
              "Pardubice", "Olomouc", "Moravia-Silesia",
              "Moravia Meridional", "Zlín", "Vysočina"]:
        republica_checa.agregar_provincia(Provincia(p))

    eslovaquia = Pais("Eslovaquia", "Bratislava", 49035)
    for p in ["Bratislava", "Trnava", "Trenčín", "Nitra",
              "Žilina", "Banská Bystrica", "Prešov", "Košice"]:
        eslovaquia.agregar_provincia(Provincia(p))

    hungria = Pais("Hungría", "Budapest", 93028)
    for p in ["Budapest", "Pest", "Győr-Moson-Sopron", "Vas", "Zala",
              "Somogy", "Baranya", "Tolna", "Fejér", "Veszprém",
              "Komárom-Esztergom", "Bács-Kiskun", "Csongrád-Csanád",
              "Békés", "Hajdú-Bihar", "Jász-Nagykun-Szolnok",
              "Szabolcs-Szatmár-Bereg", "Heves", "Nógrád",
              "Borsod-Abaúj-Zemplén"]:
        hungria.agregar_provincia(Provincia(p))

    rumania = Pais("Rumania", "Bucarest", 238397)
    for p in ["Bucarest", "Cluj", "Timișoara", "Iași", "Constanța",
              "Craiova", "Brașov", "Galați", "Ploiești", "Oradea",
              "Brăila", "Arad", "Pitești", "Sibiu", "Bacău",
              "Târgu Mureș", "Baia Mare", "Buzău", "Botoșani", "Satu Mare"]:
        rumania.agregar_provincia(Provincia(p))

    # ── EUROPA DEL SUR Y BALCANES ────────────────────────────────────────────
    bulgaria = Pais("Bulgaria", "Sofía", 110879)
    for p in ["Sofía", "Plovdiv", "Varna", "Burgas", "Ruse",
              "Stara Zagora", "Pleven", "Sliven", "Dobrich", "Shumen",
              "Pernik", "Haskovo", "Yambol", "Pazardzhik", "Blagoevgrad",
              "Lovech", "Vidin", "Kardzhali", "Gabrovo", "Montana",
              "Targovishte", "Kyustendil", "Silistra", "Razgrad",
              "Vratsa", "Smolyan", "Veliko Tarnovo"]:
        bulgaria.agregar_provincia(Provincia(p))

    grecia = Pais("Grecia", "Atenas", 131957)
    for p in ["Ática", "Macedonia Central", "Macedonia Oriental y Tracia",
              "Macedonia Occidental", "Epiro", "Tesalia", "Grecia Central",
              "Islas Jónicas", "Grecia Occidental", "Peloponeso",
              "Egeo Septentrional", "Egeo Meridional", "Creta"]:
        grecia.agregar_provincia(Provincia(p))

    serbia = Pais("Serbia", "Belgrado", 77474)
    for p in ["Belgrado", "Vojvodina", "Šumadija", "Morava Occidental",
              "Morava Meridional", "Pomoravlje", "Bor", "Zaječar",
              "Zlatibor", "Moravica", "Raška", "Rasina",
              "Nišava", "Toplica", "Pirot", "Jablanica", "Pčinja"]:
        serbia.agregar_provincia(Provincia(p))

    croacia = Pais("Croacia", "Zagreb", 56594)
    for p in ["Zagreb", "Krapina-Zagorje", "Sisak-Moslavina", "Karlovac",
              "Varaždin", "Koprivnica-Križevci", "Bjelovar-Bilogora",
              "Primorje-Gorski Kotar", "Lika-Senj", "Virovitica-Podravina",
              "Požega-Slavonia", "Brod-Posavina", "Zadar",
              "Osijek-Baranja", "Šibenik-Knin", "Vukovar-Srijem",
              "Split-Dalmacia", "Istria", "Dubrovnik-Neretva", "Međimurje"]:
        croacia.agregar_provincia(Provincia(p))

    # ── EUROPA DEL NORTE ─────────────────────────────────────────────────────
    suecia = Pais("Suecia", "Estocolmo", 450295)
    for p in ["Estocolmo", "Uppsala", "Södermanland", "Östergötland",
              "Jönköping", "Kronoberg", "Kalmar", "Gotland", "Blekinge",
              "Skåne", "Halland", "Västra Götaland", "Värmland",
              "Örebro", "Västmanland", "Dalarna", "Gävleborg",
              "Västernorrland", "Jämtland", "Västerbotten", "Norrbotten"]:
        suecia.agregar_provincia(Provincia(p))

    noruega = Pais("Noruega", "Oslo", 385207)
    for p in ["Agder", "Innlandet", "Møre og Romsdal", "Nordland",
              "Oslo", "Rogaland", "Troms og Finnmark", "Trøndelag",
              "Vestfold og Telemark", "Vestland", "Viken"]:
        noruega.agregar_provincia(Provincia(p))

    finlandia = Pais("Finlandia", "Helsinki", 338145)
    for p in ["Laponia", "Ostrobotnia del Norte", "Kainuu", "Carelia del Norte",
              "Savo del Norte", "Savo del Sur", "Carelia del Sur",
              "Finlandia Central", "Ostrobotnia del Sur", "Ostrobotnia",
              "Ostrobotnia Central", "Pirkanmaa", "Satakunta",
              "Tavastia Propia", "Päijät-Häme", "Kymenlaakso",
              "Uusimaa", "Finlandia del Suroeste", "Åland"]:
        finlandia.agregar_provincia(Provincia(p))

    dinamarca = Pais("Dinamarca", "Copenhague", 42924)
    for p in ["Región Capital", "Zelanda", "Dinamarca Meridional",
              "Dinamarca Central", "Dinamarca del Norte"]:
        dinamarca.agregar_provincia(Provincia(p))

    # ── AGREGAR PAÍSES A CONTINENTES ─────────────────────────────────────────
    paises_america = [
        argentina, brasil, chile, uruguay, paraguay, bolivia, peru,
        colombia, venezuela, ecuador, guyana, suriname,
        usa, canada, mexico,
        guatemala, belize, honduras, el_salvador, nicaragua, costa_rica, panama,
        cuba, republica_dominicana, haiti, jamaica
    ]
    for p in paises_america:
        america.agregar_pais(p)

    paises_europa = [
        alemania, francia, espana, italia, reino_unido, portugal,
        paises_bajos, belgica, suiza, austria, irlanda, islandia, luxemburgo,
        polonia, republica_checa, eslovaquia, hungria, rumania,
        bulgaria, grecia, serbia, croacia,
        suecia, noruega, finlandia, dinamarca
    ]
    for p in paises_europa:
        europa.agregar_pais(p)

    # ── FRONTERAS ────────────────────────────────────────────────────────────
    # Sudamérica
    argentina.agregar_limitrofe(chile)
    argentina.agregar_limitrofe(bolivia)
    argentina.agregar_limitrofe(paraguay)
    argentina.agregar_limitrofe(uruguay)
    argentina.agregar_limitrofe(brasil)

    brasil.agregar_limitrofe(argentina)
    brasil.agregar_limitrofe(uruguay)
    brasil.agregar_limitrofe(paraguay)
    brasil.agregar_limitrofe(bolivia)
    brasil.agregar_limitrofe(peru)
    brasil.agregar_limitrofe(colombia)
    brasil.agregar_limitrofe(venezuela)
    brasil.agregar_limitrofe(guyana)
    brasil.agregar_limitrofe(suriname)

    chile.agregar_limitrofe(argentina)
    chile.agregar_limitrofe(bolivia)
    chile.agregar_limitrofe(peru)

    uruguay.agregar_limitrofe(argentina)
    uruguay.agregar_limitrofe(brasil)

    paraguay.agregar_limitrofe(argentina)
    paraguay.agregar_limitrofe(bolivia)
    paraguay.agregar_limitrofe(brasil)

    bolivia.agregar_limitrofe(argentina)
    bolivia.agregar_limitrofe(chile)
    bolivia.agregar_limitrofe(peru)
    bolivia.agregar_limitrofe(brasil)
    bolivia.agregar_limitrofe(paraguay)

    peru.agregar_limitrofe(ecuador)
    peru.agregar_limitrofe(colombia)
    peru.agregar_limitrofe(brasil)
    peru.agregar_limitrofe(bolivia)
    peru.agregar_limitrofe(chile)

    colombia.agregar_limitrofe(venezuela)
    colombia.agregar_limitrofe(brasil)
    colombia.agregar_limitrofe(peru)
    colombia.agregar_limitrofe(ecuador)
    colombia.agregar_limitrofe(panama)

    venezuela.agregar_limitrofe(colombia)
    venezuela.agregar_limitrofe(brasil)
    venezuela.agregar_limitrofe(guyana)

    ecuador.agregar_limitrofe(colombia)
    ecuador.agregar_limitrofe(peru)

    guyana.agregar_limitrofe(venezuela)
    guyana.agregar_limitrofe(brasil)
    guyana.agregar_limitrofe(suriname)

    suriname.agregar_limitrofe(guyana)
    suriname.agregar_limitrofe(brasil)

    # Norteamérica
    usa.agregar_limitrofe(canada)
    usa.agregar_limitrofe(mexico)
    canada.agregar_limitrofe(usa)
    mexico.agregar_limitrofe(usa)
    mexico.agregar_limitrofe(guatemala)
    mexico.agregar_limitrofe(belize)

    # Centroamérica
    guatemala.agregar_limitrofe(mexico)
    guatemala.agregar_limitrofe(belize)
    guatemala.agregar_limitrofe(honduras)
    guatemala.agregar_limitrofe(el_salvador)

    belize.agregar_limitrofe(mexico)
    belize.agregar_limitrofe(guatemala)

    honduras.agregar_limitrofe(guatemala)
    honduras.agregar_limitrofe(el_salvador)
    honduras.agregar_limitrofe(nicaragua)

    el_salvador.agregar_limitrofe(guatemala)
    el_salvador.agregar_limitrofe(honduras)

    nicaragua.agregar_limitrofe(honduras)
    nicaragua.agregar_limitrofe(costa_rica)

    costa_rica.agregar_limitrofe(nicaragua)
    costa_rica.agregar_limitrofe(panama)

    panama.agregar_limitrofe(costa_rica)
    panama.agregar_limitrofe(colombia)

    # Caribe (solo Haiti y R. Dominicana comparten frontera terrestre)
    haiti.agregar_limitrofe(republica_dominicana)
    republica_dominicana.agregar_limitrofe(haiti)

    # Europa Occidental
    alemania.agregar_limitrofe(francia)
    alemania.agregar_limitrofe(belgica)
    alemania.agregar_limitrofe(paises_bajos)
    alemania.agregar_limitrofe(suiza)
    alemania.agregar_limitrofe(austria)
    alemania.agregar_limitrofe(republica_checa)
    alemania.agregar_limitrofe(polonia)
    alemania.agregar_limitrofe(dinamarca)
    alemania.agregar_limitrofe(luxemburgo)

    francia.agregar_limitrofe(espana)
    francia.agregar_limitrofe(belgica)
    francia.agregar_limitrofe(luxemburgo)
    francia.agregar_limitrofe(alemania)
    francia.agregar_limitrofe(suiza)
    francia.agregar_limitrofe(italia)

    espana.agregar_limitrofe(francia)
    espana.agregar_limitrofe(portugal)

    italia.agregar_limitrofe(francia)
    italia.agregar_limitrofe(suiza)
    italia.agregar_limitrofe(austria)

    portugal.agregar_limitrofe(espana)

    belgica.agregar_limitrofe(francia)
    belgica.agregar_limitrofe(alemania)
    belgica.agregar_limitrofe(paises_bajos)
    belgica.agregar_limitrofe(luxemburgo)

    paises_bajos.agregar_limitrofe(belgica)
    paises_bajos.agregar_limitrofe(alemania)

    luxemburgo.agregar_limitrofe(francia)
    luxemburgo.agregar_limitrofe(belgica)
    luxemburgo.agregar_limitrofe(alemania)

    suiza.agregar_limitrofe(francia)
    suiza.agregar_limitrofe(alemania)
    suiza.agregar_limitrofe(austria)
    suiza.agregar_limitrofe(italia)

    austria.agregar_limitrofe(alemania)
    austria.agregar_limitrofe(suiza)
    austria.agregar_limitrofe(italia)
    austria.agregar_limitrofe(hungria)
    austria.agregar_limitrofe(republica_checa)
    austria.agregar_limitrofe(eslovaquia)

    reino_unido.agregar_limitrofe(irlanda)
    irlanda.agregar_limitrofe(reino_unido)

    # Europa Central y del Este
    polonia.agregar_limitrofe(alemania)
    polonia.agregar_limitrofe(republica_checa)
    polonia.agregar_limitrofe(eslovaquia)

    republica_checa.agregar_limitrofe(alemania)
    republica_checa.agregar_limitrofe(austria)
    republica_checa.agregar_limitrofe(eslovaquia)
    republica_checa.agregar_limitrofe(polonia)

    eslovaquia.agregar_limitrofe(republica_checa)
    eslovaquia.agregar_limitrofe(austria)
    eslovaquia.agregar_limitrofe(hungria)
    eslovaquia.agregar_limitrofe(polonia)

    hungria.agregar_limitrofe(austria)
    hungria.agregar_limitrofe(eslovaquia)
    hungria.agregar_limitrofe(rumania)
    hungria.agregar_limitrofe(serbia)
    hungria.agregar_limitrofe(croacia)

    rumania.agregar_limitrofe(hungria)
    rumania.agregar_limitrofe(serbia)
    rumania.agregar_limitrofe(bulgaria)

    # Balcanes
    bulgaria.agregar_limitrofe(rumania)
    bulgaria.agregar_limitrofe(serbia)
    bulgaria.agregar_limitrofe(grecia)

    grecia.agregar_limitrofe(bulgaria)

    serbia.agregar_limitrofe(hungria)
    serbia.agregar_limitrofe(rumania)
    serbia.agregar_limitrofe(bulgaria)
    serbia.agregar_limitrofe(croacia)

    croacia.agregar_limitrofe(hungria)
    croacia.agregar_limitrofe(serbia)

    # Europa del Norte
    suecia.agregar_limitrofe(noruega)
    suecia.agregar_limitrofe(finlandia)

    noruega.agregar_limitrofe(suecia)
    noruega.agregar_limitrofe(finlandia)

    finlandia.agregar_limitrofe(suecia)
    finlandia.agregar_limitrofe(noruega)

    dinamarca.agregar_limitrofe(alemania)

    return [america, europa]
