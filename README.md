# update-metadata-zenodo
This python script allows you to update the metadata of zenodo records in batches using the Zenodo RESTful API. Specifically, the current script adds a batch of records to the `meisebotanicgarden` community on Zenodo.

To use, you need Python3 and the listed packages. You will also need to create an API access token for your Zenodo account which owns the records you want to add to the community. 

- To create an API token, go to your Zenodo account settings and make a new token under the "Applications" menu. Enable both `deposit:actions` and `deposit:write`. Make sure to **copy and save the token** after creating it, but **never share** it with anyone else. You will not be able to see your token after creating it, but you can always delete it and create a new one if you forgot. After creating, **double-check that the `deposit` settings are enabled**.

- After creating the token, edit the `update_community.py` script by setting the token as the `access_token` variable.

- To process batches of records, you need the Zenodo record IDs for these records. List them in a text file similar to the examples in this repository, with `id` as a header.

- To launch the script, you can run `python3 update_community.py filename.txt` from the directory where both the script and the list of ids (`filename.txt`) can be found.

- To check whether everything went well, you can check the `quicklog upd.txt` file. All requests should give a response code of 200, 201 or 202. If there are any Python errors, they may be indicated here. Errors at the Zenodo side (e.g. 400, 403, 500) may be more extensively described in the logged JSON responses in the `updlog.txt` file. This file logs all JSON responses for all requests, so it may grow quite big, in particular if your records have a large number of files.
