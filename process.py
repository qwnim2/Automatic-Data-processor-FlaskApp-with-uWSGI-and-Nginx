def process_data(input_data):
    import dateutil
    import pandas as pd
    date_parser = dateutil.parser.parse

    file = pd.read_csv(input_data)

    info={}
    min_date = date_parser("2120/1/1").date()
    max_date = date_parser("1970/1/1").date()
    Event, Message_id, Premiere, Caption, Username, Diamond = file.columns

    debut_df = file[file[Diamond] ==1 ]
    for Id, Title, Date in zip(debut_df[Message_id], debut_df[Caption], debut_df[Premiere]):
        Title = Title[:Title.find('\n')]
        if date_parser(Date).date() < min_date:
            min_date = date_parser(Date).date()
        elif date_parser(Date).date() > max_date:
            max_date = date_parser(Date).date()
        info[Id] = [Title, "",Date, 0]  # {id:[Title, CP, Date, Diamond_consumption]}

    consumption_df = file[file[Diamond] !=1 ]
    for Id, Swagger, Date, Revenue in zip(consumption_df[Message_id],
                                          consumption_df[Username],
                                          consumption_df[Premiere],
                                          consumption_df[Diamond]):
        if Id in info.keys():
            Date = date_parser(Date).date()
            Debut = date_parser(info[Id][2]).date()
            delta = (Date-Debut).days
            if delta < 7:
                info[Id][1]=Swagger
                info[Id][3]+=Revenue

    result = 'ID,Title,CP,Premiere,Diamond\n'
    for Id in info.keys():
        result += ','.join([Id, info[Id][0], info[Id][1],info[Id][2], str(info[Id][3])])
        result +='\n'
    return result

