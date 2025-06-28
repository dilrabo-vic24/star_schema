import uuid
from src import utils
import pandas as pd

def create_dimension_tables(df_raw):
    "create all dimensional data from raw_data.xlsx"

    #1.dim subject
    dim_subject = df_raw[['subject']].drop_duplicates().reset_index(drop = True)
    dim_subject['subject_id'] = dim_subject.index + 1
    dim_subject = dim_subject[['subject', 'subject_id']]

    #2. dim_comm_type
    dim_comm_type = df_raw[['comm_type']].drop_duplicates().reset_index(drop = True)
    dim_comm_type['comm_type_id'] = dim_comm_type.index + 1
    dim_comm_type = dim_comm_type[['comm_type_id', 'comm_type']]

    #3.dim_audio
    unique_audio = utils.extract_unique_from_raw_content(df_raw, "audio_url")
    dim_audio = pd.DataFrame(unique_audio, columns = ["raw_audio_url"])
    dim_audio["audio_id"] = dim_audio.index + 1
    dim_audio = dim_audio[["audio_id", "raw_audio_url"]]

    #4.dim_video
    unique_video = utils.extract_unique_from_raw_content(df_raw, "video_url")
    dim_video = pd.DataFrame(unique_video, columns = ["raw_video_url"])
    dim_video['video_id'] = dim_video.index + 1
    dim_video = dim_video[['video_id', 'raw_video_url']]


    parsed_content = df_raw['raw_content'].apply(utils.parse_raw_content)

    #5.dim_user(Meeting attendees)
    all_attendees = []
    
    for content in parsed_content:
        attendees = content.get('meeting_attendees', [])
        if attendees:
            all_attendees.extend(attendees)

    if not all_attendees:
        dim_user = pd.DataFrame(columns=['user_id', 'name', 'email', 'location', 'displayName', 'phoneNumber'])
    else:
        dim_user = pd.DataFrame(all_attendees)
        dim_user.drop_duplicates(inplace = True)
        dim_user.reset_index(drop=True, inplace=True)
        dim_user['user_id'] = dim_user.apply(lambda _: str(uuid.uuid4()), axis=1)
        dim_user = dim_user[['user_id', 'name', 'email', 'location', 'displayName', 'phoneNumber']]


    #6.dim_transcript
    unique_transcript = utils.extract_unique_from_raw_content(df_raw, "transcript_url")
    dim_transcript = pd.DataFrame(unique_transcript, columns = ["raw_transcript_url"])
    dim_transcript['transcript_id'] = dim_transcript.index + 1
    dim_transcript = dim_transcript[['transcript_id', 'raw_transcript_url']]

    #7.dim_calendar
    unique_calendar = utils.extract_unique_from_raw_content(df_raw, "calendar_id")
    dim_calendar = pd.DataFrame(unique_calendar, columns = ["raw_calendar_id"])
    dim_calendar['calendar_id'] = dim_calendar.index + 1
    dim_calendar = dim_calendar[['raw_calendar_id', 'calendar_id']]

    #all dimensions
    dimensions = {
        'dimm_subject': dim_subject,
        'dimm_comm_type': dim_comm_type,
        'dimm_user': dim_user,
        'dimm_audio': dim_audio,
        'dimm_video': dim_video,
        'dimm_transcript': dim_transcript,
        'dimm_calendar': dim_calendar
    }

    return dimensions