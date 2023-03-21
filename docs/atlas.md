Database Recovery process. 
Reference: https://www.mongodb.com/docs/atlas/backup/cloud-backup/restore-from-snapshot/#std-label-restore-from-snapshot

1
Click Database in the top-left corner of Atlas.

2
From the Database Deployments view, click on the database deployment name.

If the database deployment has no Backup tab, then Atlas backups are disabled for it and no snapshots are available.

3
Select the snapshot to restore and click Restore.

4
In the modal window, select the target database deployment from the dropdown menu.

5
Follow the prompt and click Restore.
6
Restart your application and ensure it uses the new target database deployment.