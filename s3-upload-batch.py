import os
import boto3
import sys

s3_resource = boto3.resource("s3", region_name="us-east-1")


def count_files(folder):
    try:

        count = 0
        for root_dir, cur_dir, files in os.walk(folder):
            count += len(files)

        return count
    except Exception as err:
        print(err)


def upload_objects(bucket_name, folder, root_path):
    try:

        my_bucket = s3_resource.Bucket(bucket_name)
        count = count_files(root_path)
        print('Total archivos:', count)
        total = 0
        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\", "/")
            for file in files:
                print('Subiendo archivo : '+str(total) +
                      ' de ' + str(count) + ' : ' + file)
                my_bucket.upload_file(os.path.join(
                    path, file), folder+'/'+file)
                total += 1

    except Exception as err:
        print(err)


def main():
    print('Iniciando')
    bucket_name = str(sys.argv[1])
    folder = str(sys.argv[2])
    root_path = str(sys.argv[3])

    print('Bucket :' + bucket_name)
    print('Folder :' + folder)
    print('Path :' + root_path)

    print('Iniciando')

    upload_objects(bucket_name, folder, root_path)


if __name__ == '__main__':
    main()
    print('Finalizo')
    # bucket_name = "files-shared-bucket"  # s3 bucket name
    #root_path = 'E:\curso\sanet.st_Adrian_Cantrill_-_AWS_Certified_Security_-_Specialty'
    # python s3-upload-batch.py files-shared-bucket cantrill E:\curso\AWS\AWS-Certified-DevOps-Engineer-Professional
