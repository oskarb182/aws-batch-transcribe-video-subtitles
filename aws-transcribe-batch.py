import boto3
import logging
from datetime import datetime


def transcribe_videos_in_folder(bucket, folder):
    logging.info('Iniciando script')
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m%d%Y%S")
    s3 = boto3.resource('s3')
    transcribe = boto3.client('transcribe')

    bucket = s3.Bucket(bucket)
    count = 1

    for obj in bucket.objects.filter(Prefix=folder):
        if obj.key.endswith('.mp4'):
            video_name = obj.key.split('/')[-1]
            job_name = date_time+video_name.split('.')[0]
            job_uri = f's3://{bucket.name}/{obj.key}'
            subtitle_name = video_name.replace('.mp4', '')
            output_key = f'{subtitle_name}'
            print('Creando job : ' + str(count) + ' : ' + output_key)
            transcribe.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': job_uri},
                Subtitles={'Formats': ['srt']},
                MediaFormat='mp4',
                LanguageCode='en-US',
                OutputBucketName=bucket.name,
                OutputKey='out/'+output_key
            )
            count += 1


def main():
    print('Iniciando')
    bucket = 'files-shared-bucket'
    folder = 'cantrill'

    transcribe_videos_in_folder(bucket, folder)


if __name__ == '__main__':
    main()
    print('Finalizo')
