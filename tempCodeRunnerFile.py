# For debugging
if __name__ == "__main__":
    print("Settings loaded successfully!")
    print(f"Admin IDs: {settings.admin_ids_list}")
    print(f"User IDs: {settings.users_list}")
    print(f"AWS Bucket: {settings.AWS_BUCKET_NAME}")
    print(f"MongoDB URL: {settings.MONGODB_URL}")