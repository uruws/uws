$ aws iam list-users

$ aws iam list-groups-for-user --user-name nelson-tapo
$ aws iam remove-user-from-group --group-name admin --user-name nelson-tapo

$ aws iam get-login-profile --user-name nelson-tapo
$ aws iam delete-login-profile --user-name nelson-tapo

$ aws iam list-attached-user-policies --user-name nelson-tapo
$ aws iam detach-user-policy --policy-arn arn:aws:iam::aws:policy/IAMUserChangePassword --user-name nelson-tapo

$ aws iam list-access-keys --user-name nelson-tapo
$ aws iam delete-access-key --access-key-id AKIARQWMPSURTJKLLV4N --user-name nelson-tapo

$ aws iam delete-user --user-name nelson-tapo
