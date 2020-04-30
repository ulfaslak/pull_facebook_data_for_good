# Pull Facebook Data for Good

This is a fork of hamishgibbs' original repository by the same name. I have changed and added some functionality, most notably:

* Check for existing data files and only download new ones
* Change `datasets.csv` structure, so it is possible to pull both raster and vector data
* Change the way files are stored. Now, they are stored in a new directory that matches the `country/type/` column values of `datasets.csv`. This is a bit more orderly.
* I removed the username and password encryption, because I couldn't make it work, and I didn't have time to figure it out. From a security standpoint this is obviously bad, but if you're running this code in your local machine it shouldn't be an issue. I would, however, appreciate if someone made a pull request adding it back and incluing proper instructions on how to make it work (writing those instructions into this README).
* I removed all the testing, and colocation scripts because I didn't need them. But I'm sure pulling colocation can be added back so you don't need a separate script (i.e. so they can be added to `datasets.csv` and downloaded in th same execution as other data). If you fork this and make it work, a PR is very welcome!

In summary, this code is (at the time of writing) more minimal, a little easier to use, does some important things that the hamishgibbs' does not, but is less complete. Please check out [the original repo](https://github.com/hamishgibbs/pull_facebook_data_for_good).

**To get it working:**

1. Download the [*chromedriver*](https://chromedriver.chromium.org/downloads) and put in your /Applications folder. If that doesn't work for you, you can put it somewhere else, then you just have to make sure the path inside the `download_data` function matches its location.
2. Save your Facebook credentials inside ~/.creds/fb.json. The file should contain a list object, like `["my@email.com", "23cr3tp4ssw0rD"]`, that is your facebook credentials. Again, you can put it elsewhere, but then you should make sure the path defined on the first line of the `Makefile` matches.
3. Change the `datasets.csv` file so it points to the datasets you need. Each row defines a dataset you want to download. The `type` field can be set to anything, and essentially just controls the name of the folder that this collections of data is moved to. The `addr` field needs to match the part of the download url that comes after `https://www.facebook.com/geoinsights-portal/` part and before the arguments (delimited by a `?`). To get the `id` you need to manually go to the GeoInsights portal, click 'Download' on the dataset and copy it from the url.
4. Set the paths inside the `Makefile` so files end up where you need.
5. Execute `make pull`.



**How it's working**

It loads your credentials, then loads the `datasets.csv` file and starts a `for` loop over its rows. In each iteration it:

1. Figures out how many files it needs to download. This works by taking the maximum of the defined `start_date` and the datetime (+8 hours) of the most recently downloaded file of the same type.
2. Launches an instance of the `chromedriver`, logs in with your credentials and starts downloading files from the top (with a 1 sleep wait between each).
3. Files are default Downloaded into your ~/Downloads folder, so in the next step it moves them (the `len(url)` most recent files in ~/Downloads) into a new or existing folder `f"{_args[2]}/{row.country}/{row.type}"`, where `row` is the variable containing the iterated row of `datasets.csv` and `_args[2]` is the `OUTDIR` defined in the `Makefile`.