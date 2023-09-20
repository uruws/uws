Meteor App Environment Variables
================================

* AMPLITUDE_API_KEY
    * FIXME

* AMPLITUDE_PARENTS_API_KEY
    * FIXME

* APM_ENDPOINT
    * FIXME

* APM_ID
    * FIXME

* APM_SECRET
    * FIXME

* AUTOUPDATE_VERSION
    * We need this to have the very __exact__ same value on any App instance running. To avoid client refresh.
    * See: https://guide.meteor.com/hot-code-push.html

* AWS_API_KEY
    * FIXME

* BACKUP_SMS_RECEIVER_URL
    * FIXME

* BANDWIDTH_ACCOUNT_ID
    * FIXME

* BANDWIDTH_API_PASSWORD
    * FIXME

* BANDWIDTH_API_USERNAME
    * FIXME

* BANDWIDTH_APPLICATIONID
    * FIXME

* BANDWIDTH_LOCATION
    * FIXME

* BANDWIDTH_SITE_ID
    * FIXME

* BANDWIDTH_TOKEN
    * FIXME

* BANDWIDTH_TOKENSECRET
    * FIXME

* BIGQUERY_DATASET_ID
    * FIXME

* BIGQUERY_PROJECT_ID
    * FIXME

* CAPTIONS_ENABLED
    * FIXME

* CDN_URL
    * AWS CDN used for serving assets.
    * It __must__ have the following format: `https://cdn.domain`
        * It __must__ start with `https://`
        * It __must__ __not__ end with an `/`

* CENSOR_ENABLED
    * FIXME

* CLASSIFIER_ID
    * FIXME

* CLASSIFIER_PASSWORD
    * FIXME

* CLASSIFIER_USERNAME
    * FIXME

* CLEVER_CLIENT_ID
    * FIXME

* CLEVER_CLIENT_SECRET
    * FIXME

* CLEVER_ON
    * Boolean to check if it should run cleverSync jobs

* COCONUT_WEBHOOK
    * FIXME

* CONCURRENCY_MESSAGES
    * FIXME

* DEMO_TWILIO_NUMBER
    * FIXME

* DISABLED_CLASSIFIER_URL
    * FIXME

* DISABLE_JOBS
    * Disable the App to behave like a __worker__ and process background jobs.
    * On web instances it __must__ be set as `DISABLE_JOBS=TRUE`.

* DISABLE_LOGS
    * FIXME

* DISABLE_SET_RECIPIENTS
    * FIXME

* DISABLE_SOCKJS
    * Allway set it as `1` to avoid buggy sockjs implementation.

* FIREBASE_SERVER_KEY_PARENTS
    * FIXME

* FIREBASE_SERVER_KEY_TEACHERS
    * FIXME

* FTP_PASSWORD
    * FIXME

* GENGO_PRIVATE
    * FIXME

* GENGO_PUBLIC
    * FIXME

* GEO_IP_API_KEY
    * FIXME

* GOOGLE_APPLICATION_CREDENTIALS
    * FIXME

* GOOGLE_SHEET_ID
    * FIXME

* GOOGLE_SHEET_PRIVATE_KEY
    * FIXME

* GOOGLE_SHEETS_ID
    * FIXME

* GOOGLE_SHEET_TRANSLATION_EMAIL
    * FIXME

* INFINITECAMPUS_ON
    * Boolean to check if it should run infiniteCampusSync jobs

* IOS_APP_ID
    * FIXME

* LOGTAIL_TOKEN
    * FIXME

* MAIL_URL
    * FIXME

* MANDRILL_API_KEY
    * FIXME

* MAX_ASSIGNATIONS_PER_PHONE
    * FIXME

* MAXIMUM_LOGIN_ATTEMPTS_TIMEOUT
    * FIXME

* MESSAGES_POLLING_INTERVAL_MS
    * FIXME

* MESSAGES_POLLING_THROTTLE_MS
    * FIXME

* METEOR_POLLING_INTERVAL_MS
    * FIXME

* METEOR_POLLING_THROTTLE_MS
    * FIXME

* MIN_NUMBER_SPREAD
    * FIXME

* MIN_STUDENTS_TO_HOLD_POST
    * FIXME

* MONGO_REPLICA_URL
    * MongoDB server's replicas URL.

* MONGO_URL
    * MongoDB server's URL to connect to.

* MYSQL_DB
    * FIXME

* MYSQL_HOST
    * FIXME

* MYSQL_PASSWORD
    * FIXME

* MYSQL_USER
    * FIXME

* NODE_ENV
    * FIXME

* NODEJS_PARAMS
    * FIXME

* NODE_OPTIONS
    * FIXME

* ONE_HOUR_TRANSLATION_PUBLIC
    * FIXME

* ONE_HOUR_TRANSLATION_SECRET
    * FIXME

* ONEROSTER_ON
    * Boolean to check if it should run oneRosterSync jobs

* OPEN_AI_API_KEY
    * FIXME

* PARENT_APP_STORE_LINK
    * FIXME

* PARENTS_STT_ENABLED
    * FIXME

* POLLING_INTERVAL_MS
    * FIXME

* POLLING_THROTTLE_MS
    * FIXME

* PORT
    * Meteor TCP port to bind to.

* RECAPTCHA_PUBLIC
    * FIXME

* RECAPTCHA_SECRET
    * FIXME

* REDISCLOUD_URL
    * FIXME

* ROOT_URL
    * Application main URL.

* ROSTERSTREAM_ON
    * Boolean to check if it should run rosterStreamSync jobs

* RUNMIGRATIONS
    * FIXME

* SFTP_ON
    * FIXME

* SKYWARD_ON
    * Boolean to check if it should run skywardSync jobs

* SMS_NOTIFICATIONS_NUMBER
    * FIXME

* SMS_RECEIVER_URL
    * FIXME

* STRIPE
    * FIXME

* STRIPE_ENABLED
    * FIXME

* TEACHER_PREMIUM_PRICE
    * FIXME

* TOOL_NODE_FLAGS
    * FIXME

* TRANSLATE
    * FIXME

* TRANSLATION_ENGINE_TOKEN
    * FIXME

* TRANSLATION_ENGINE_URL
    * FIXME

* TWILIO
    * FIXME

* TWILIO_ACCOUNT_SID
    * FIXME

* TWILIO_AUTH_TOKEN
    * FIXME

* USE_BOOT_PROXY
    * FIXME

* USE_NEW_FEED_QUERY
    * FIXME

* USE_NEW_MESSAGES_QUERY
    * FIXME

* VIDEO_CAPTIONS_API_KEY
    * FIXME

* WATSON_NLU_PASSWORD
    * FIXME

* WATSON_NLU_URL
    * FIXME

* WATSON_NLU_USERNAME
    * FIXME
