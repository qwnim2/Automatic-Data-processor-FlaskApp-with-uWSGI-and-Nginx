import dateutil
import pandas as pd

def flix_week_consumption(input_data):

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
        result +='\n'       # CSV format
    return result

def CPchat_difference(input_data):

    file = pd.read_csv(input_data)

    EVENT, RECEIVER, SENDER, AMOUNT = file.columns    
    df_group = file.groupby(EVENT)
    types = list(df_group.groups.keys())

    if "cost.amount" in types[0]:
        diamond = df_group.get_group(types[0])
        chat_qty = df_group.get_group(types[1])
    else:
        diamond = df_group.get_group(types[1])
        chat_qty = group.get_group(types[0])

    diamond_df = diamond[diamond[AMOUNT]>=500]
    alert_info = []

    for swagger, user, diamond in zip(diamond_df[RECEIVER], diamond_df[SENDER], diamond_df[AMOUNT]):
        for receiver1, sender1, user2cp in zip(chat_qty[RECEIVER], chat_qty[SENDER], chat_qty[AMOUNT]):
            # user send to swagger
            if swagger == receiver1 and user == sender1:
                for receiver2, sender2, cp2user in zip(chat_qty[RECEIVER], chat_qty[SENDER], chat_qty[AMOUNT]):
                    if user == receiver2 and swagger == sender2:
                        if cp2user/user2cp < 1:
                            ratio = round(cp2user/user2cp, 2)
                            alert_info.append([swagger, user, cp2user, user2cp, ratio, diamond])
                            
    result = 'CP,User,CP_to_User,User_to_CP,Ratio,Diamond\n'
    for line in alert_info:
        result += ','.join(line)
        result += '\n'
        
    return result