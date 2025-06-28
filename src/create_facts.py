import pandas as pd
from src import utils

def create_fact_bridge_tables(df_raw, dimensions):

    #create fact communication table(fact_communication)
    fact_table = df_raw.copy()

    fact_table = pd.merge(fact_table, dimensions["dimm_comm_type"], on="comm_type", how="left")
    fact_table = pd.merge(fact_table, dimensions["dimm_subject"], on="subject", how="left")

    parsed_content = fact_table['raw_content'].apply(utils.parse_raw_content)

    fact_table["raw_id"] = parsed_content.apply(lambda x: x.get("id"))
    fact_table['raw_audio_url'] = parsed_content.apply(lambda x: x.get('audio_url'))
    fact_table['raw_video_url'] = parsed_content.apply(lambda x: x.get('video_url'))
    fact_table['raw_transcript_url'] = parsed_content.apply(lambda x: x.get('transcript_url'))
    fact_table['raw_calendar_id'] = parsed_content.apply(lambda x: x.get('calendar_id'))

    fact_table = pd.merge(fact_table, dimensions['dimm_audio'], on='raw_audio_url', how='left')
    fact_table = pd.merge(fact_table, dimensions['dimm_video'], on='raw_video_url', how='left')
    fact_table = pd.merge(fact_table, dimensions['dimm_transcript'], on='raw_transcript_url', how='left')
    fact_table = pd.merge(fact_table, dimensions['dimm_calendar'], on='raw_calendar_id', how='left')

    fact_columns = [
        'id', 'raw_id', 'source_id', 'comm_type_id', 'subject_id', 'calendar_id',
        'audio_id', 'video_id', 'transcript_id', 'ingested_at',
        'processed_at', 'is_processed'
    ]
    fact_communication = fact_table[fact_columns].copy()

    fact_communication.rename(columns={'id': 'comm_id'}, inplace=True)

    final_fact_columns_order = [
        'comm_id', 'raw_id', 'source_id', 'comm_type_id', 'subject_id', 
        'calendar_id', 'audio_id', 'video_id', 'transcript_id',
        'ingested_at', 'processed_at', 'is_processed'
    ]
    fact_communication = fact_communication[final_fact_columns_order]


    #-----------------------------------------------------------------------


    #create bridge table(bridge_comm_user)
    all_records_long_list = []
    
    dim_user = dimensions['dimm_user']
    user_by_name = dim_user.dropna(subset=['name']).set_index('name')['user_id']
    user_by_email = dim_user.dropna(subset=['email']).set_index('email')['user_id']

    for index, row in df_raw.iterrows():
        comm_id = row['id']
        content = utils.parse_raw_content(row['raw_content'])
        
        def get_user_id(identifier, id_type):
            if pd.isna(identifier): return None
            user_map = user_by_name if id_type == 'name' else user_by_email
            user_id = user_map.get(identifier)
            if isinstance(user_id, pd.Series):
                return user_id.iloc[0]
            return user_id

        # add speakers
        for speaker in content.get('speakers', []):
            user_id = get_user_id(speaker.get('name'), 'name')
            if user_id:
                all_records_long_list.append({'comm_id': comm_id, 'user_id': user_id, 'role': 'speaker'})

        #emails
        all_emails = set(content.get('participants', []))
        all_emails.update(attendee.get('email') for attendee in content.get('meeting_attendees', []) if attendee.get('email'))
        
        for email in all_emails:
            user_id = get_user_id(email, 'email')
            if user_id:
                all_records_long_list.append({'comm_id': comm_id, 'user_id': user_id, 'role': 'attendee'})
        
        # organizer
        organizer_email = content.get('organizer_email')
        if organizer_email:
            user_id = get_user_id(organizer_email, 'email')
            if user_id:
                all_records_long_list.append({'comm_id': comm_id, 'user_id': user_id, 'role': 'organiser'})

    #create dataframe from all_recors_long_list
    if not all_records_long_list:
        bridge_comm_user = pd.DataFrame(columns=['comm_id', 'user_id', 'isAttendee', 'isParticipant', 'isSpeaker', 'isOrganiser'])
    else:
        df_long = pd.DataFrame(all_records_long_list)

        df_long.drop_duplicates(inplace=True)

        df_long['isSpeaker'] = df_long['role'] == 'speaker'
        df_long['isAttendee'] = df_long['role'] == 'attendee'
        df_long['isParticipant'] = df_long['role'] == 'participant'
        df_long['isOrganiser'] = df_long['role'] == 'organiser'

        bridge_comm_user = df_long.groupby(['comm_id', 'user_id']).agg({
            'isSpeaker': 'max',
            'isAttendee': 'max',
            'isParticipant': 'max',
            'isOrganiser': 'max'
        }).reset_index()

        is_attending_or_participating = bridge_comm_user['isAttendee'] | bridge_comm_user['isParticipant']
        bridge_comm_user['isAttendee'] = is_attending_or_participating
        bridge_comm_user['isParticipant'] = is_attending_or_participating
        
        bool_columns = ['isSpeaker', 'isAttendee', 'isParticipant', 'isOrganiser']
        for col in bool_columns:
            bridge_comm_user[col] = bridge_comm_user[col].astype(bool)

    facts = {
        'fact_communication': fact_communication,
        'bridge_comm_user': bridge_comm_user
    }
    
    return facts